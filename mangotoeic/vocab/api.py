import json
from typing import List
from flask import request, jsonify
from flask_restful import Resource, reqparse
from mangotoeic.vocab.dto import VocabDto, VocabVo
from mangotoeic.vocab.dao import VocabDao

parser = reqparse.RequestParser()  # only allow price changes, no name changes allowed
parser.add_argument('user_id', type=int, required=True,
                                        help='This field should be a userid')
parser.add_argument('vocabId', type=int, required=True,
                                        help='This field should be a vocabId')
parser.add_argument('vocab', type=str, required=True,
                                        help='This field should be a vocab')
parser.add_argument('correctAvg', type=float, required=True,
                                        help='This field should be a correctAvg')

def Vocab(Resrouce):
    @staticmethod
    def post():
        args = parser.parse_args()
        print(f'Vocab {args["id"]} added')
        params = json.loads(request.get_data(), encoding='utf-8')
        if len(params) == 0:
            return 'No parameter'
        params_str = ''
        for key in params.keys():
            params_str += 'key: {}, value {}<br>'.format(key, params[key])
        return {'code':0, 'message': 'SUCCESS'}, 200
    
    @staticmethod
    def get(id):
        print(f'Vocab {id} added')
        try:
            vocab = VocabDao.find_by_id(id)
            if vocab:
                return vocab.json()
        except Exception as e:
            return {'message': 'Vocabulary not found'}, 404
    
    @staticmethod
    def update():
        args = parser.parse_args()
        print(f'Vocab {args["id"]} updated')
        return {'code':0, 'message':'SUCCESS'}, 200
    
    @staticmethod
    def delete():
        args = parser.parse_args()
        print(f'Vocab {args["id"]} deleted')
        return {'code':0, 'message':'SUCCESS'}, 200

class Auth(Resource):
    def post(self):
        body = request.get_json()
        vocab = VocabDao(**body)
        VocabDao.save(vocab)
        id = vocab.vocabId

        return {'id': str(id)}, 200 

class Access(Resource):
    def __init__(self):
        print('========== 5 ==========')
    
    def post(self):
        print('========== 6 ==========')
        args = parser.parse_args()
        vocab = VocabVo()
        vocab.vocabId = args.vocabId
        vocab.user_id = args.user_id
        print(vocab.user_id)
        print(vocab.vocabId)
        data = VocabDao.login(vocab)
        return data[0], 200