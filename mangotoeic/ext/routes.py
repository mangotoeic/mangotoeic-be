# from mangotoeic.item.api import Item, Items
from mangotoeic.user.api import User, Users
from mangotoeic.review.api import Review,Reviews
# from mangotoeic.article.api import Article, Articles
from mangotoeic.home.api import Home
import logging

def initialize_routes(api):
    
    print('===============2=================')
    api.add_resource(Home, '/api')
    # api.add_resource(Item, '/api/item/<string:id>')
    # api.add_resource(Items,'/api/items')
    api.add_resource(User, '/api/user/<string:id>')
    api.add_resource(Users, '/api/users')
    api.add_resource(Review, '/api/review/<string:id>')
    api.add_resource(Reviews, '/api/reviews/')
    # api.add_resource(Article, '/api/article/<string:id>')
    # api.add_resource(Articles, '/api/articles/')

@article.errorhandler(500)
def article_api_error(e):
    logging.exception('An error occured during article request. %s' % str(e))
    return 'An internal error occurred.', 500