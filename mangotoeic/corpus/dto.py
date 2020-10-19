from mangotoeic.ext.db import db
class  CorpusDto(db.Model):
    __tablename__ ="Corpus"
    __table_args__={'mysql_collate':'utf8_general_ci'}
    id = db.Column(db.Integer, primary_key = True, index = True)
    CorId= db.Column(db.Integer)
    corpus = db.Column(db.VARCHAR(200))
    def __init__(self, CorId, Corpus):
        self.CorId = CorId
        self.corpus  = corpus 
       

    def __repr__(self):
        return f'Corpus(id={self.id},CorId={self.CorId},corpus={self.corpus})'

    @property
    def json(self):
        return {
            'id' : self.id,
            'CorId' : self.corpus_Id,
            'corpus' : self.corpus,
            
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()