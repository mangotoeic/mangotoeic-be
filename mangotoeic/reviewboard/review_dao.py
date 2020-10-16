from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from mangotoeic.review import Review
from mangotoeic.ext.db import Base

class ReviewDao():
    def __init__(self):
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.engine = create_engine('mysql+mysqlconnector://root:root@127.0.0.1/mariadb?charset=utf8', encoding='utf8', echo=True)

    def create_table(self):
        Base.metadata.create_all(self.engine)
    
    def add_review(self):
        session.add(Review(review='넘나 좋은 앱!', star=5, label=1))

    def fetch_review_by_star(self, param : int):
        query = session.query(Review).filter((Review.star == param)).all()
        return query

    def fetch_review_by_user_id(self, param : int):
        query = session.query(Review).filter((Review.user_id == param)).first()
        return query

    def fetch_all_reviews(self):
        return session.query(Review).all()
     
    def delete_review_by_user_id(self, param : int):
        result = session.query(Review).filter(Review.user_id == param).first()
        session.delete(result)
        session.commit()