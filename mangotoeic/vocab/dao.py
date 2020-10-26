from mangotoeic.ext.db import db, openSession
from mangotoeic.vocab.dto import VocabDto
from mangotoeic.vocab.pro import VocabPro
import pandas as pd
import json

class VocabDao(UserDto):

    @classmethod
    def find_all(cls):
        sql = cls.query
        df = pd.read_sql(sql.statement, sql.session.bind)
        return json.loads(df.to_json(orient='records'))
    
    @classmethod
    def find_by_vocab(cls, vocabId):
        return cls.query.filter_by(vocabId == vocabId).all()
    
    @classmethod
    def find_by_id(cls, userid):
        return cls.query.filter_by(userid == userid).first()
    
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