from mangotoeic.ext.db import db
from mangotoeic.user.dto import UserDto

class ReviewDto(db.Model):
    __tablename__ = "reviews"
    __table_args__ = {'mysql_collate':'utf8_general_ci'}

    id: int = db.Column(db.Integer, primary_key=True, index=True)
    email : str = db.Column(db.String(500)) 
    # , db.ForeignKey(UserDto.email) 
    review: str = db.Column(db.String(500))
    star: int = db.Column(db.Integer) 
  
    
    def __init__(self, id = None, email=None, review=None, star=None):
        self.id = id
        self.email = email
        self.review = review
        self.star = star 
    

    def __repr__(self):
        return f'Review(id=\'{self.id}\',email=\'{self.email}\',review=\'{self.review}\', star=\'{self.star}\',)'

    @property
    def json(self):
        return {
            'id' : self.id,
            'email' : self.email,
            'review' : self.review,
            'star' : self.star
        }

class ReviewVo:
    id: int = 1
    email : str = ''
    review: str = ''
    star: int = 1
    