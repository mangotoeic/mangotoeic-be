from typing import List
from flask_restful import Resource, reqparse
from mangotoeic.user.dao import UserDao
from mangotoeic.user.dto import UserDto

class User(Resource):
    def __init__(self):
        parser = reqparse.RequestParser()  # only allow price changes, no name changes allowed
        parser.add_argument('user_id', type=str, required=True, help='This field cannot be left blank')
        # parser.add_argument('user_name', type=str, required=True, help='Must enter the store id')
        # parser.add_argument('password', type=str, required=True, help='Must enter the store id')
        parser.add_argument('Qid', type=int, required=True, help='Must enter the store id')
        parser.add_argument('user_answer', type=int, required=True, help='Must enter the store id')
        parser.add_argument('answered_correctly', type=int, required=True, help='Must enter the store id')
        parser.add_argument('prior_question_elapsed_time', type=int, required=True, help='Must enter the store id')
        self.dao = UserDao

    def get(self, name):
        item = self.dao.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    

class Users(Resource):
    def get(self):
        ...