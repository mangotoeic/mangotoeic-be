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
from mangotoeic.resource.user import UserDto
from mangotoeic.resource.testresult import TestResultDto
import os
from mangotoeic.resource.legacy import LegacyDto
from mangotoeic.resource.corpus import CorpusDto
from mangotoeic.resource.vocab import VocabDto
from mangotoeic.resource.predictvocab import PredictVocabDto
import random
basedir= os.path.dirname(os.path.abspath(__file__))

class VocabRcdPro:
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

class VocabRcdDto(db.Model):
    
    __tablename__ = 'vocabrcd'
    __table_args__={'mysql_collate':'utf8_general_ci'}

    vocabId: int = db.Column(db.Integer, primary_key=True, index=True)
    vocab: str = db.Column(db.String(50),db.ForeignKey('vocablist.vocab'))
    user_id: int = db.Column(db.Integer,db.ForeignKey('users.user_id'))
    # db.ForeignKey(VocabRcdDto.qId)
    answered_correctly = db.Column(db.Integer,db.ForeignKey('testresult.anwered_correctly'))
    correctAvg : float = db.Column(db.Float)
    user_avg: float = db.Column(db.Float)

    @property
    def json(self):
        return {            
            'user_id' : self.user_id,
            'vocabId' : self.vocabId,
            'vocab': self.vocab,
            'correctAvg': self.correctAvg,
            'user_avg': self.user_avg
        }
    
class VocabRcdVo:
    user_id: int = 0
    vocabId: int = 0
    vocab: str = ''
    correctAvg: float = 0.0
class VocabRcdDao(VocabRcdDto):
    @staticmethod
    def hook(id):

        VocabRcdDao.set_datas_from_user_id(id)
        dtos=VocabRcdDao.get_dtos_from_user_id(id)
        rcds=VocabRcdDao.rcd(dtos)

    @staticmethod
    def set_datas_from_user_id(id):
        testresult_dtos=TestResultDto.query.filter_by(user_id=id).all()
        for item in testresult_dtos:
            answered_correctly=item.answered_correctly
            qId =item.qId
            corpusdto=CorpusDto.query.filter_by(CorId= qId).first()
            corpus=corpusdto.corpus
            df=VocabRcdPro.hook(corpus,id,answered_correctly,qId)
            VocabRcdDao.bulk(df)
        VocabRcdDao.get_average()
        VocabRcdDao.get_average2()
        
    @staticmethod
    def get_average():
        db.session.execute('update vocabrcd as t inner join (select user_id, avg(answered_correctly) as av from vocabrcd group by user_id ) t1 on t.user_id = t1.user_id set t.user_avg= t1.av;')
        db.session.commit()
        db.session.close()
    @staticmethod
    def get_average2():
        db.session.execute('update vocabrcd as t inner join (select user_id,qid, avg(answered_correctly) as av from vocabrcd group by user_id, qId ) t1 on t.user_id = t1.user_id and t.qId= t1.qId  set t.correctAvg= t1.av;')
        db.session.commit()
        db.session.close()
        
    @staticmethod
    def get_dtos_from_user_id(id):
        vocabrcddtos=db.session.query(VocabRcdDto).filter_by(user_id=id).all()
        return vocabrcddtos
    @staticmethod   
    def bulk(df):
        print(df.head())
        db.session.bulk_insert_mappings(VocabRcdDto, df.to_dict(orient="records"))
        db.session.commit()
        db.session.close()
    @staticmethod
    def rcd(dtos,id):
        users=UserDto.query.all()
        # print(users)
        minvalue= 100
        minuser=None
        for user in users:
            rcddtos=VocabDto.query.filter_by(user_id=user.user_id).all()
            # print(rcddtos)
            mylist=[]
            for dto in dtos:
                mylist.append(dto.qId)
            minis=dtos
            for mini in minis:
                mylist.append(mini.qId)
            
            mylist = set(mylist)
            sum =0
            for rcditm in rcddtos:
                if rcditm.qId in mylist:
                    # print("=="*100,rcditm)
                    minidto =VocabRcdDto.query.filter_by(user_id=id,qId=rcditm.qId).first()
                    # print(minidto)
                    value=abs(rcditm.correctAvg-minidto.correctAvg)
                    sum+=value
                elif not rcditm.qId in mylist:
                    sum2=0
                    count=0
                    for rcditm2 in rcddtos:
                        sum2+=rcditm2.correctAvg
                        count+=1
                    avg_of_user_from_rcd= sum2/count
                    minidto =VocabRcdDto.query.filter_by(user_id=id).first()
                    # print(minidto)
                    value=abs(avg_of_user_from_rcd-minidto.user_avg)
                    sum+=value
            corrent_value=sum
            if corrent_value<minvalue:
                minvalue=corrent_value
                minuser=user.user_id
            
        print(minuser)
        print(minvalue)
        q=PredictVocabDto.query.filter_by(user_id=minuser)
        df= pd.read_sql(q.statement,q.session.bind)
        df_sorted_by_values=df.sort_values(by='correctAvg',ascending =False)
        print(df_sorted_by_values)
        p=df_sorted_by_values.iloc[int(len(df)/2)]
        print(p)
        median=p['correctAvg']
        mfdtos=q.all()
        mylist2=[]
        for mfdto in mfdtos:
            # mfdto중 가장 중간 오답률을 찾는다
            difference=median-mfdto.correctAvg
            if abs(difference)>0.25:
                continue
            if difference < 0: #맞출확률이 높다면
                x=random.randint(0,1)
                if x==0: 
                    continue
                if x==1:
                    pass
            mylist2.append(mfdto)
        samplelists= random.sample(mylist2,5)
        mylist3=[]
        print(samplelists)
        for samplelist in samplelists:
            legacydto=LegacyDto.query.filter_by(qId=samplelist.qId).first()
            mylist3.append(legacydto.json)
        print(mylist3)
        # NextMiniSetDao.delete(id)
        for item in mylist3:
            qId= item['qId']
            
            # NextMiniSetDao.add(id,qId)
        return mylist3 , 200


        