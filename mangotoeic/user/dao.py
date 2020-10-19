from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from mangotoeic.user.dto import UserDto
from mangotoeic.ext.db import Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.mysql import DECIMAL, VARCHAR, LONGTEXT
import pandas as pd


class UserDao():
    engine = create_engine('mysql+mysqlconnector://root:root@127.0.0.1/mariadb?charset=utf8', encoding='utf8', echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    base = Base()

    def __init__(self):
        pass

    def userdata_to_sql(self):
        df = pd.read_csv('./mangotoeic/user/data/sample.csv') # 정제된 데이터로 변경 예정
        # df_sample = df[['user_id', 'content_id', 'user_answer', 'answered_correctly', 'prior_question_elapsed_time']]
        # df_sample_head = df_sample.head(100)
        self.conn = self.engine.connect()
        # self.base.metadata.create_all(self.engine)
        df.to_sql(name='users', con=self.conn, if_exists='append', index=False)

    def add_user(self, user_id, content_id, user_answer, answered_correctly, prior_question_elapsed_time):
        user = UserDto(user_id=user_id, content_id=content_id, user_answer=user_answer, answered_correctly=answered_correctly, prior_question_elapsed_time=prior_question_elapsed_time)
        self.session.add(user)
        self.session.commit()

    def fetch_user(self, userid):
        query = self.session.query(UserDto).filter((UserDto.user_id == userid))
        return query[0]

    def fetch_all_users(self):
        querys = self.session.query(UserDto).all()
        return querys

    def update_user(self, userid, column, value):
        user = self.session.query(UserDto).filter(UserDto.user_id == userid).update({column : value})
        self.session.commit()

    def delete_user(self, userid):
        user = self.session.query(UserDto).filter(UserDto.user_id == userid).first()
        self.session.delete(user)
        self.session.commit()

if __name__ == "__main__":
    userdao = UserDao()
    # userdao.userdata_to_sql()
    userdao.add_user('444', 9834, 3, 1, 39000)
    # userdao.delete_user('115')
    # userdao.update_user('124', 'user_answer', '123')
    # a = userdao.fetch_user('666')