from typing import List
from flask import request
from flask_restful import Resource, reqparse
from mangotoeic.review.dao import ReviewDao
from mangotoeic.review.fromweb import WebCrawler
from mangotoeic.review.model import Prepro
from mangotoeic.review.dto import ReviewDto, ReviewVo
import json
import pandas as pd
from mangotoeic.ext.db import engine
from flask import jsonify
import keras
import numpy as np

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
        
