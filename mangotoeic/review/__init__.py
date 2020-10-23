import logging
from flask import Blueprint
from flask_restful import Api
from mangotoeic.review.api import Review,Reviews

review = Blueprint('review', __name__, url_prefix='/api/review')
reviews = Blueprint('reviews', __name__, url_prefix='/api/reviews')

print('===============3=================')

api = Api(review)
api = Api(reviews)

print('===============4=================')

# api.add_resource(Review, '/api/review/<review_key>')

@review.errorhandler(500)
def server_error(e):
    logging.exception('An error occured during review request. %s' %str(e))
    return 'An internal error occurred.', 500