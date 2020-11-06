from mangotoeic.ext.db import db
from mangotoeic.resource.user import UserDto
from flask_restful import Resource, reqparse

class MinitestDto(db.Model):
    __tablename__ = "minitest"
    __table_args__ = {'mysql_collate':'utf8_general_ci'}
    id = db.Column(db.Integer, primary_key=True, index=True)
    qId = db.Column(db.Integer, db.ForeignKey('legacies.qId'))
    user_id= db.Column(db.Integer, db.ForeignKey('users.user_id'))
    answer_correctly = db.Column(db.Integer)
        

    @property
    def json(self):
        return {
            'user_id' :self.user_id,
            'qId' : self.qId,
            'answer_correctly' :self.answer_correctly
        }
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
    def post(self):
        pass
class Minitests(Resource):
    pass
