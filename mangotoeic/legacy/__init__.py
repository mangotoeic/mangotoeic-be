import logging
from flask import Blueprint
from flask_restful import Api

legacy = Blueprint('legacy', __name__, url_prefix='/api/legacy')
legacies = Blueprint('legacies', __name__, url_prefix='/api/legacies')

api = Api(legacy)
api = Api(legacies)

print('========== 3 legacy==========')

print('========== 4 legacy==========')
@legacy.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during user request. %s' % str(e))
    return 'An internal error occurred.', 500