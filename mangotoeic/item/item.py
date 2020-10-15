from sqlalchemy import Column, Integer, String, ForeignKey
from mangotoeic.ext.db import Base

class Item(Base):
    __tablename__ = 'items'

    id = Column(String(120), primary_key=True, index=True)
    name = Column(String)
    price = Column(Integer)


    def __init__(self):
        pass