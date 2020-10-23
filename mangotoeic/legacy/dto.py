from mangotoeic.ext.db import db
from mangotoeic.legacy.pro import LegacyPro
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
class  LegacyDto(db.Model):
    __tablename__ ="legacies"
    __table_args__={'mysql_collate':'utf8_general_ci'}
    qId = db.Column(db.Integer, primary_key = True, index = True)
    question = db.Column(db.VARCHAR(300))
    ansA = db.Column(db.CHAR(10))
    ansB = db.Column(db.CHAR(10))
    ansC = db.Column(db.CHAR(10))
    ansD = db.Column(db.CHAR(10))
    answer = db.Column(db.CHAR(10))

    def __init__(self, qId, question, ansA , ansB, ansC,ansD ,answer):
        self.qId = qId
        self.question = question
        self.ansA  = ansA 
        self.ansB = ansB
        self.ansC  = ansC 
        self.ansD  = ansD 
        self.answer  = answer
        
        
    def __repr__(self):
        return f'legacies(id={self.id},ansA={self.ansA},ansB={self.ansB},ansC={self.ansC},ansD={self.ansD},answer={self.answer},question={self.question},qId ={self.qId})'


        
    @property
    def json(self):
        return {
            'qId' : self.qId,
            'question' : self.question,
            'ansA' : self.ansA,
            'ansB' : self.ansB,
            'ansC' : self.ansC,
            'ansD' : self.ansD,
            'answer' : self.answer
        
        }


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
    service = LegacyPro()
    Session = sessionmaker(bind=engine)
    s = Session()
    df = service.hook()
    print(df.head())

    s.bulk_insert_mappings(LegacyDto, df.to_dict(orient="records"))
    s.commit()
    s.close()