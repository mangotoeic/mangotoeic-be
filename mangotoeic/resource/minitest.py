from mangotoeic.ext.db import db
from mangotoeic.user.dto import UserDto
from flask_restful import Resource, reqparse

class MinitestDto(db.Model):
    __tablename__ = "minitest"
    __table_args__ = {'mysql_collate':'utf8_general_ci'}
    groupNum: int = db.Column(db.Integer, primary_key=True, index=True)
    qId: int = db.Column(db.Integer)

    # user_id : str = db.Column(db.String(30), db.ForeignKey("UserDto.user_id"))

    def __init__(self,qId,groupNum):
        # self.user_id = user_id
        self.qId = qId
        self.groupNum =groupNum
        
          
          
    def __repr__(self):
        return f'minitest(groupNum={self.groupNum},qId={self.qId})'

    @property
    def json(self):
        return {
            # 'user_id' : self.user_id,
            'qId' : self.qId,
            'groupNum' :self.groupNum
        }
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
class MinitestDao(MinitestDto):
    
    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod 
    def find_by_qId(cls,qId):
        return cls.query.filter_by(qId==qId).all()

    @classmethod
    def find_by_id(cls,id):
        return cls.query.filter_by(id==id).first()
        
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
