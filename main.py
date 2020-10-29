from flask import Flask
from flask_restful import Api
from mangotoeic.ext.db import url, db
from mangotoeic.ext.routes import initialize_routes
from mangotoeic.user.api import User, Users
from mangotoeic.resource.legacy import LegacyDao 
from mangotoeic.resource.vocab import VocabDao 
from flask_cors import CORS
from mangotoeic.review.api import Review, Reviews
app = Flask(__name__)
CORS(app, resources={r'/api/*': {"origins": "*"}})
print(url)
app.config['SQLALCHEMY_DATABASE_URI'] = url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
api = Api(app)
with app.app_context():
    db.create_all()
    legacy_count = LegacyDao.count()
    print(f'***** Users Total Count is {legacy_count} *****')
    if legacy_count[0] == 0:
        LegacyDao.bulk()
    vocab_count = VocabDao.count()
    print(f'***** Users Total Count is {vocab_count} *****')
    if vocab_count[0] == 0:
        VocabDao.bulk()
initialize_routes(api)