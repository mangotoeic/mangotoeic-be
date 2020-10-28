from mangotoeic.ext.db import db, openSession
from mangotoeic.review.model import Prepro
from mangotoeic.review.dto import ReviewDto 
from mangotoeic.user.dto import UserDto
from sqlalchemy import func
import pandas as pd
import json
Session = openSession()
session = Session()
class ReviewDao(ReviewDto):
    
    @staticmethod
    def find_all():
        
        df = session.query(ReviewDto).all() 
        return session.query(ReviewDto).all()

    @classmethod 
    def find_by_user_id(cls,email):
        return cls.query.filter_by(email==email).all()

    @classmethod
    def find_by_id(cls,id):
        return cls.query.filter_by(id==id).first()

    @classmethod
    def find_by_star(cls,star):
        return cls.query.filter_by(star==star).first()

    @staticmethod
    def save(review):
        session.add(review)
        session.commit()
        
    @staticmethod
    def modify_review(review):
        Session = openSession()
        session = Session()
        session.add(review)
        session.commit()

    @classmethod
    def delete_review(cls,id):
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

     