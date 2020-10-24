print('==========================legacy api=============================')
from typing import List
from flask import request
from flask_restful import Resource, reqparse
from mangotoeic.legacy.dao import LegacyDao
from mangotoeic.legacy.dto import LegacyDto, LegacyVo
import json

parser = reqparse.RequestParser()  # only allow price changes, no name changes allowed
parser.add_argument('userid', type=str, required=True,
                                        help='This field should be a userid')
parser.add_argument('password', type=str, required=True,
                                        help='This field should be a password')

class Legacy(Resource):
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
    def get(id):
        print(f'User {id} added ')
        try:
            user = LegacyDao.find_by_id(id)
            if user:
                return user.json()
        except Exception as e:
            return {'message': 'User not found'}, 404

    @staticmethod
    def update():
        args = parser.parse_args()
        print(f'User {args["id"]} updated ')
        return {'code':0, 'message': 'SUCCESS'}, 200

    @staticmethod
    def delete():
        args = parser.parse_args()
        print(f'USer {args["id"]} deleted')
        return {'code' : 0, 'message' : 'SUCCESS'}, 200

    

class Legacies(Resource):
    def post(self):
        ud = LegacyDao()
        ud.insert_many('users')

    def get(self):
        print('========== 10 ==========')
        data = LegacyDao.find_all()
        return data, 200