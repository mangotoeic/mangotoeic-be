from mangotoeic.ext.db import db, openSession,engine
import pandas as pd
import json
from typing import List
from flask import request, jsonify
from flask_restful import Resource, reqparse
import pickle
from sqlalchemy import func
import os
basedir= os.path.dirname(os.path.abspath(__file__))
Session = openSession()
session = Session()

class VocablistPro:
    def __init__(self):
        self.fpath = os.path.join(basedir, './data/vocabdict.pickle')
        self.fpath2 = os.path.join(basedir, './data/vocabdict2.pickle')
        self.fpath3 = os.path.join(basedir, './data/vocabdict3.pickle')
    
    def hook(self):
        df=self.fileread()
        return df
    
    def fileread(self):
        with open(self.fpath, 'rb') as f:
            data = pickle.load(f)
        with open(self.fpath2, 'rb') as f:
            data2 = pickle.load(f)
        with open(self.fpath3, 'rb') as f:
            data3 = pickle.load(f)
        data.update(data2)
        data.update(data3)
        mylist = (list(data.keys()))
        df=pd.DataFrame(mylist , columns=['vocab'])
        
        return df
    
class VocablistDto(db.Model):
    __tablename__ ='vocablist'
    __table_args__={'mysql_collate':'utf8_general_ci'}
    # id = db.Column(db.Integer,primary_key=True, index=True)
    vocab = db.Column(db.String(50),primary_key=True)
    vocabs = db.relationship("VocabDto", backref='vocablist2',lazy=True)
    vocabs2 = db.relationship("VocabdictDto", backref='vocablist',lazy=True) 

class VocablistVo:
    vocab: str = ''

class VocablistDao(VocablistDto):
    @staticmethod   
    def bulk():
        service = VocablistPro()
        Session = openSession()
        session = Session()
        df = service.hook()
        session.bulk_insert_mappings(VocablistDto, df.to_dict(orient="records"))
        session.commit()
        session.close()
    
    @staticmethod
    def count():
        Session = openSession()
        session = Session()
        return session.query(func.count(VocablistDto.vocab)).one()


if __name__ == "__main__":
    prepro = VocablistDao
    prepro.bulk()
