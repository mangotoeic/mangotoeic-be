from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from mangotoeic.ext.db import db, openSession
from mangotoeic.user.dto import UserDto
from sqlalchemy.orm import sessionmaker
from mangotoeic.ext.db import Base
import pandas as pd
import json


class UserDao(UserDto):
    engine = create_engine('mysql+mysqlconnector://root:root@127.0.0.1/mariadb?charset=utf8', encoding='utf8', echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    base = Base()

    def __init__(self):
        pass

    @classmethod
    def userdata_to_sql(self):
        df = pd.read_csv('./mangotoeic/user/data/user_table_prepro.csv',) # 정제된 데이터로 변경 예정
        self.conn = self.engine.connect()
        df.to_sql(name='users', con=self.conn, if_exists='append', index=False)

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filer_by(name == name).all()

    @classmethod
    def find_by_id(cls, userid):
        return cls.query.filter_by(userid == userid).first()

    @classmethod
    def login(cls, user):
        print('=============== 7 ==================')
        sql = cls.query\
            .filter(cls.email.like(user.email))\
            .filter(cls.password.like(user.password))
        df = pd.read_sql(sql.statement, sql.session.bind)
        print(json.loads(df.to_json(orient='records')))
        return json.loads(df.to_json(orient='records'))
            

    @staticmethod
    def save(user):
        db.session.add(user)
        db.session.commit()

    # @staticmethod   
    # def insert_many():
    #     service = UserService()
    #     Session = openSession()
    #     session = Session()
    #     df = service.hook()
    #     print(df.head())
    #     session.bulk_insert_mappings(UserDto, df.to_dict(orient="records"))
    #     session.commit()
    #     session.close()

    @staticmethod
    def modify_user(user):
        db.session.add(user)
        db.session.commit()

    @classmethod
    def delete_user(cls,id):
        data = cls.query.get(id)
        db.session.delete(data)
        db.session.commit()


    # def add_user(self, user_id, qId, user_answer, answered_correctly, prior_question_elapsed_time):
    #     user = UserDto(user_id=user_id, qId=qId, user_answer=user_answer, answered_correctly=answered_correctly, prior_question_elapsed_time=prior_question_elapsed_time)
    #     self.session.add(user)
    #     self.session.commit()

    # def fetch_user(self, userid):
    #     query = self.session.query(UserDto).filter((UserDto.user_id == userid))
    #     return query[0]

    # def fetch_all_users(self):
    #     querys = self.session.query(UserDto).all()
    #     return querys

    def update_user(self, userid, column, value):
        user = self.session.query(UserDto).filter(UserDto.user_id == userid).update({column : value})
        self.session.commit()

    # def delete_user(self, userid):
    #     user = self.session.query(UserDto).filter(UserDto.user_id == userid).first()
    #     self.session.delete(user)
    #     self.session.commit()



if __name__ == "__main__":
    userdao = UserDao()
    # userdao.userdata_to_sql()
    # userdao.add_user('444', 9834, 3, 1, 39000)
    # userdao.delete_user('115')
    # names_loop = [name for name in names]
    # print(names_loop)
    # user_id_loop = [i for i in range(1, 16)]
    # print(user_id_loop)
    # names = [{1:'김지우'},{2: '이민준'},{3: '박서연'},{4: '최강준'},{5: '정서윤'},
    # {6: '김예준'},{7: '서유진'},{8: '노인호'},{9: '김민석'},{10 :'강제니'},{11 :'윤채린'},{12: '정소민'},{13: '박다윤'}, {14:'노세은'} ,{ 15: '장도연'}, {16: '정종목'}]
    # for group in names:
    #     for num, name in group.items():
    #         print(num, name)
    #         userdao.update_user(num, 'confirmPassword', num)

    # emails = [{1:'cuy39887@cuoly.com'},{2: 'loi96853@cuoly.com'},{3: 'kaz03160@eoopy.com'},{4: 'xwp35125@eoopy.com'},{5: 'gtq94800@cuoly.com'},
    # {6: 'kqn00371@bcaoo.com'},{7: 'yvq21331@bcaoo.com'},{8: 'boo04861@eoopy.com'},{9: 'mpv92133@cuoly.com'},{10 :'lcg54832@bcaoo.com'},
    # {11 :'cdp16926@eoopy.com'},{12: 'ppi36606@cuoly.com'},{13: 'ppi36606@cuoly.com'}, {14:'tbi13462@cuoly.com'} ,{ 15: 'zkd71659@eoopy.com'}, {16: 'vcm94832@eoopy.com'}]
    # for group in emails:
    #     for num, email in group.items():
    #         print(num, email)
    #         userdao.update_user(num, 'email', email)
    # userdao.update_user(16, 'email', 'kim')
    # userdao.update_user(user_id_loop, names_loop)
    # a = userdao.fetch_user('666')