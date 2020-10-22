from typing import List
from flask_restful import Resource, reqparse
from mangotoeic.legacy.dao import LegacyDao
from mangotoeic.legacy.dto import LegacyDto

class Legacy(Resource):
    def __init__(self):
        parser = reqparse.RequestParser()  # only allow price changes, no name changes allowed
        parser.add_argument('id', type=int, required=False, help='This field cannot be left blank')
        parser.add_argument('aid', type=int, required=False, help='This field cannot be left blank')
        parser.add_argument('ansA', type=str, required=False, help='This field cannot be left blank')
        parser.add_argument('ansB', type=str, required=False, help='This field cannot be left blank')
        parser.add_argument('ansC', type=str, required=False, help='This field cannot be left blank')
        parser.add_argument('ansD', type=str, required=False, help='This field cannot be left blank')
       
        self.dao = LegacyDao

    def get(self, name):
        item = self.dao.find_by_id(id)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    

class Legacyes(Resource):
    def get(self):
        return {'legacies': list(map(lambda legacy: legacy.json(), LegacyDao.find_all()))}