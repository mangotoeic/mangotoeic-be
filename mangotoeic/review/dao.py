from mangotoeic.ext.db import db, openSession
from mangotoeic.review.tokenizer import Prepro
from mangotoeic.review.dto import ReviewDto 
from mangotoeic.user.dto import UserDto
 



class ReviewDao():
    
    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod 
    def find_by_user_id(cls,user_id):
        return cls.query.filter_by(user_id==user_id).all()

    @classmethod
    def find_by_id(cls,id):
        return cls.query.filter_by(id==id).first()

    @classmethod
    def find_by_star(cls,star):
        return cls.query.filter_by(star==star).first()

    @classmethod
    def find_by_label(cls,label):
        return cls.query.filter_by(label==label).first()
    
    @staticmethod
    def save(review):
        db.session.add(review)
        db.session.commit()
         
    @staticmethod
    def insert_many():
        service = Prepro()
        Session = openSession()
        session = Session()
        df = service.get_data()
        print(df.head())
        session.bulk_insert_mappings(ReviewDto, df.to_dict(orient = 'records'))
        session.commit()
        session.close()
        print('done')

    @classmethod
    def delete_review(cls,id):
        data = cls.query.get(id)
        db.session.delete(data)
        db.session.commit()

rd = ReviewDao()
rd.insert_many()

     
    # @classmethod
    # def add_review(cls, user_id,review, star, label):
    #     add_review = cls.query.filter(user_id == user_id, review == review, star==star, label==label).add(review,star,label)
    #     return add_review

    # def to_sql(self):
        
    #     engine = create_engine('mysql+mysqlconnector://root:root@127.0.0.1/mariadb?charset=utf8', encoding='utf8', echo=True)
    #     Base.metadata.create_all(engine)   # 처음 테일블만들때 제외하고는 주석처리
    #     Session = sessionmaker(bind=engine)
    #     session = Session()
    #     session.add(ReviewDto(review = '123review', star=5, label=1))
    #     session.add(ReviewDto(review = '123review', star=5, label=1))
    #     session.add(ReviewDto(review = '123review', star=5, label=1))
    #     session.add(ReviewDto(review = '123review', star=5, label=1))
    #     session.add(ReviewDto(review = '123review', star=5, label=1))
    #     session.commit()
        # reader = FileReader()
        # reader.context = os.path.join(basedir,'data')
        # reader.fname = "앱리뷰csv파일.csv"
        # reader.new_file()
        # df = reader.csv_to_dframe()
        # add_me = df.head(n)
        # for index,row in add_me.iterrows():
        #     session.add(ReviewDto(user_id = user_id, review=row['review'], star=row['star'], label=row['label']))

        # query = session.query(ReviewDto).filter((ReviewDto.star == '5'))
        # print(query)
        # for i in query:
        #     print(i)
            
        # session.commit()

# if __name__ == "__main__":
#     reviewdao = ReviewDao()
#     reviewdao.to_sql()