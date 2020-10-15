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

    id = Column(Integer, primary_key = True, index = True)
    user_id = Column(VARCHAR(10))
    user_name = Column(VARCHAR(20))
    password = Column(VARCHAR(20))
    content_id = Column(DECIMAL(6))
    user_answer = Column(DECIMAL(1))
    answered_correctly = Column(DECIMAL(1))
    prior_question_elapsed_time = Column(DECIMAL(10))

    # def __repr__(self):
    #     return f'User(id=\'{self.id}\',userid=\'{self.user_id}'


df = pd.read_csv('./mangotoeic/user/data/train.csv')
df_sample = df[['user_id', 'user_name', 'password', 'content_id', 'user_answer', 'answered_correctly', 'prior_question_elapsed_time']]
df_sample_head = df_sample.head(2000)
engine = create_engine('mysql+mysqlconnector://root:root@127.0.0.1/mariadb?charset=utf8', encoding='utf8', echo=True)
conn = engine.connect()
df_sample_head.to_sql(name='users', con=engine)

# Base.metadata.create_all(engine)
# Session = sessionmaker(bind=engine)
# session = Session()
# session.add(User(User.load_data()))
# query = session.query(User).filter((User.userid == 'tom'))
# print(query)
# for i in query:
#     print(i)
    
# session.commit()
