from mangotoeic.ext.db import db
#from mango.user.dto import UserDto
from mangotoeic.minitest.dto import MinitestDto

class VocabDto(db.Model):

    __tablename__ = 'vocab'
    __table_args__={'mysql_collate':'utf8_general_ci'}

    id: int = db.Column(db.Integer, primary_key=True, index=True)
    vocabid: int = db.Column(db.Integer)
    answer: str = db.Column(db.String(50))

    userid: int = db.Column(db.Integer)
    Qid: int = db.Column(db.Integer) # db.ForeignKey(MinitestDto.Qid)

    def __init__(self, userid, vocabid, answer, Qid):
        self.userid = userid
        self.vocabid = vocabid
        self.answer = answer
        self.Qid = Qid

    def __repr__(self):
        return f'id={self.id}, userid={self.userid}, vocabid={self.vocabid}, answer={self.answer}, Qid={self.Qid}'

    @property
    def json(self):
        return {
            'id' : self.id,
            'userid' : self.userid,
            'vocabid' : self.vocabid,
            'answer': self.answer,
            'Qid' : self.Qid
        }
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()