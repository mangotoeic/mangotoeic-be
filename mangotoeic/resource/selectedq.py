import pandas as pd
from mangotoeic.ext.db import db , openSession
import pandas as pd
from typing import List
from flask import request
from flask_restful import Resource, reqparse
import json
from sqlalchemy import func
import os
basedir = os.path.dirname(os.path.abspath(__file__))
class SelectedQPro:
    def __init__(self):
        self.fpath = os.path.join(basedir,'data/selecteQID.csv') 
    def hook(self):
        df=self.fileread()
        df=self.filerename(df)
        return df

    def fileread(self):
        df= pd.read_csv(self.fpath)
        return df
    def filerename(self,df):
        print(df)
        df=df.set_index(['selected_qid'])
        df["percent_to_selected"]=0
        df=df.drop(columns=["Unnamed: 0"],axis=1)
        df=df.reset_index()
        df.index.names=['id']
        print(df)
        return df
        
class  SelectedQDto(db.Model):
    __tablename__ ="selectedq"
    __table_args__={'mysql_collate':'utf8_general_ci'}
    id =db.Column(db.Integer, primary_key = True, index = True)
    selected_qid = db.Column(db.Integer, db.ForeignKey('legacies.qId'))
    percent_to_selected =db.Column(db.Integer)

class SelectedQDao(SelectedQDto):
    @staticmethod
    def bulk():
        service = SelectedQPro()
        Session = openSession()
        session = Session()
        df = service.hook()
        print(df.head())
        session.bulk_insert_mappings(SelectedQDto, df.to_dict(orient="records"))
        session.commit()
        session.close()
    @staticmethod
    def count():
        Session = openSession()
        session = Session()
        return session.query(func.count(SelectedQDto.selected_qid)).one()

if __name__ == "__main__":
    pro = SelectedQDao()
    pro.bulk()