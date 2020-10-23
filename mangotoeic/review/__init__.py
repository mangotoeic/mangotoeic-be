import logging
from flask import Blueprint
from flask_restful import Api
from mangotoeic.review.api import Review

review = Blueprint('review', __name__, url_prefix='/api/review')
api = Api(review)

api.add_resource(Review, '/api/review/<review_key>')

@review.errorhandler(500)
def server_error(e):
    logging.exception('An error occured during review request. %s' %str(e))
    return 'An internal error occurred.', 500