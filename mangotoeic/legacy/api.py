from typing import List
from flask_restful import Resource, reqparse
from mangotoeic.legacy.dao import LegacyDao
from mangotoeic.legacy.dto import LegacyDto

class Legacy(Resource):
    def __init__(self):
        parser = reqparse.RequestParser()  # only allow price changes, no name changes allowed
        parser.add_argument('id', type=int, required=False, help='This field cannot be left blank')
        parser.add_argument('Qid', type=int, required=False, help='This field cannot be left blank')
        parser.add_argument('AnsA', type=str, required=False, help='This field cannot be left blank')
        parser.add_argument('AnsB', type=str, required=False, help='This field cannot be left blank')
        parser.add_argument('AnsC', type=str, required=False, help='This field cannot be left blank')
        parser.add_argument('AnsD', type=str, required=False, help='This field cannot be left blank')
       
        self.dao = LegacyDao

    def get(self, name):
        item = self.dao.find_by_id(id)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    

class Legacyes(Resource):
    def get(self):
        return {'legacys': list(map(lambda legacy: legacy.json(), LegacyDao.find_all()))}