from flask.globals import session
import pandas as pd
from flask import request
from flask_restful import Resource, reqparse
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, func
from sqlalchemy import engine
from sqlalchemy.orm import sessionmaker
from mangotoeic.ext.db import db, openSession, engine
from mangotoeic.ext.db import Base
from mangotoeic.resource.user import UserDto
from mangotoeic.resource.legacy import LegacyDto
import json

# 토익 시험 몇번 봤는지, 목표점수, 시험날짜, 본인의 영어실력 입력
# 데이터 베이스에 반영할 건지?

class TestResultDto(db.Model):
    __tablename__ = 'testresult'
    __table_args__={'mysql_collate':'utf8_general_ci'}

    id = db.Column(db.Integer, primary_key=True, index=True)
    #userid: int = db.Column(db.Integer, db.ForeignKey(UserDto.user_id))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    timestamp = db.Column(db.Float)
    qId = db.Column(db.Integer, db.ForeignKey('legacies.qId'))
    user_answer = db.Column(db.Integer)
    answered_correctly = db.Column(db.Float)
    prior_question_elapsed_time = db.Column(db.Float)
    user_avg = db.Column(db.Float)

    # def __init__(self, id=0, user_id=0, qId=0, user_answer=0, answered_correctly=0.0, prior_question_elapsed_time=0.0, timestamp=0):
    #     self.id = id
    #     self.timestamp = timestamp
    #     self.user_id = user_id
    #     self.qId = qId
    #     self.user_answer = user_answer
    #     self.answered_correctly = answered_correctly
    #     self.prior_question_elapsed_time = prior_question_elapsed_time

    def __repr__(self):
        return f'user_id={self.user_id}, qId={self.qId},\
                user_answer={self.user_answer}, answered_correctly={self.answered_correctly},\
                prior_question_elapsed_time={self.prior_question_elapsed_time}'


    @property
    def json(self):
        return {
            'id' : self.id,
            'timestamp' : self.timestamp,
            'user_id' : self.user_id,
            'qId' : self.qId,
            'user_answer' : self.user_answer,
            'answered_correctly': self.answered_correctly,
            'prior_question_elapsed_time': self.prior_question_elapsed_time,
            'user_avg' : self.user_avg
        }
        
        
    # def save(self):
    #     Session = openSession()
    #     session = Session()
    #     newUser = UserDto(user_id = user['user_id'], 
    #                             email = user['email'], 
    #                             password = user['password'])
    #     session.add(newUser)
    #     session.commit()

    # @classmethod
    # def delete(cls):
    #     Session = openSession()
    #     session = Session()
    #     data = cls.query.get(user_id)
    #     session.delete(data)
    #     session.commit()
    

class TestResultDao(TestResultDto):

    def __init__(self):
        pass

    @staticmethod
    def bulk():
        Session = openSession()
        session = Session()
        df = pd.read_csv('./mangotoeic/resource/data/user_table_prepro4.csv')
        session.bulk_insert_mappings(TestResultDto, df.to_dict(orient="records"))
        session.commit()
        session.close()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filer_by(name == name).all()

    @classmethod
    def find_by_id(cls, userid):
        return cls.query.filter_by(userid == userid).first()

    @staticmethod
    def count():
        Session = openSession()
        session = Session()
        return session.query(func.count(TestResultDto.user_id)).one()

    @staticmethod
    def get_average():
        Session = openSession()
        session = Session()
        session.execute('update testresult as t inner join (select user_id, avg(answered_correctly) as av from testresult group by user_id ) t1 on t.user_id = t1.user_id set t.user_avg= t1.av;')
        session.commit()
        session.close()
            

    @staticmethod
    def save(testresult):
        db.session.add(testresult)
        db.session.commit()

    def update_user(self, userid, column, value):
        Session = openSession()
        session = Session()
        session.query(UserDto).filter(UserDto.user_id == userid).update({column : value})
        session.commit()

    @staticmethod
    def add_testresult(data):
        print(data)
        user_id= data['user_id']
        timestamp = data['timestamp']
        prior_question_elapsed_time = data['prior_question_elapsed_time']
        answered_correctly = data['answered_correctly']
        user_answer = data['user_answer']
        print(user_id)
        for idx ,qid in enumerate(data['qId']):
            some_question=LegacyDto.query.filter_by(qId=qid).first()
            print(some_question)

            x=TestResultDto(user_id=user_id, timestamp=timestamp[idx], \
                prior_question_elapsed_time=prior_question_elapsed_time[idx], \
                    answered_correctly=answered_correctly[idx], user_answer=user_answer[idx],\
                        legacy2=some_question)
            db.session.add(x)    
        db.session.commit()
        db.session.close()

    # @staticmethod
    # def modify_user(user):
    #     Session = openSession()
    #     session = Session()
    #     session.add(user)
    #     session.commit()

    # @classmethod
    # def delete_user(cls,id):
    #     Session = openSession()
    #     session = Session()
    #     data = cls.query.get(user_id)
    #     session.delete(data)
    #     session.commit()


class TestResult(Resource):
    pass


class TestResults(Resource):
    @staticmethod
    def post():
        body = request.get_json()
        print(body)
        # df=pd.DataFrame.from_dict(body)
        TestResultDao.add_testresult(body)
        TestResultDao.get_average()
        data=TestResultDto.query.filter_by(user_id=body['user_id']).first()
        return data.user_avg, 200


    # def post():
    #     args = parser.parse_args()
    #     print(f'User {args["id"]} added ')
    #     params = json.loads(request.get_data(), encoding='utf-8')
    #     if len(params) == 0:

    #         return 'No parameter'

    #     params_str = ''
    #     for key in params.keys():
    #         params_str += 'key: {}, value: {}<br>'.format(key, params[key])
    #     return {'code':0, 'message': 'SUCCESS'}, 200

    @staticmethod
    def get(id: str):
        try:
            user = TestResultDao.find_by_id(id)
            if user:
                return user.json()
        except Exception as e:
            return {'message': 'User not found'}, 404


# class Auth(Resource):
#     def post(self):
#         body = request.get_json()
#         user = UserDto(**body)
#         UserDao.save(user)
#         email = user.email
#         password = user.password

#         return {'email': str(email), 'password': str(password)}, 200 


# class Access(Resource):
#     def __init__(self):
#         print('========== 5 ==========')
#     def post(self):
#         print('========== 6 ==========')
#         args = parser.parse_args()
#         user = UserVo()
#         user.password = args.password
#         user.email = args.email
#         data = UserDao.login(user)
#         return data[0], 200
