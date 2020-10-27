from mangotoeic.ext.db import db ,openSession
from mangotoeic.recommendation.pro import  RecommendationPro
from mangotoeic.recommendation.dto import RecommendationDto
class RecommendationDao():
    
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
if __name__ == '__main__':
    dao = RecommendationDao()
    dao.insert_many()
    