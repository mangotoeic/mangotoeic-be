from typing import List
from flask_restful import Resource, reqparse
from mangotoeic.newq.dao import NewQDao
from mangotoeic.newq.dto import NewQDto

class NewQ(Resource):
    def __init__(self):
        parser = reqparse.RequestParser()  # only allow price changes, no name changes allowed
        parser.add_argument('id', type=int, required=False, help='This field cannot be left blank')
        parser.add_argument('Qid', type=int, required=False, help='This field cannot be left blank')
        parser.add_argument('AnsA', type=str, required=False, help='This field cannot be left blank')
        parser.add_argument('AnsB', type=str, required=False, help='This field cannot be left blank')
        parser.add_argument('AnsC', type=str, required=False, help='This field cannot be left blank')
        parser.add_argument('AnsD', type=str, required=False, help='This field cannot be left blank')
       
        self.dao = NewQDao

    def get(self, name):
        item = self.dao.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    

class NewQs(Resource):
    def get(self):
        ...