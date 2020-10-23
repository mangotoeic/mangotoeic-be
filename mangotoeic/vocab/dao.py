from mangotoeic.ext.db import db, openSession
from mangotoeic.vocab.dto import VocabDto
from mangotoeic.vocab.pro import VocabPro

class VocabDao():

    @classmethod
    def find_all(cls):
        return cls.query.all
    
    @classmethod
    def add_vocab(cls, userid, vocabId, newv):
        add_vocab = cls.query.filter(userid == userid, vocabId != vocabId).add(newv)
        return add_vocab

    @staticmethod   
    def insert_many():
        service = VocabPro()
        Session = openSession()
        session = Session()
        df = service.hook()
        print(df.head())
        session.bulk_insert_mappings(VocabDto, df.to_dict(orient="records"))
        session.commit()
        session.close()
    
    @classmethod
    def delete_vocab(cls, userid, vocabId):
        del_vocab = cls.query.filter(userid == userid, vocabId == vocabId).delete(vocabId)
        return del_vocab

if __name__ == "__main__":
    dao = VocabDao()
    dao.insert_many()
