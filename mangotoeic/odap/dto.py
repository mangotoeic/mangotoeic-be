from mangotoeic.ext.db import db
#from mango.user.dto import UserDto


class OdapDto(db.Model):

    __tablename__ = 'odap'
    __table_args__={'mysql_collate':'utf8_general_ci'}

    user_id: int = db.Column(db.Integer, primary_key=True, index=True)
    #userid: int = db.Column(db.Integer, db.ForeignKey(UserDto.user_id))
    qId: int = db.Column(db.Integer) # db.ForeignKey(MinitestDto.qId)

    def __init__(self, userid, qId):
        self.user_id = user_id
        self.qId = qId
    
    def __repr__(self):
        return f'user_id={self.user_id}, qId={self.qId}'

    @property
    def json(self):
        return {
            'user_id' : self.user_id,
            'qId' : self.qId
        }

class OdapVo:
    user_id: int = 0
    qId = int = 0