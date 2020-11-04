from typing import List
from flask import request
from flask_restful import Resource, reqparse 
from mangotoeic.review.fromweb import WebCrawler
from mangotoeic.review.model import Prepro 
 
from mangotoeic.ext.db import engine
from flask import jsonify
import keras
import numpy as np
 
from mangotoeic.ext.db import db, openSession
from mangotoeic.review.model import Prepro 
from mangotoeic.user.dto import UserDto
from sqlalchemy import func
import pandas as pd
import json

class ReviewDto(db.Model):
    __tablename__ = "reviews"
    __table_args__ = {'mysql_collate':'utf8_general_ci'}

    id: int = db.Column(db.Integer, primary_key=True, index=True)
    email : str = db.Column(db.String(500)) 
    # , db.ForeignKey(UserDto.email) 
    review: str = db.Column(db.String(500))
    star: int = db.Column(db.Integer) 
  
    
    def __init__(self, id = None, email=None, review=None, star=None):
        self.id = id
        self.email = email
        self.review = review
        self.star = star 
    

    def __repr__(self):
        return f'Review(id=\'{self.id}\',email=\'{self.email}\',review=\'{self.review}\', star=\'{self.star}\',)'

    @property
    def json(self):
        return {
            'id' : self.id,
            'email' : self.email,
            'review' : self.review,
            'star' : self.star
        }

class ReviewVo:
    id: int = 1
    email : str = ''
    review: str = ''
    star: int = 1
    

    
class ReviewService(object):

    @staticmethod
    def predict(input):
        wc = WebCrawler()
        model = Prepro()
        reviewtext = wc.strip_emoji(input.review)
        reviewtext = wc.cleanse(reviewtext)
        reviewtext = model.tokenize(reviewtext, model.get_stopwords())
        reviewtext = model.encoding(reviewtext)
        reviewtext = model.zeropadding(reviewtext)

        rnnmodel = keras.models.load_model('RNN_review_star_model.h5')
        predictions = rnnmodel.predict(reviewtext)
        prob = predictions[-1][np.argmax(predictions[-1])]*100
        prob = round(prob, 2)
        star = int(np.argmax(predictions[-1])) + 1
        return [prob,star]
        


# ==============================================================
# =====================                  =======================
# =====================    Dao    =======================
# =====================                  =======================
# ==============================================================


Session = openSession()
session = Session()

class ReviewDao(ReviewDto):
    
    @staticmethod
    def find_all():
        return session.query(ReviewDto).all()

    @classmethod 
    def find_by_email(cls,email):
        return session.query(ReviewDto).filter(ReviewDto.email.like(f'%{email}%')).all() 
      

    @classmethod
    def find_by_id(cls,id):
        return session.query(ReviewDto).filter(ReviewDto.email.like(f'%{id}%')).one()

    @classmethod
    def find_by_star(cls,star):
        return session.query(ReviewDto).filter(ReviewDto.email.like(f'%{star}%')).all()

    @classmethod
    def find_by_review(cls,review):
        return session.query(ReviewDto).filter(ReviewDto.email.like(f'%{review}%')).all()

    @staticmethod
    def save(review):
        session.add(review)
        session.commit()
        
    @staticmethod
    def update(review):
        Session = openSession()
        session = Session()
        session.add(review)
        session.commit()

    @classmethod
    def delete(cls,id):
        Session = openSession()
        session = Session()
        data = cls.query.get(id)
        session.delete(data)
        session.commit()
    
    @staticmethod
    def count():
        Session = openSession()
        session = Session()
        return session.query(func.count(ReviewDto.id)).one()

    @staticmethod
    def insert_many():
        service = Prepro()
        Session = openSession()
        session = Session()
        df = service.get_data()
        print(df.head())
        session.bulk_insert_mappings(ReviewDto, df.to_dict(orient = 'records'))
        session.commit()
        session.close()
        print('done') 

     


# ==============================================================
# =====================                  =======================
# =====================    Resourcing    =======================
# =====================                  =======================
# ==============================================================


parser = reqparse.RequestParser()

parser.add_argument('email', type = str, required = True, help = 'This field should be email, cannot be left blank')
parser.add_argument('review', type = str, required = True, help = 'This field should be review, cannot be left blank') 

class Review(Resource):

    @staticmethod
    def post():
        args = parser.parse_args()
        probstar = ReviewService.predict(args)
        print(f'예측 별점은 {probstar[0]}% 의 확률로 {probstar[1]}입니다')
        new_review = ReviewDto(email=args.email, review=args.review, star=probstar[1])
        print(new_review)
        try:
            ReviewDao.save(new_review) 
            return {'star': probstar[1], 'prob':probstar[0]}, 200
        except:
            return {'message' : ' an error occured while inserting review'}, 500 

    @staticmethod
    def get(email):
        try:
            review = ReviewDao.find_by_email(email)
            if review:
                return review.json()
        except Exception as e:
            return {'message': 'review not found'}, 404 

    @staticmethod
    def update():
        args = parser.parse_args()
        print(f'Review {args.email} updated')
        return {'code' :0, 'message' : 'Success'}, 200

    @staticmethod
    def delete():
        args = parser.parse_args()
        print(f'Review posted by {args.email} deleted')
        return {'code' :0, 'message' : 'Success'}, 200

 

class Reviews(Resource): 

    @staticmethod
    def get():
        df = pd.read_sql_table('reviews', engine.connect()) 
        return json.loads(df.to_json(orient = 'records'))

    @staticmethod
    def post():
        rd = ReviewDao()
        rd.insert_many('reviews')
        