from flask import Flask, request
from flask_restful import Api
from mangotoeic.ext.db import url, db
from mangotoeic.ext.routes import initialize_routes
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

app = Flask(__name__)
CORS(app, resources={r'/api/*': {"origins": "*"}})
from mangotoeic.user.api import User, Users
from mangotoeic.odap.api import Odap, Odaps
from mangotoeic.resource.legacy import LegacyDao 
from flask_cors import CORS
from mangotoeic.review.api import Review, Reviews
app = Flask(__name__)
CORS(app, resources={r'/api/*': {"origins": "*"}})
print(url)
app.config['SQLALCHEMY_DATABASE_URI'] = url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
db.init_app(app)
api = Api(app)



initialize_routes(api)


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

with app.app_context():
    db.create_all()
    legacy_count = LegacyDao.count()
    print(f'***** Users Total Count is {legacy_count} *****')
    if legacy_count[0] == 0:
        LegacyDao.bulk()
        
initialize_routes(api)
