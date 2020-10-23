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
from mangotoeic.review import review
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
print('========== url ==========')
print(url)
app.register_blueprint(review)
app.config['SQLALCHEMY_DATABASE_URI'] = url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

initialize_routes(api)
