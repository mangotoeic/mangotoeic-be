from mangotoeic.ext.db import db
from mangotoeic.user.dto import UserDto


class MinitestDto(db.Model):
    __tablename__ = "minitest"
    __table_args__ = {'mysql_collate':'utf8_general_ci'}

    id: int = db.Column(db.Integer, primary_key=True, index=True)
    answer: str = db.Column(db.String(5))
    Qid: int = db.Column(db.Integer)
  
    # user_id : str = db.Column(db.String(30), db.ForeignKey("UserDto.user_id"))

    def __init__(self,Qid, answer):
        # self.user_id = user_id
        self.Qid = Qid
        self.answer = answer
        
          
          
    def __repr__(self):
        return f'Minitest(id=\'{self.id}\',Qid=\'{self.Qid}\',answer=\'{self.answer}\')'

    @property
    def json(self):
        return {
            'id' : self.id,
            # 'user_id' : self.user_id,
            'Qid' : self.Qid,
            'answer' : self.answer,
        }
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

