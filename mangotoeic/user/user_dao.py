from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from user_dto import User
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

    def create_table(self):
        Base.metadata.create_all(self.engine)

    def userdata_to_sql(self):
        df = pd.read_csv('./mangotoeic/user/data/sample.csv') # 정제된 데이터로 변경 예정
        # df_sample = df[['user_id', 'content_id', 'user_answer', 'answered_correctly', 'prior_question_elapsed_time']]
        # df_sample_head = df_sample.head(100)
        self.conn = self.engine.connect()
        # self.base.metadata.create_all(self.engine)
        df.to_sql(name='users', con=self.conn, if_exists='append', index=False)

    def add_user(self, userid):
        user = User(user_id=userid)
        self.session.add(user)
        self.session.commit()

    def fetch_user(self, userid):
        query = self.session.query(User).filter((User.user_id == userid))
        return query[0]

    def fetch_all_users(self):
        querys = self.session.query(User).all()
        return querys

    def update_user(self, userid, column, value):
        user = self.session.query(User).filter(User.user_id == userid).update({column : value})
        self.session.commit()

    def delete_user(self, userid):
        user = self.session.query(User).filter(User.user_id == userid).first()
        self.session.delete(user)
        self.session.commit()

if __name__ == "__main__":
    userdao = UserDao()
    # userdao.userdata_to_sql()
    # userdao.add_user('666')
    # userdao.delete_user('115')
    userdao.update_user('5382', 'content_id', '777')