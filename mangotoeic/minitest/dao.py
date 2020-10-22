
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
basedir = os.path.dirname(os.path.abspath(__file__))
from mangotoeic.utils.file_helper import FileReader
import pandas as pd 

from mangotoeic.ext.db import Base,db
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker  
 
from mangotoeic.minitest.dto import MinitestDto

class MinitestDao():
    
    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod 
    def find_by_qId(cls,qId):
        return cls.query.filter_by(qId==qId).all()

    @classmethod
    def find_by_id(cls,id):
        return cls.query.filter_by(id==id).first()

    # @classmethod
    # def find_by_user_id(cls,user_id):
    #     return cls.query.filter_by(user_id==user_id).first()


    def to_sql(self):
        engine = create_engine('mysql+mysqlconnector://root:root@127.0.0.1/mariadb?charset=utf8', encoding='utf8', echo=True)
        Base.metadata.create_all(engine)   # 처음 테일블만들때 제외하고는 주석처리
        Session = sessionmaker(bind=engine)
        session = Session()
        session.add(MinitestDto(qId = 1, answer='AA'))
        session.add(MinitestDto(qId = 2, answer='B'))
        session.add(MinitestDto(qId = 3, answer='C'))
        session.add(MinitestDto(qId = 5, answer='F'))
        session.commit()
        
mt = MinitestDao() 
mt.to_sql()
