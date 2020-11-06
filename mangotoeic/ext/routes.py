import logging
from flask import Blueprint
from flask_restful import Api
from mangotoeic.resource.user import User, Users, Auth, Access, Profile 
from mangotoeic.resource.preinfo import PreInfo
from mangotoeic.home.api import Home
from mangotoeic.resource.legacy import Legacy, Legacies
from mangotoeic.resource.minitest import Minitest
from mangotoeic.resource.newq import NewQ , NewQs
from mangotoeic.resource.recommendation import Recommendation
from mangotoeic.resource.odap import Odap, Odaps
from mangotoeic.resource.vocab import Vocab, Vocabs
from mangotoeic.resource.testresult import TestResult, TestResults
from mangotoeic.resource.review import Review, Review2, Reviews
from mangotoeic.resource.selectedq import SelectedQs
legacies = Blueprint('legacies', __name__, url_prefix='/api/legacies')
legacy = Blueprint('legacy', __name__, url_prefix='/api/legacy')

odaps = Blueprint('odaps', __name__, url_prefix='/api/odaps')
odap = Blueprint('odap', __name__, url_prefix='/api/odap')

vocabs = Blueprint('vocabs', __name__, url_prefix='/api/vocabs')
vocab = Blueprint('vocab', __name__, url_prefix='/api/vocab/<int:id>')

user = Blueprint('user', __name__, url_prefix='/api/user')
users = Blueprint('users', __name__, url_prefix='/api/users')

profile = Blueprint('profile', __name__, url_prefix='/api/profile/<int:id>')

auth = Blueprint('auth', __name__, url_prefix='/api/auth')
access = Blueprint('access', __name__, url_prefix='/api/access')

testresult = Blueprint('testresult', __name__, url_prefix='/api/testresult/<int:id>')
testresults = Blueprint('testresults', __name__, url_prefix='/api/testresults')

review = Blueprint('review', __name__, url_prefix='/api/review/<string:review>') 
review2 = Blueprint('review2', __name__, url_prefix='/api/review2/')
reviews = Blueprint('reviews', __name__, url_prefix='/api/reviews') 

preinfo = Blueprint('diagnosis', __name__, url_prefix='/api/preinfo')
selectedqs = Blueprint('selectedq', __name__, url_prefix='/api/selectedqs')

api = Api(legacy)
api = Api(legacies)
api = Api(odaps)
api = Api(odap)
api = Api(vocabs)
api = Api(vocab)
api = Api(user)
api = Api(users)
api = Api(access)
api = Api(auth)
api = Api(testresult)
api = Api(testresults)
api = Api(preinfo)
api = Api(review)
api = Api(review2)
api = Api(reviews) 
api = Api(selectedqs)
def initialize_routes(api):
    api.add_resource(Home, '/api')
    api.add_resource(User, '/api/user')
    api.add_resource(Users, '/api/users')
    api.add_resource(Review, '/api/review/<string:review>') 
    api.add_resource(Review2, '/api/review2') 
    api.add_resource(Reviews, '/api/reviews/')
    api.add_resource(Legacy, '/api/legacy')
    api.add_resource(Legacies, '/api/legacies')
    api.add_resource(Odaps, '/api/odaps')
    api.add_resource(Odap, '/api/odap')
    api.add_resource(Vocabs, '/api/vocabs')
    api.add_resource(Vocab, '/api/vocab/<int:id>')
    api.add_resource(Access, '/api/access')
    api.add_resource(Auth, '/api/auth')
    api.add_resource(TestResult, '/api/testresult')
    api.add_resource(TestResults, '/api/testresults')
    api.add_resource(PreInfo, '/api/preinfo')
    api.add_resource(Profile, '/api/profile/<int:id>')
    api.add_resource(SelectedQs, '/api/selectedqs')


    
@legacy.errorhandler(500)
def legacy_api_error(e):
    logging.exception('An error occurred during home request. %s' % str(e))
    return 'An internal error occurred.', 500

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
    
@review.errorhandler(500)
def review_api_error(e):
    logging.exception('An error occured during review request. %s' %str(e))
    return 'An internal error occurred.', 500