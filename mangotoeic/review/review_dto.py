from sqlalchemy import Column, Integer, String, ForeignKey 
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.mysql import DECIMAL, VARCHAR, LONGTEXT
from mangotoeic.ext.db import Base

class Review(Base):
    __tablename__ = "reviews"
    __table_args__ = {'mysql_collate':'utf8_general_ci'}

    id = Column(Integer, primary_key = True, index = True)
    # user_id = Column(Integer, ForeignKey("user.user_id"))
    review =  Column(LONGTEXT)
    star =  Column(Integer)
    label = Column(Integer)

    def __repr__(self):
        return f'Review(id=\'{self.id}\',review=\'{self.review}\',\
            star=\'{self.star}\',label=\'{self.label}\',)'

    @property
    def serialize(self):
        return {
            'id' : self.id,
            'user_id' : self.user_id,
            'review' : self.review,
            'star' : self.star,
            'label' : self.label
        }

class ReviewDto(object):
    id: int
    user_id: int
    review: str
    star: int
    label: int


