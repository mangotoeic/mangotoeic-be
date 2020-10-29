import logging
from flask import Blueprint
from flask_restful import Api
from mangotoeic.resource.user import User, Users, Auth, Access
from mangotoeic.review.api import Review,Reviews
from mangotoeic.home.api import Home
<<<<<<< HEAD
from mangotoeic.vocab.api import Vocab, Vocabs
=======
>>>>>>> master
from mangotoeic.resource.legacy import Legacy, Legacies
from mangotoeic.resource.minitest import Minitest
from mangotoeic.resource.newq import NewQ , NewQs
from mangotoeic.resource.recommendation import Recommendation
from mangotoeic.resource.odap import Odap, Odaps
from mangotoeic.resource.vocab import Vocab, Vocabs

legacies = Blueprint('legacies', __name__, url_prefix='/api/legacies')
legacy = Blueprint('legacy', __name__, url_prefix='/api/legacy')

odaps = Blueprint('odaps', __name__, url_prefix='/api/odaps')
odap = Blueprint('odap', __name__, url_prefix='/api/odap')

vocabs = Blueprint('vocabs', __name__, url_prefix='/api/vocabs')
vocab = Blueprint('vocab', __name__, url_prefix='/api/vocab')

user = Blueprint('user', __name__, url_prefix='/api/user')
users = Blueprint('users', __name__, url_prefix='/api/users')
auth = Blueprint('auth', __name__, url_prefix='/api/auth')
access = Blueprint('access', __name__, url_prefix='/api/access')

api = Api(legacy)
api = Api(legacies)
<<<<<<< HEAD


user = Blueprint('user', __name__, url_prefix='/api/user')
users = Blueprint('users', __name__, url_prefix='/api/users')
auth = Blueprint('auth', __name__, url_prefix='/api/auth')
access = Blueprint('access', __name__, url_prefix='/api/access')

=======
api = Api(odaps)
api = Api(odap)
api = Api(vocabs)
api = Api(vocab)
>>>>>>> master
api = Api(user)
api = Api(users)
api = Api(access)
api = Api(auth)

def initialize_routes(api):
    api.add_resource(Home, '/api')
    api.add_resource(User, '/api/user')
    api.add_resource(Users, '/api/users')
    # api.add_resource(Review, '/api/review/<string:id>')
    # api.add_resource(Reviews, '/api/reviews/')
    api.add_resource(Legacy, '/api/legacy')
    api.add_resource(Legacies, '/api/legacies')
<<<<<<< HEAD
    # api.add_resource(Vocab, '/api/vocab/')
    # api.add_resource(Vocabs, '/api/vocabs')
    api.add_resource(Access, '/api/access')
    api.add_resource(Auth, '/api/auth')

@user.errorhandler(500)
def user_api_error(e):
    logging.exception('An error occurred during user request. %s' % str(e))
    return 'An internal error occurred.', 500


=======
    api.add_resource(Odaps, '/api/odaps')
    api.add_resource(Odap, '/api/odap')
    api.add_resource(Vocabs, '/api/vocabs')
    api.add_resource(Vocab, '/api/vocab')
    api.add_resource(Access, '/api/access')
    api.add_resource(Auth, '/api/auth')
    
>>>>>>> master
@legacy.errorhandler(500)
def legacy_api_error(e):
    logging.exception('An error occurred during home request. %s' % str(e))
    return 'An internal error occurred.', 500

<<<<<<< HEAD
=======
@odap.errorhandler(500)
def odap_api_error(e):
    logging.exception('An error occurred during home request. %s' % str(e))
    return 'An internal error occurred.', 500

@vocab.errorhandler(500)
def vocab_api_error(e):
    logging.exception('An error occurred during home request. %s' % str(e))
    return 'An internal error occurred.', 500

@user.errorhandler(500)
def user_api_error(e):
    logging.exception('An error occurred during user request. %s' % str(e))
    return 'An internal error occurred.', 500
    
>>>>>>> master
