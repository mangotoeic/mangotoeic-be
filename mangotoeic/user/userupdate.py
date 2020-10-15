from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from mangotoeic.ext.db import Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.mysql import DECIMAL, VARCHAR, LONGTEXT
import pandas as pd

# 토익 시험 몇번 봤는지, 목표점수, 시험날짜, 본인의 영어실력 입력
# 데이터 베이스에 반영할 건지?

class UserUpdate(Base):
    __tablename__ = 'users'
    __table_args__={'mysql_collate':'utf8_general_ci'}

    id = Column(Integer, primary_key = True, index = True)
    user_id = Column(VARCHAR(10))
    content_id = Column(DECIMAL(6))
    user_answer = Column(DECIMAL(1))
    answered_correctly = Column(DECIMAL(1))
    prior_question_elapsed_time = Column(DECIMAL(10))
    level = Column(DECIMAL(1))
    score_pred = Column(DECIMAL(3))

    # def __repr__(self):
    #     return f'User(id=\'{self.id}\',userid=\'{self.user_id}'


df = pd.read_csv('./mangotoeic/user/data/train.csv')
df_sample = df[['user_id', 'content_id', 'user_answer', 'answered_correctly', 'prior_question_elapsed_time']]
df_sample_tail = df_sample.tail(100)
engine = create_engine('mysql+mysqlconnector://root:root@127.0.0.1/mariadb?charset=utf8', encoding='utf8', echo=True)
conn = engine.connect()

# 입력값을 받아서 columns을 add