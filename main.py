from flask import Flask, request
print('========== main ==========')
from flask import Flask
from flask_restful import Api
print('========== db ==========')
from mangotoeic.ext.db import url, db
print('========== dbout ==========')
print('========== home ==========')
from mangotoeic.ext.routes import initialize_routes
print('========== homeout ==========')
from mangotoeic.user.user import User, Users, UserDto
from mangotoeic.user import user
from mangotoeic.odap.api import Odap
from mangotoeic.vocab.api import Vocab, Vocabs
import json
from mangotoeic.review import review
from mangotoeic.legacy import legacy
from mangotoeic.vocab import vocab, vocabs
from flask_cors import CORS
from mangotoeic.review.api import Review, Reviews

print('========== 1 ==========')
app = Flask(__name__)
CORS(app, resources={r'/api/*': {"origins": "*"}})
app.config['SQLALCHEMY_DATABASE_URI'] = url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
db.init_app(app)
api = Api(app)


# @app.before_first_request
# def create_tables():
#     db.create_all()

initialize_routes(api)

# with app.app_context():
#     db.create_all()


@app.route('/api/minitest')
def minitest():
    with open('./mangotoeic/legacy/data/toeic_test.json', 'r', encoding='utf-8') as json_file:
        json_data = json.load(json_file)
        json_file.close()
    return json_data

@app.route('/api/diagnosis')
def diagnosis():
    with open('./mangotoeic/minitest/data/diagnosis.json', 'r', encoding='utf-8') as json_file:
        json_data = json.load(json_file)
        json_file.close()
    return json_data

