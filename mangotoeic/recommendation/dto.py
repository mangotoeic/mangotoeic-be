from mangotoeic.ext.db import db
class  RecommendationDto(db.Model):
    __tablename__ ="recommendation"
    __table_args__={'mysql_collate':'utf8_general_ci'}
    qId= db.Column(db.Integer, primary_key = True, index = True)
    question = db.Column(db.VARCHAR(200))
    user_id = db.Column(db.Integer)
    correctAvg = db.Column(db.Float)
    
    def __init__(self, qId, question, user_id,correctAvg):
        self.qId = qId
        self.question  = question 
        self.user_id = user_id
        self.correctAvg = correctAvg

    def __repr__(self):
        return f'recommendation(qId={self.qId},question={self.question},user_id={self.user_id},correctAvg={self.correctAvg})'

    @property
    def json(self):
        return {
            'qId' : self.qId,
            'user_id' : self.user_id,
            'question' : self.question,
            'correctAvg': self.correctAvg
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()