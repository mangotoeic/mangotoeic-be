
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



        
mt = MinitestDao() 
mt.to_sql()
