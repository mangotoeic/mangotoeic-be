from mangotoeic.resource.vocablist import VocablistDto
from selenium import webdriver
import pandas as pd
import json
from mangotoeic.ext.db import db, openSession
from typing import List
from flask import request, jsonify
from flask_restful import Resource, reqparse
from sqlalchemy import func
from mangotoeic.resource.chrome import sel_searching_data
import os
basedir= os.path.dirname(os.path.abspath(__file__))

class PredictVocabPro:
    def __init__(self):
        self.fpath = os.path.join(basedir,'./data/data.csv')
    
    def hook(self):
        df=self.fileread()
        print(df.head())
        return df

    def fileread(self):
        df = pd.read_csv(self.fpath,index_col=False,)
        df = df.drop('Unnamed: 0', axis=1)
        df = df.rename(index ={0:'vocabId'})
        
        return df

class PredictVocabDto(db.Model):
    
    __tablename__ = 'vocab'
    __table_args__={'mysql_collate':'utf8_general_ci'}

    vocabId: int = db.Column(db.Integer, primary_key=True, index=True)
    vocab: str = db.Column(db.String(50),db.ForeignKey('vocablist.vocab'))
    user_id: int = db.Column(db.Integer)
    # db.ForeignKey(MinitestDto.qId)
    correctAvg : float = db.Column(db.Float)

    def __repr__(self):
        return f' user_id={self.user_id}, vocabId={self.vocabId}, vocab={self.vocab},correctAvg={self.correctAvg}'

    @property
    def json(self):
        return {            
            'user_id' : self.user_id,
            'vocabId' : self.vocabId,
            'vocab': self.vocab,
            'correctAvg': self.correctAvg
        }
    