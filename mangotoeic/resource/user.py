import pandas as pd
from flask import request
from flask_restful import Resource, reqparse
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker
from mangotoeic.ext.db import db, openSession
from mangotoeic.ext.db import Base
import json

# 토익 시험 몇번 봤는지, 목표점수, 시험날짜, 본인의 영어실력 입력
# 데이터 베이스에 반영할 건지?

class UserDto(db.Model):
    __tablename__ = 'users'
    __table_args__={'mysql_collate':'utf8_general_ci'}

    user_id = db.Column(db.Integer, primary_key=True, index=False)
    timestamp = db.Column(db.Integer)
    user_name = db.Column(db.String(20))
    password = db.Column(db.String(20))
    qId = db.Column(db.Integer)
    user_answer = db.Column(db.Integer)
    answered_correctly = db.Column(db.Float)
    prior_question_elapsed_time = db.Column(db.Float)
    email = db.Column(db.String(20))

    # password: str = ''
    # email: str = ''
    # user_name : str = ''
    # user_id : int = 0
    # qId : int = 0
    # user_answer : int = 0
    # answered_correctly : float = 0.0
    # prior_question_elapsed_time : float = 0.0
    # email : str = ''
    def __init__(self, user_id=0, user_name='', password='', qId=0, user_answer=0, answered_correctly=0.0, prior_question_elapsed_time=0.0, email='', timestamp=0):
        self.timestamp = timestamp
        self.user_id = user_id
        self.user_name = user_name
        self.password = password
        self.qId = qId
        self.user_answer = user_answer
        self.answered_correctly = answered_correctly
        self.prior_question_elapsed_time = prior_question_elapsed_time
        self.email = email

    def __repr__(self):
        return f'user_id={self.user_id}, user_name={self.user_name} password={self.password}, qId={self.qId},\
                user_answer={self.user_answer}, answered_correctly={self.answered_correctly},\
                prior_question_elapsed_time={self.prior_question_elapsed_time}, email={self.email}'


    @property
    def json(self):
        return {
            'timestamp' : self.timestamp,
            'user_id' : self.user_id,
            'user_name' : self.user_name,
            'password' : self.password,
            'qId' : self.qId,
            'user_answer' : self.user_answer,
            'answered_correctly': self.answered_correctly,
            'prior_question_elapsed_time': self.prior_question_elapsed_time,
            'email': self.email
        }
        
        
    def save(self):
        Session = openSession()
        session = Session()
        newUser = UserDto(user_id = user['user_id'], 
                                email = user['email'], 
                                password = user['password'])
        session.add(newUser)
        session.commit()

    @classmethod
    def delete(cls):
        Session = openSession()
        session = Session()
        data = cls.query.get(user_id)
        session.delete(data)
        session.commit()


class UserVo:
    timestamp: int = 0
    password: str = ''
    email: str = ''
    user_name : str = ''
    user_id : int = 0
    qId : int = 0
    user_answer : int = 0
    answered_correctly : float = 0.0
    prior_question_elapsed_time : float = 0.0
    email : str = ''
    


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

    @staticmethod
    def modify_user(user):
        Session = openSession()
        session = Session()
        session.add(user)
        session.commit()

    @classmethod
    def delete_user(cls,id):
        Session = openSession()
        session = Session()
        data = cls.query.get(user_id)
        session.delete(data)
        session.commit()


parser = reqparse.RequestParser()  # only allow price changes, no name changes allowed
parser.add_argument('name', type=str, required=False, help='This field should be a email')
parser.add_argument('email', type=str, required=True,
                                        help='This field should be a email')
parser.add_argument('password', type=str, required=True,
                                        help='This field should be a password')


class User(Resource):

    @staticmethod
    def post():
        body = request.get_json()
        print("+++=++"*30,body)
        user = UserDto(**body)
        # user.user_name = body['user_name']
        # user.email =body['email']
        # user.password = body['password']
        UserDao.save(user)
        # user_name = user.user_name
        # email = user.email
        # password = user.password
        # return {'hi'}, 200

        # try: 
        #     UserDao.save(args)
        #     return {'code' : 0, 'message' : 'SUCCESS'}, 200    
        # except:
        #     return {'message': 'An error occured inserting the user'}, 500

    @staticmethod
    def get(email):
        print(f'User {email} added ')
        try:
            user = UserDao.find_by_id(id)
            if user:
                return user.json()
        except:
            return {'message': 'User not found'}, 404

    def put(self, id):
        data = User.parser.parse_args()
        user = User.find_by_id(id)

        user.user_id = data['user_id']
        user.email = data['email']
        user.save()
        return user.json()

class Users(Resource):
    @staticmethod
    def post():
        args = parser.parse_args()
        print(f'User {args["id"]} added ')
        params = json.loads(request.get_data(), encoding='utf-8')
        if len(params) == 0:

            return 'No parameter'

        params_str = ''
        for key in params.keys():
            params_str += 'key: {}, value: {}<br>'.format(key, params[key])
        return {'code':0, 'message': 'SUCCESS'}, 200

    @staticmethod
    def get(id: str):
        try:
            user = UserDao.find_by_id(id)
            if user:
                return user.json()
        except Exception as e:
            return {'message': 'User not found'}, 404


class Auth(Resource):
    def post(self):
        body = request.get_json()
        user = UserDto(**body)
        UserDao.save(user)
        email = user.email
        password = user.password

        return {'email': str(email), 'password': str(password)}, 200 


class Access(Resource):
    def __init__(self):
        print('========== 5 ==========')
    def post(self):
        print('========== 6 ==========')
        args = parser.parse_args()
        user = UserVo()
        user.password = args.password
        user.email = args.email
        data = UserDao.login(user)
        return data[0], 200