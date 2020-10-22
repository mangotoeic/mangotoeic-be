from mangotoeic.ext.db import db

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
        