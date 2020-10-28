from flask import Flask
from flask_restful import Api
from mangotoeic.ext.db import url, db
from mangotoeic.ext.routes import initialize_routes
from mangotoeic.user.api import User, Users
from mangotoeic.corpus.api import Corpus, Corpuses
from mangotoeic.legacy.api import Legacy, Legacyes
from mangotoeic.newq.api import NewQ, NewQs
from mangotoeic.recommendation.api import Recommendation, Recommendations
from mangotoeic.review.api import Review, Reviews
from mangotoeic.odap.api import Odap, Odaps
from mangotoeic.vocab.api import Vocab, Vocabs
from mangotoeic.review.dao import ReviewDao
from mangotoeic.review.dto import ReviewDto
from mangotoeic.review import review
from mangotoeic.review.model import Prepro  
from mangotoeic.review.fromweb import WebCrawler

from mangotoeic.ext.db import db, openSession


from flask_cors import CORS




print('===========1=================')
app = Flask(__name__)

CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
api = Api(app)

'''
@app.before_first_request
def create_tables():
    db.create_all()
'''
Session = openSession()
session = Session()

with app.app_context():
    db.create_all()
with app.app_context():
    count = ReviewDao.count()
    if count[0] == 0 :
        ReviewDao.insert_many()
  
initialize_routes(api)

 