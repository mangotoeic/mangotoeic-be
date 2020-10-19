from flask_restful import Resource, reqparse
from mangotoeic.reviewboard.dao import ReviewDao
from mangotoeic.reviewboard.dto import ReviewDto


class Review(Resource):

    def __init__(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id',type = int, required = False, help = 'This field cannot be left blank')
        parser.add_argument('user_id',type = str, required = False, help = 'This field cannot be left blank')
        parser.add_argument('review',type = str, required = False, help = 'This field cannot be left blank')
        parser.add_argument('star',type = int, required = False, help = 'This field cannot be left blank')
        parser.add_argument('label',type = int, required = False, help = 'This field cannot be left blank')

    def post(self):
        data = self.parser.parse_args()
        review = ReviewDto(data['user_id'], data['review'], data['star'], data['label'])
        try:
            review.save()
        except:
            return {'message' : 'An error occured inserting the review'}, 500
        return review.json(), 201

    def get(self,id):
        review = ReviewDao.find_by_id(id)
        if review:
            return review.json()
        return {'message' : 'Review not found'}, 404

    def put(self,id):
        data = Review.parser.parse_args()
        review = ReviewDao.find_by_id(id)

        review.review = data['review']
        review.star = data['star']
        review.label = data['label']
        review.save()
        return review.json


class Reviews(Resource):
    def get(self):
        return {'reviews': list(map(lambda review: review.json(), ReviewDao.find_all()))}
        # return {'reviews':[review.json() for review in ReviewDao.find_all()]}


