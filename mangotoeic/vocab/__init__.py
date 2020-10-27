import logging
from flask import Blueprint
from flask_restful import Api

vocab = Blueprint('vocab', __name__, url_prefix='/api/vocab')
vocabs = Blueprint('vocabs', __name__, url_prefix='/api/vocabs')

api = Api(vocab)
api = Api(vocabs)

print('========== 3 vocab ==========')

print('========== 4 vocab ==========')

@vocab.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during user request. %s' % str(e))
    return 'An internal error occurred.', 500