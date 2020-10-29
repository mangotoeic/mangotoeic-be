from mangotoeic.ext.db import db ,openSession
from typing import List
from flask_restful import Resource, reqparse
class NewQPro:
    def __init__(self):
        ...

class  NewQDto(db.Model):
    __tablename__ ="newQs"
    __table_args__={'mysql_collate':'utf8_general_ci'}
    qId = db.Column(db.Integer, primary_key = True, index = True)
    question = db.Column(db.VARCHAR(300))
    ansA = db.Column(db.CHAR(10))
    ansB = db.Column(db.CHAR(10))
    ansC = db.Column(db.CHAR(10))
    ansD = db.Column(db.CHAR(10))
    answer = db.Column(db.CHAR(10))

    def __init__(self, qId, question, ansA , ansB, ansC,ansD ,answer):
        self.qId = qId
        self.question = question
        self.ansA  = ansA 
        self.ansB = ansB
        self.ansC  = ansC 
        self.ansD  = ansD 
        self.answer  = answer
    def __repr__(self):
        return f'newQs(id={self.id},ansA={self.ansA},ansB={self.ansB},ansC={self.ansC},ansD={self.ansD},answer={self.answer},question={self.question})'


        
    @property
    def json(self):
        return {
            'qId' : self.qId,
            'question' : self.question,
            'ansA' : self.ansA,
            'ansB' : self.ansB,
            'ansC' : self.ansC,
            'ansD' : self.ansD,
            'answer' : self.answer
        
        }
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class NewQDao(NewQDto):
    
    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id == id).first()

class NewQ(Resource):
    def __init__(self):
        parser = reqparse.RequestParser()  # only allow price changes, no name changes allowed
        parser.add_argument('id', type=int, required=False, help='This field cannot be left blank')
        parser.add_argument('qId', type=int, required=False, help='This field cannot be left blank')
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
if __name__ == '__main__':
    ...
    