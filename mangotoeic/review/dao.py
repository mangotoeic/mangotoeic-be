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

     