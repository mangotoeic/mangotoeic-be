from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, ForeignKey

db = SQLAlchemy()
Base = declarative_base()

config = {
    'user' : 'mangotoeic',
    'password' : 'mangotoeic',
    'host': 'mangotoeic.cp4t8fiwvw7w.ap-northeast-2.rds.amazonaws.com',
    'port' : '3306',
    'database' : 'mangotoeic'
}
charset = {'utf8':'utf8'}
url = f"mysql+mysqlconnector://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}?charset=utf8"
def openSession():
    ...