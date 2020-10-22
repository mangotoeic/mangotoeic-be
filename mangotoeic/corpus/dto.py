from mangotoeic.ext.db import db
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from mangotoeic.corpus.pro import CorpusPro


class  CorpusDto(db.Model):
    __tablename__ ="corpuses"
    __table_args__={'mysql_collate':'utf8_general_ci'}
    corId= db.Column(db.Integer, primary_key = True, index = True)
    corpus = db.Column(db.VARCHAR(200))
    def __init__(self, corId, corpus):
        self.corId = corId
        self.corpus  = corpus 
       

    def __repr__(self):
        return f'corpuses(corId={self.corId},corpus={self.corpus})'

    @property
    def json(self):
        return {
            'corId' : self.corId,
            'corpus' : self.corpus,
            
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
if __name__ == '__main__':
    config = {
    # 'user' : 'mangotoeic',
    # 'password' : 'mangotoeic',
    # 'host': 'mangotoeic.cgaqgqvxtixg.ap-northeast-2.rds.amazonaws.com',
    # 'port' : '3306',
    # 'database' : 'mangotoeic'
    'user' : 'root',
    'password' : 'root',
    'host': 'localhost',
    'port' : '3306',
    'database' : 'mariadb'
    }
    charset = {'utf8':'utf8'}
    url = f"mysql+mysqlconnector://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}?charset=utf8"
    engine = create_engine(url)


    service = CorpusPro()
    Session = sessionmaker(bind=engine)
    s = Session()
    df = service.hook()
    print(df.head())
    s.bulk_insert_mappings(CorpusDto, df.to_dict(orient="records"))
    s.commit()
    s.close()