from mangotoeic.ext.db import db
from mangotoeic.user.dto import UserDto

class ReviewDto(db.Model):
    __tablename__ = "reviews"
    __table_args__ = {'mysql_collate':'utf8_general_ci'}

    id: int = db.Column(db.Integer, primary_key=True, index=True)
    user_id : int = db.Column(db.Integer) 
    # , db.ForeignKey(UserDto.user_id) 
    review: str = db.Column(db.String(500))
    star: int = db.Column(db.Integer) 
  
    
    def __init__(self, user_id, review, star, label):
        self.user_id = user_id
        self.review = review
        self.star = star 
    

    def __repr__(self):
        return f'Review(id=\'{self.id}\',user_id=\'{self.user_id}\',review=\'{self.review}\', star=\'{self.star}\',)'

    @property
    def json(self):
        return {
            'id' : self.id,
            'user_id' : self.user_id,
            'review' : self.review,
            'star' : self.star
        }

class ReviewVo:
    id: int = 1
    user_id : int = 0 
    review: str = ''
    star: int = 0 
    