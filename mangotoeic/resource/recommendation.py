import pandas as pd
from mangotoeic.ext.db import db ,openSession
from typing import List
from flask_restful import Resource, reqparse
class RecommendationPro:
    def __init__(self):
        ...
    def read_csv(self):
        df=pd.read_csv("./data/realdata.csv")
        return df
    def hook(self):
        df=self.read_csv()
        df=self.prepro(df)
        return df
    def prepro(self,df):
        
        print(df)
        
        df= df.rename(index={0:'id'},columns={'answered_correctly': "correctAvg"})
        print(df)
        return df

class  RecommendationDto(db.Model):
    __tablename__ ="recommendation"
    __table_args__={'mysql_collate':'utf8_general_ci'}
    id = db.Column(db.Integer, primary_key =True, index = True)
    qId: int = db.Column(db.Integer, db.ForeignKey('legacies.qId'))
    user_id = db.Column(db.Integer)
    correctAvg = db.Column(db.Float)
    
    def __init__(self,id, qId, user_id,correctAvg):
        self.id = id
        self.qId = qId
        self.user_id = user_id
        self.correctAvg = correctAvg

    def __repr__(self):
        return f'recommendation(id={self.id},qId={self.qId},user_id={self.user_id},correctAvg={self.correctAvg})'

    @property
    def json(self):
        return {
            'qId' : self.qId,
            'user_id' : self.user_id,
            "id":self.id,
            'correctAvg': self.correctAvg
        }

class RecommendationDao(RecommendationDto):
    
    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id == id).first()
    @staticmethod   
    def insert_many():
        service = RecommendationPro()
        Session = openSession()
        session = Session()
        df = service.hook()
        print(df.head())
        session.bulk_insert_mappings(RecommendationDto, df.to_dict(orient="records"))
        session.commit()
        session.close()
    @staticmethod
    def save(corpus):
        db.session.add(corpus)
        db.session.commit()
    @classmethod
    def delete(cls,id):
        data = cls.query.get(id)
        db.session.delete(data)
        db.session.commit()

class Recommendation(Resource):
    def __init__(self):
        parser = reqparse.RequestParser()  # only allow price changes, no name changes allowed
        self.dao = RecommendationDao

    def get(self, id):
        item = self.dao.find_by_id(id)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

class Recommendations(Resource):
    def get(self):
        ...