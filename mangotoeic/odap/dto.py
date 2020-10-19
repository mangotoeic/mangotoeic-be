from mangotoeic.ext.db import db
#from mango.user.dto import UserDto
from mangotoeic.minitest.dto import MinitestDto

class OdapDto(db.Model):

    __tablename__ = 'odap'
    __table_args__={'mysql_collate':'utf8_general_ci'}

    id: int = db.Column(db.Integer, primary_key=True, index=True)
    #userid: int = db.Column(db.Integer, db.ForeignKey(UserDto.user_id))
    Qid: int = db.Column(db.Integer) # db.ForeignKey(MinitestDto.Qid)
    userid: int = db.Column(db.Integer)

    def __init__(self, userid, Qid):
        self.userid = userid
        self.Qid = Qid
    
    def __repr__(self):
        return f'id={self.id}, Qid={self.Qid}'

    @property
    def json(self):
        return {
            'id' : self.id,
            'userid' : self.userid,
            'Qid' : self.Qid
        }
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()