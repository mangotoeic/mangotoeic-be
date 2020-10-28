from mangotoeic.ext.db import db
from mangotoeic.user.user import UserDto

class ReviewDto(db.Model):
    __tablename__ = "reviews"
    __table_args__ = {'mysql_collate':'utf8_general_ci'}

    id: int = db.Column(db.Integer, primary_key=True, index=True)
    user_id : str = db.Column(db.VARCHAR(10))
    review: str = db.Column(db.String(500))
    star: int = db.Column(db.Integer)
    label: int = db.Column(db.Integer)
  
    
    def __init__(self, user_id, review, star, label):
        self.user_id = user_id
        self.review = review
        self.star = star
        self.label = label
    

    def __repr__(self):
        return f'Review(id=\'{self.id}\',user_id=\'{self.user_id}\',review=\'{self.review}\', star=\'{self.star}\',label=\'{self.label}\',)'

    @property
    def json(self):
        return {
            'id' : self.id,
            'user_id' : self.user_id,
            'review' : self.review,
            'star' : self.star,
            'label' : self.label
        }
    
    # def save(self):
    #     db.session.add(self)
    #     db.session.commit()

    # def delete(self):
    #     db.session.delete(self)
    #     db.session.commit()
    
     