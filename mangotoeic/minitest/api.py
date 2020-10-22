from flask_restful import Resource, reqparse
from mangotoeic.minitest.dao import MinitestDao
from mangotoeic.minitest.dto import MinitestDto



class Minitest(Resource):

    def __init__(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id',type = int, required = False, help = 'This field cannot be left blank')
        parser.add_argument('user_id',type = str, required = False, help = 'This field cannot be left blank')
        parser.add_argument('qId',type = int, required = False, help = 'This field cannot be left blank') 
        parser.add_argument('answer',type = str, required = False, help = 'This field cannot be left blank')

    def post(self):
        data = self.parser.parse_args()
        minitest = MinitestDto(data['qId'], data['answer'])
        try:
            minitest.save()
        except:
            return {'message' : 'An error occured inserting the minitest'}, 500
        return minitest.json(), 201

    def get(self,id):
        minitest = MinitestDao.find_by_id(id)
        if minitest:
            return minitest.json()
        return {'message' : 'Minitest not found'}, 404

    def put(self,id):
        data = Minitest.parser.parse_args()
        minitest = MinitestDao.find_by_id(id)

        minitest.qId = data['qId']
        minitest.answer = data['answer']
        minitest.save()
        return minitest.json


class Minitests(Resource):
    def get(self):
        return {'minitests': list(map(lambda minitest: minitest.json(), MinitestDao.find_all()))}
        # return {'minitests':[minitest.json() for minitest in MinitestDao.find_all()]}


