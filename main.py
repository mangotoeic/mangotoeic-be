print('========== main ==========')
from flask import Flask
from flask_restful import Api
print('========== db ==========')
from mangotoeic.ext.db import url, db
print('========== dbout ==========')
print('========== home ==========')
from mangotoeic.ext.routes import initialize_routes
print('========== homeout ==========')
from mangotoeic.user.api import User, Users

from mangotoeic.odap.api import Odap, Odaps
from mangotoeic.vocab.api import Vocab, Vocabs
from mangotoeic.review import review
from mangotoeic.legacy import legacy
from flask_cors import CORS
from mangotoeic.review.api import Review, Reviews


app = Flask(__name__)
CORS(app)
print('========== url ==========')
print(url)
# app.register_blueprint(review)
app.register_blueprint(legacy)

app.config['SQLALCHEMY_DATABASE_URI'] = url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

initialize_routes(api)

with app.app_context():
    db.create_all()


@app.route('/api/test')
def test():
    return {'test':'SUCCESS'}
print('========== url2 ==========' )
