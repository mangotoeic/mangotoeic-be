import pandas as pd
import json
from mangotoeic.ext.db import db, openSession
from flask_restful import Resource, reqparse
import pickle
import os
basedir= os.path.dirname(os.path.abspath(__file__))

class VocabdictPro:
    def __init__(self):
        self.fpath = os.path.join(basedir, './data/vocabdict.pickle')
        self.fpath2 = os.path.join(basedir, './data/vocabdict2.pickle')
        self.fpath3 = os.path.join(basedir, './data/vocabdict3.pickle')
    
    def hook(self):
        df=self.fileread()
        print(df.head())
        return df
    
    def fileread(self):
        with open(self.fpath, 'rb') as f:
            data = pickle.load(f)
        with open(self.fpath2, 'rb') as f:
            data2 = pickle.load(f)
        with open(self.fpath3, 'rb') as f:
            data3 = pickle.load(f)
        df = pd.DataFrame.from_dict(data, orient='index')
        df2 = pd.DataFrame.from_dict(data2, orient='index')
        df3 = pd.DataFrame.from_dict(data3, orient='index')
        df = df.append(df2)
        df = df.append(df3)
        # print(df)
        df.to_csv(os.path.join(basedir, './data/dfcsv.csv'))

        return df

class VocabdictDto(db.Model):
    
    __tablename__ = 'vocabdict'
    __table_args__={'mysql_collate':'utf8_general_ci'}

    vocab = db.Column(db.String(50), primary_key=True)
    meaning = db.Column(db.JSON)
    vocabs = db.relationship("VocabDto", backref='vocabdict',lazy=True)

    def __init__(self, vocab, meaning):
        self.vocab = vocab
        self.meaning = meaning
    
    def __repr__(self):
        return f' vocab={self.vocab}, meaning={self.meaning}'
    
    @property
    def json(self):
        return {            
            'vocab': self.vocab,
            'meaning': self.meaning
        }

class VocabdictVo:
    vocab: str = ''
    meaning: str = ''

class VocabdictDao(VocabdictDto):
    @staticmethod   
    def bulk():
        service = VocabdictPro()
        Session = openSession()
        session = Session()
        df = service.hook()
        print(df.head())
        session.bulk_insert_mappings(VocabdictDto, df.to_dict(orient="records"))
        session.commit()
        session.close()

parser = reqparse.RequestParser()
parser.add_argument('vocab', type=str, required=True,
                                        help='This field should be a userid')
parser.add_argument('meaning', type=str, required=True,
                                        help='This field should be a vocabId')

class Vocabdict(Resource):
    def get(id):
        pass

if __name__ == "__main__":
    prepro = VocabdictDao
    prepro.bulk()