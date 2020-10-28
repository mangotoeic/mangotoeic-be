import logging
from flask import Blueprint
from flask_restful import Api
from mangotoeic.user.user import User, Users, Auth, Access
from mangotoeic.review.api import Review,Reviews
from mangotoeic.home.api import Home
from mangotoeic.legacy.api import Legacy ,Legacies
from mangotoeic.vocab.api import Vocab, Vocabs


user = Blueprint('user', __name__, url_prefix='/api/user')
users = Blueprint('users', __name__, url_prefix='/api/users')
auth = Blueprint('auth', __name__, url_prefix='/api/auth')
access = Blueprint('access', __name__, url_prefix='/api/access')

api = Api(user)
api = Api(users)
api = Api(access)
api = Api(auth)

def initialize_routes(api):
    print('===============initialize===================')
    api.add_resource(Home, '/api')
    api.add_resource(User, '/api/user')
    api.add_resource(Users, '/api/users')
    # api.add_resource(Review, '/api/review/<string:id>')
    # api.add_resource(Reviews, '/api/reviews/')
    api.add_resource(Legacy, '/api/legacy')
    api.add_resource(Legacies, '/api/legacies')
    # api.add_resource(Vocab, '/api/vocab/')
    # api.add_resource(Vocabs, '/api/vocabs')
    api.add_resource(Access, '/api/access')
    api.add_resource(Auth, '/api/auth')

@user.errorhandler(500)
def user_api_error(e):
    logging.exception('An error occurred during user request. %s' % str(e))
    return 'An internal error occurred.', 500