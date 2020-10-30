# from mangotoeic.item.api import Item, Items
from mangotoeic.user.api import User, Users
from mangotoeic.review.api import Review,Reviews
# from mangotoeic.article.api import Article, Articles
from mangotoeic.home.api import Home
import logging
from flask import Blueprint
from flask_restful import Api

review = Blueprint('review', __name__, url_prefix='/api/review')
reviews = Blueprint('reviews', __name__, url_prefix='/api/reviews')
# board_page = Blueprint('board_page', __name__, url_prefix = '/board-page')

api = Api(review)
api = Api(reviews)
# api = Api(board_page)

def initialize_routes(api):
    
    print('===============2=================')
    api.add_resource(Home, '/api')
    # api.add_resource(Item, '/api/item/<string:id>')
    # api.add_resource(Items,'/api/items')
    api.add_resource(User, '/api/user/<string:id>')
    api.add_resource(Users, '/api/users')
    api.add_resource(Review, '/api/review/<string:id>')
    api.add_resource(Reviews, '/api/reviews/')
    # api.add_resource(Review, '/board-page/')

    # api.add_resource(Article, '/api/article/<string:id>')
    # api.add_resource(Articles, '/api/articles/')

@review.errorhandler(500)
def review_api_error(e):
    logging.exception('An error occured during review request. %s' %str(e))
    return 'An internal error occurred.', 500