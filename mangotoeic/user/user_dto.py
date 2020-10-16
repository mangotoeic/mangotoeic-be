from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from mangotoeic.ext.db import Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.mysql import DECIMAL, VARCHAR, LONGTEXT
import pandas as pd

# 토익 시험 몇번 봤는지, 목표점수, 시험날짜, 본인의 영어실력 입력
# 데이터 베이스에 반영할 건지?

class User(Base):
    __tablename__ = 'users'
    __table_args__={'mysql_collate':'utf8_general_ci'}

    user_id = Column(VARCHAR(10), primary_key=True, index=False)
    # user_name = Column(VARCHAR(20))
    # password = Column(VARCHAR(20))
    content_id = Column(DECIMAL(6))
    user_answer = Column(DECIMAL(1))
    answered_correctly = Column(DECIMAL(1))
    prior_question_elapsed_time = Column(DECIMAL(10))

    # def __repr__(self):
    #     return f'id={self.user_id}, userid={self.user_name} password={self.password}, content_id={content_id}'


    @property
    def serilize(self):
        return {
            'user_id' : self.user_id,
            # 'user_name' : self.user_name,
            # 'password' : self.password,
            'content_id' : self.content_id,
            'user_answer' : self.user_answer,
            'answered_correctly': self.answered_correctly,
            'prior_question_elapsed_time': self.prior_question_elapsed_time
        }

class UserDto(object):
    user_id : str
    # user_name : str
    # password : str
    content_id : int
    user_answer : int
    answered_correctly: int
    prior_question_elapsed_time: int