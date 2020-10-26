from mangotoeic.ext.db import db, openSession
from mangotoeic.review.tokenizer import Prepro
from mangotoeic.review.dto import ReviewDto 
from mangotoeic.user.dto import UserDto
import pandas as pd
import json

class ReviewDao(ReviewDto):
    
    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod 
    def find_by_user_id(cls,user_id):
        return cls.query.filter_by(user_id==user_id).all()

    @classmethod
    def find_by_id(cls,id):
        return cls.query.filter_by(id==id).first()

    @classmethod
    def find_by_star(cls,star):
        return cls.query.filter_by(star==star).first()

    @staticmethod
    def save(review):
        print(review)
        Session = openSession()
        session = Session()
        """"asasdasdasddddddddddnklkladskdsklndsnklsadnkdsnjsk"""
        """"asasdasdasddddddddddnklkladskdsklndsnklsadnkdsnjsk"""
        """"asasdasdasddddddddddnklkladskdsklndsnklsadnkdsnjsk"""
        """"asasdasdasddddddddddnklkladskdsklndsnklsadnkdsnjsk"""
        star
        newReview = ReviewDto(id = review['id'], user_id = review['user_id'], review = review['review'], star )
         
    @staticmethod
    def insert_many():
        service = Prepro()
        Session = openSession()
        session = Session()
        df = service.get_data()
        # print(df.head())
        session.bulk_insert_mappings(ReviewDto, df.to_dict(orient = 'records'))
        session.commit()
        session.close()
        print('done') 
        
    @staticmethod
    def modify_review(review):
        db.session.add(review)
        db.session.commit()

    @classmethod
    def delete_review(cls,id):
        data = cls.query.get(id)
        db.session.delete(data)
        db.session.commit()

# rd = ReviewDao()
# rd.insert_many()

     