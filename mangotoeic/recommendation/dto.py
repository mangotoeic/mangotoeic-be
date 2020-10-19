from mangotoeic.ext.db import db
class  RecommendationDto(db.Model):
    __tablename__ ="recommendation"
    __table_args__={'mysql_collate':'utf8_general_ci'}
    id = db.Column(db.Integer, primary_key = True, index = True)
    Qid= db.Column(db.Integer)
    question = db.Column(db.VARCHAR(200))
    userid = db.Column(db.Integer)
    def __init__(self, Qid, question):
        self.Qid = Qid
        self.question  = question 
        self.userid = userid

    def __repr__(self):
        return f'recommendation(id={self.id},Qid={self.Qid},question={self.question},userid={self.userid})'

    @property
    def json(self):
        return {
            'id' : self.id,
            'Qid' : self.Qid,
            'userid' : self.userid,
            'question' : self.question
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()