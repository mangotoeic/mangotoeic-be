from mangotoeic.ext.db import db
class  RecommendationDto(db.Model):
    __tablename__ ="recommendation"
    __table_args__={'mysql_collate':'utf8_general_ci'}
    id = db.Column(db.Integer, primary_key =True, index = True)
    qId= db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    correctAvg = db.Column(db.Float)
    
    def __init__(self,id, qId, user_id,correctAvg):
        self.id = id
        self.qId = qId
        self.user_id = user_id
        self.correctAvg = correctAvg

    def __repr__(self):
        return f'recommendation(id={self.id},qId={self.qId},user_id={self.user_id},correctAvg={self.correctAvg})'

    @property
    def json(self):
        return {
            'qId' : self.qId,
            'user_id' : self.user_id,
            "id":self.id,
            'correctAvg': self.correctAvg
        }

