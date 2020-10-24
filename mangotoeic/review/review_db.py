import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
basedir = os.path.dirname(os.path.abspath(__file__))
from mangotoeic.utils.file_helper import FileReader
import pandas as pd 

from mangotoeic.ext.db import Base
from sqlalchemy import Column, Integer, String, ForeignKey,create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.mysql import DECIMAL, VARCHAR, LONGTEXT

class Review(Base):
    __tablename__ = "reviews"
    __table_args__ = {'mysql_collate':'utf8_general_ci'}
    
    id = Column(Integer, primary_key = True, index = True)
    # user = Column(Integer, ForeignKey("user.id"))
    review =  Column(LONGTEXT)
    star =  Column(Integer)
    label = Column(Integer)

    def __repr__(self):
        return f'Review(id=\'{self.id}\',review=\'{self.review}\',\
            star=\'{self.star}\',label=\'{self.label}\',)'



# 캐글 데이터 userid 문제번호 ...
# 플레이스토 크롤링csv :   리뷰, 별점, 긍/부정 

    def to_sql(self):
        
        engine = create_engine('mysql+mysqlconnector://root:root@127.0.0.1/mariadb?charset=utf8', encoding='utf8', echo=True)
        # Base.metadata.create_all(engine)   # 처음 테일블만들때 제외하고는 주석처리
        
        Session = sessionmaker(bind=engine)
        session = Session()
        reader = FileReader()
        reader.context = os.path.join(basedir,'data')
        reader.fname = "앱리뷰csv파일.csv"
        reader.new_file()
        df = reader.csv_to_dframe()
        add_me = df.head(2500)
        for index,row in add_me.iterrows():
            session.add(Review(review=row['review'], star=row['star'], label=row['label']))

        query = session.query(Review).filter((Review.star == '5'))
        print(query)
        for i in query:
            print(i)
            
        session.commit()
if __name__ == '__main__':

    
    review = Review()
    review.to_sql()