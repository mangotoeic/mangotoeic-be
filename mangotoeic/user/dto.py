from sqlalchemy import  create_engine
from mangotoeic.ext.db import db
from sqlalchemy.orm import sessionmaker

import pandas as pd

# 토익 시험 몇번 봤는지, 목표점수, 시험날짜, 본인의 영어실력 입력
# 데이터 베이스에 반영할 건지?

class UserDto(db.Model):
    __tablename__ = 'users'
    __table_args__={'mysql_collate':'utf8_general_ci'}

    user_id = db.Column(db.Integer, primary_key=True, index=False)
    user_name = db.Column(db.String(20))
    password = db.Column(db.String(20))
    qId = db.Column(db.Integer)
    user_answer = db.Column(db.Integer)
    answered_correctly = db.Column(db.Float)
    prior_question_elapsed_time = db.Column(db.Float)
    email = db.Column(db.String(20))
    confirmPassword = db.Column(db.String(20))

    # def __repr__(self):
    #     return f'id={self.user_id}, userid={self.user_name} password={self.password}, qId={qId}'

    def __init__(self, user_id=None, qId=None, user_answer=None, answered_correctly=None, prior_question_elapsed_time=None):
        self.user_id = user_id
        self.qId = qId
        self.user_answer = user_answer
        self.answered_correctly = answered_correctly
        self.prior_question_elapsed_time = prior_question_elapsed_time




    @property
    def json(self):
        return {
            'user_id' : self.user_id,
            'user_name' : self.user_name,
            'password' : self.password,
            'qId' : self.qId,
            'user_answer' : self.user_answer,
            'answered_correctly': self.answered_correctly,
            'prior_question_elapsed_time': self.prior_question_elapsed_time
        }
        
        
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class UserVo:
    password: str = ''
    email: str = ''
    user_id : int = 0 
    user_name : str = ''
    password : str = ''
    qId : int = 0 
    user_answer : int = 0 
    answered_correctly : float = 0
    prior_question_elapsed_time : float = 0 
    email : str = ''
    confirmPassword : str = ''