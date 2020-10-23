from typing import List
from flask import request
from flask_restful import Resource, reqparse
from mangotoeic.review.dao import ReviewDao
from mangotoeic.review.dto import ReviewDto, ReviewVo
import json
from flask import jsonify

parser = reqparse.RequestParser()
parser.add_argument('user_id', type = int, required = True, help = 'This field should be user_id')
parser.add_argument('review', type = str, required = True, help = 'This field should be user_id')

class Review(Resource):
    def __init__(self):
        print('===============55=================')

    @staticmethod
    def post(id):
        args = parser.parse_args()
        print(f'Review {args["id"]} added')
        params = json.loads(request.get_data(), encoding = 'utf-8')
        if len(params) ==0 :
            return 'No parameter'

        params_str = ''
        for key in params.keys():
            params_str += 'key: {}, value {}<br>'.format(key, params[key])
        return {'code':0, 'message': 'SUCCESS'}, 200  
    
    @staticmethod
    def get(id):
        print(f'Review {id} gets called')
        try: 
            review = ReviewDao.find_by_id(id)
            if review:
                return review.json()
        except Exception as e:
            return {'message': 'User not found'}, 404 

    @staticmethod
    def update(id):
        args = parser.parse_args()
        print(f'Review {args["id"]} updated')
        return {'code':0, 'message': 'SUCCESS'}, 200
    
    @staticmethod
    def delete(id):
        args = parser.parse_args()
        print(f'User {args["id"]} deleted')
        return {'code':0, 'message': 'SUCCESS'}, 200 

class Reviews(Resource): 

    def post(self):
        rd = ReviewDao()
        rd.insert_many('reviews')
        
        print('===============6=========================')

    def get(self):
        print('reviews gettttttttttt')
        data = ReviewDao.find_all()
        return data, 200







# class Auth(Resource):

#     def post(self):
#         body = request.get_json()
#         review = ReviewDto(**body)
#         ReviewDao.save(review)
#         id = review.id
#         return {'id': str(id)}, 200

# class Access(Resource):
    
#     def __init__(self):
#         print('===============5=================')

#     def post(self):
        
#         print('===============6=========================')
#         args = parser.parse_args()
#         review = ReviewVo()
#         review.id = args.id
        

