from typing import List
from flask_restful import Resource, reqparse
from mangotoeic.odap.dto import OdapDto
from mangotoeic.odap.dao import OdapDao

def Odap(Resrouce):
    def __init__(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=False, help='This field cannot be left blank')
        parser.add_argument('user_id', type=int, required=False, help='This field cannot be left blank')
        parser.add_argument('Qid', type=int, required=False, help='This field cannot be left blank')
    
    def post(self):
        data = self.parser.parse_args()
        odap = OdapDto(data['user_id'], data['Qid'])
        try:
            odap.save()
        except:
            return {'message': 'An error occured inserting the question'}, 500
        return odap.json(), 201
    
    def get(self, id):
        odap = OdapDao.find_by_id(id)
        if odap:
            return odap.json()
        return {'message': 'Question not found'}, 404
    
    def put(self, id):
        data = Odap.parser.parse_args()
        odap = OdapDao.find_by_id(id)

        odap.Qid = data['Qid']
        odap.save()
        return odap.json()

class Odaps(Resource):
    def get(self):
        return {'odaps': list(map(lambda odap: odap.json(), OdapDao.find_all()))}