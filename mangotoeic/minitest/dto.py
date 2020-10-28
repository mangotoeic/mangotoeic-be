from mangotoeic.ext.db import db
from mangotoeic.user.user import UserDto


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

