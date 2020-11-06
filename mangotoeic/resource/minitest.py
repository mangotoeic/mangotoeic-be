from mangotoeic.ext.db import db,openSession
from mangotoeic.resource.user import UserDto
from flask_restful import Resource, reqparse
import pandas as pd
from flask import request
from mangotoeic.resource.recommendation import RecommendationDao, RecommendationDto
from mangotoeic.resource.predictMF import PredictMFDto 
from mangotoeic.resource.legacy import LegacyDto
import random
class MinitestDto(db.Model):
    __tablename__ = "minitest"
    __table_args__ = {'mysql_collate':'utf8_general_ci'}
    id = db.Column(db.Integer, primary_key=True, index=True)
    qId = db.Column(db.Integer, db.ForeignKey('legacies.qId'))
    user_id= db.Column(db.Integer, db.ForeignKey('users.user_id'))
    answer_correctly = db.Column(db.Integer)
    user_avg = db.Column(db.Float)

    @property
    def json(self):
        return {
            'user_id' :self.user_id,
            'qId' : self.qId,
            'answer_correctly' :self.answer_correctly,
            "user_avg":self.user_avg
        }
class MinitestDao(MinitestDto):
    
    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod 
    def find_by_qId(cls,qId):
        return cls.query.filter_by(qId==qId).all()

    @classmethod
    def find_by_id(cls,id):
        return cls.query.filter_by(id==id).first()
    @staticmethod
    def bulk(body):
        Session = openSession()
        session = Session()
        df=pd.DataFrame.from_dict(body)
        session.bulk_insert_mappings(MinitestDto, df.to_dict(orient="records"))
        session.commit()
        session.close()
    @staticmethod
    def get_average():
        Session = openSession()
        session = Session()
        session.execute('update minitest as t inner join (select user_id, avg(answer_correctly) as av from minitest group by user_id ) t1 on t.user_id = t1.user_id set t.user_avg= t1.av;')
        session.commit()
        session.close()

    
class Minitest(Resource):
    def post(self):
        pass

class Minitests(Resource):
    @staticmethod
    def post():
        body =request.get_json()
        # print(body)
        MinitestDao.bulk(body)
        MinitestDao.get_average()
        # df=RecommendationDao.pivot_table_build()
        users=UserDto.query.all()
        # print(users)
        maxvalue=0
        maxuser=None
        for user in users:
            rcddtos=RecommendationDto.query.filter_by(user_id=user.user_id).all()
            mylist=body['qId']
            sum =0
            for rcditm in rcddtos:
                if rcditm.qId in mylist:
                    print("=="*100,rcditm)
                    minidto =MinitestDto.query.filter_by(user_id=body["user_id"],qId=rcditm.qId).first()
                    print(minidto)
                    value=abs(rcditm.correctAvg-minidto.user_avg)
                    sum+=value
                elif not rcditm.qId in mylist:
                    sum2=0
                    count=0
                    for rcditm2 in rcddtos:
                        sum2+=rcditm2.correctAvg
                        count+=1
                    avg_of_user_from_rcd= sum/count
                    minidto =MinitestDto.query.filter_by(user_id=user.user_id,qId=rcditm.qId).first()
                    value=abs(avg_of_user_from_rcd-minidto.user_avg)
                    sum+=value
            corrent_value=sum
            if corrent_value>maxvalue:
                maxvalue=corrent_value
                maxuser=user.user_id
            
        print(maxuser)
        print(maxvalue)
        q=PredictMFDto.query.filter_by(user_id=maxuser)
        df= pd.read_sql(q.statement,q.session.bind)
        # print(df)
        df_sorted_by_values=df.sort_values(by='correctAvg',ascending =False)
        p=df_sorted_by_values[len(df)/2]
        # print(p)
        median=p['correctAvg']
        mfdtos=q.all()
        mylist2=[]
        for mfdto in mfdtos:
            # mfdto중 가장 중간 오답률을 찾는다
            difference=median-mfdto.correctAvg
            if abs(difference)>0.5:
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
        for samplelist in samplelists:
            legacydto=LegacyDto.query.filter_by(qId=samplelist.qId).first()
            mylist3.append(legacydto.json)
        
        return mylist3 , 200


    
        

            
        
               
         



                
                
                    








            

        
        

