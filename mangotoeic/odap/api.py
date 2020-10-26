import json
from typing import List
from flask import request, jsonify
from flask_restful import Resource, reqparse
from mangotoeic.odap.dto import OdapDto, OdapVo
from mangotoeic.odap.dao import OdapDao

parser = reqparse.RequestParser()  # only allow price changes, no name changes allowed
parser.add_argument('user_id', type=int, required=True,
                                        help='This field should be a userid')
parser.add_argument('qId', type=int, required=True,
                                        help='This field should be a qId')

def Odap(Resrouce):
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
class Auth(Resource):
    def post(self):
        body = request.get_json()
        odap = OdapDao(**body)
        OdapDao.save(odap)
        id = odap.qId

        return {'id': str(id)}, 200 

class Access(Resource):
    def __init__(self):
        print('========== 5 ==========')
    
    def post(self):
        print('========== 6 ==========')
        args = parser.parse_args()
        odap = OdapVo()
        odap.qId = args.qId
        odap.user_id = args.user_id
        print(odap.user_id)
        print(odap.qId)
        data = OdapDao.login(odap)
        return data[0], 200