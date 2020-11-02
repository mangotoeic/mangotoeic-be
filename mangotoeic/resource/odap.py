from mangotoeic.ext.db import db, openSession
from mangotoeic.resource.minitest import MinitestDto
import pandas as pd
import json
from typing import List
from flask import request, jsonify
from flask_restful import Resource, reqparse
import os
basedir= os.path.dirname(os.path.abspath(__file__))

class OdapPro:
    def __init__(self):
        self.fpath =''
    
    def hook(self):
        df=self.fileread()
        print(df.head())
        return df

    def fileread(self):
        df= pd.read_csv(self.fpath,index_col=False,)
        df = df.drop('Unnamed: 0', axis=1)
        df = df.rename(index ={0:'vocabId'})
        
        return df

class OdapDto(db.Model):
    
    __tablename__ = 'odap'
    __table_args__={'mysql_collate':'utf8_general_ci'}
    id: int = db.Column(db.Integer, primary_key=True, index=True)
    user_id: int = db.Column(db.Integer)
    qId: int = db.Column(db.Integer) # db.ForeignKey(MinitestDto.qId)

    def __init__(self, user_id, qId):
        self.user_id = user_id
        self.qId = qId
    
    def __repr__(self):
        return f'user_id={self.user_id}, qId={self.qId}'

    @property
    def json(self):
        return {
            'user_id' : self.user_id,
            'qId' : self.qId
        }

class OdapVo:
    user_id: int = 0
    qId = int = 0

class OdapDao(OdapDto):
    
    @classmethod
    def find_all(cls):
        sql = cls.query
        df = pd.read_sql(sql.statement, sql.session.bind)
        return json.loads(df.to_json(orient='records'))
    
    @classmethod
    def add_odap(cls, userid, qId, newq):
        add_odap = cls.query.filter(userid == userid, qId != qId).add(newq)
        return add_odap
    
    @classmethod
    def delete_odap(cls, userid, qId):
        del_odap = cls.query.filter(userid == userid, qId == qId).delete(qId)
        return del_odap
    
    @staticmethod   
    def bulk(data):
        Session = openSession()
        session = Session()
        session.bulk_insert_mappings(OdapDto, data.to_dict(orient="records"))
        session.commit()
        session.close()

parser = reqparse.RequestParser()  # only allow price changes, no name changes allowed
parser.add_argument('user_id', type=int, required=True,
                                        help='This field should be a userid')
parser.add_argument('qId', type=int, required=True,
                                        help='This field should be a qId')

class Odap(Resource):
    @staticmethod    
    def post(self):
        args = parser.parse_args()
        print(f'Wrong question {args["id"]} added')
        params = json.loads(request.get_data(), encoding='utf-8')
        if len(params) == 0:
            return 'No parameter'
        params_str = ''
        for key in params.keys():
            params_str += 'key: {}, value {}<br>'.format(key, params[key])
        return {'code':0, 'message': 'SUCCESS'}, 200
    
    @staticmethod
    def update():
        args = parser.parse_args()
        print(f'Question {args["id"]} updated')
        return {'code':0, 'message':'SUCCESS'}, 200
    
    @staticmethod
    def delete():
        args = parser.parse_args()
        print(f'Question {args["id"]} deleted')
        return {'code':0, 'message':'SUCCESS'}, 200

class Odaps(Resource):
    def get(self):
        data = OdapDao.find_all()
        return data, 200

    def post(self):
        body = request.get_json()
        print(body)
        df=pd.DataFrame.from_dict(body)
        OdapDao.bulk(df)
        user = OdapDto(**body)
        OdapDao.save(user)
        return {'id': "good"}, 200
    
    #{'user_id': None, 'qId': [2, 3, 4]}

        
if __name__ == '__main__':
    prepro = OdapPro()
    prepro.hook()