import logging
from flask import Blueprint
from flask_restful import Api
from mangotoeic.user.api import User, Users
from mangotoeic.review.api import Review,Reviews
from mangotoeic.home.api import Home
<<<<<<< HEAD
from mangotoeic.legacy.api import Legacy ,Legacies
from mangotoeic.vocab.api import Vocab, Vocabs
=======
from mangotoeic.resource.legacy import Legacy, Legacies
from mangotoeic.resource.minitest import Minitest
from mangotoeic.resource.newq import NewQ , NewQs
from mangotoeic.resource.recommendation import Recommendation

legacies = Blueprint('legacies', __name__, url_prefix='/api/legacies')
legacy = Blueprint('legacy', __name__, url_prefix='/api/legacy')

api = Api(legacy)
api = Api(legacies)
>>>>>>> deef3117688702ea726f3c2fd26dd7ae41b3ae17

def initialize_routes(api):
    api.add_resource(Home, '/api')
    api.add_resource(User, '/api/user/<string:id>')
    api.add_resource(Users, '/api/users')
    api.add_resource(Review, '/api/review/<string:id>')
    api.add_resource(Reviews, '/api/reviews/')
    api.add_resource(Legacy, '/api/legacy')
    api.add_resource(Legacies, '/api/legacies')
<<<<<<< HEAD
    # api.add_resource(Vocab, '/api/vocab/')
    api.add_resource(Vocabs, '/api/vocabs/')
=======
    
@legacy.errorhandler(500)
def legacy_api_error(e):
    logging.exception('An error occurred during home request. %s' % str(e))
    return 'An internal error occurred.', 500
>>>>>>> deef3117688702ea726f3c2fd26dd7ae41b3ae17
    