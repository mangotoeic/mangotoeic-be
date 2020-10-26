from mangotoeic.ext.db import db
#from mango.user.dto import UserDto
from mangotoeic.minitest.dto import MinitestDto

class VocabDto(db.Model):

    __tablename__ = 'vocab'
    __table_args__={'mysql_collate':'utf8_general_ci'}

    vocabId: int = db.Column(db.Integer, primary_key=True, index=True)
    vocab: str = db.Column(db.String(50))
    user_id: int = db.Column(db.Integer)
    # db.ForeignKey(MinitestDto.qId)
    correctAvg : float = db.Column(db.Float)

    def __init__(self, user_id, vocabId, vocab, qId,correctAvg):
        self.user_id = user_id
        self.vocabId = vocabId
        self.vocab = vocab
        self.correctAvg = correctAvg
        
    def __repr__(self):
        return f' user_id={self.user_id}, vocabId={self.vocabId}, vocab={self.vocab},correctAvg={self.correctAvg}'

    @property
    def json(self):
        return {            
            'user_id' : self.user_id,
            'vocabId' : self.vocabId,
            'vocab': self.vocab,
            'correctAvg': self.correctAvg
        }
    
class VocabVo:
    user_id: int = 0
    vocabId: int = 0
    vocab: str = ''
    correctAvg: float = 0.0