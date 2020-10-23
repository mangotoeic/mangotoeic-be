from mangotoeic.ext.db import db , openSession
from mangotoeic.legacy.dto import LegacyDto
from mangotoeic.legacy.pro import LegacyPro
class LegacyDao():
    
    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id == id).first()
    @staticmethod   
    def insert_many():
        service = LegacyPro()
        Session = openSession()
        session = Session()
        df = service.hook()
        print(df.head())
        session.bulk_insert_mappings(LegacyDto, df.to_dict(orient="records"))
        session.commit()
        session.close()
    @staticmethod
    def save(legacy):
        db.session.add(legacy)
        db.session.commit()
    @classmethod
    def delete(cls,id):
        data = cls.query.get(id)
        db.session.delete(data)
        db.session.commit()