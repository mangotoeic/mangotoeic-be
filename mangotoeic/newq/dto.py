from mangotoeic.ext.db import db

class  NewQDto(db.Model):
    __tablename__ ="NewQ"
    __table_args__={'mysql_collate':'utf8_general_ci'}
    id = db.Column(db.Integer, primary_key = True, index = True)

    Qid = db.Column(db.Integer)
    question = db.Column(db.VARCHAR(300))
    AnsA = db.Column(db.CHAR(10))
    AnsB = db.Column(db.CHAR(10))
    AnsC = db.Column(db.CHAR(10))
    AnsD = db.Column(db.CHAR(10))
    Answer = db.Column(db.CHAR(1))

    def __init__(self, Qid, AnsA , AnsB, AnsC,AnsD ):
        self.Qid = Qid
        self.AnsA  = AnsA 
        self.AnsB = AnsB
        self.AnsC  = AnsC 
        self.AnsD  = AnsD 
    def __repr__(self):
        return f'Corpus(id={self.id},AnsA={self.AnsA},AnsB={self.AnsB},AnsC={self.AnsC},AnsD={self.AnsD},Answer={self.Answer})'


        
    @property
    def json(self):
        return {
            'Qid' : self.Qid,
            'question' : self.question,
            'AnsA' : self.AnsA,
            'AnsB' : self.AnsB,
            'AnsC' : self.AnsC,
            'AnsD' : self.AnsD,
            'Answer' : self.Answer,
        
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()