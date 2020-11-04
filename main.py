from flask import Flask, request
from flask_restful import Api
from mangotoeic.ext.db import url, db
from mangotoeic.ext.routes import initialize_routes 
from mangotoeic.resource.legacy import LegacyDao 
from mangotoeic.resource.vocab import VocabDao 
from mangotoeic.resource.user import UserDao
from mangotoeic.resource.review import ReviewDao
from flask_cors import CORS
import json



print('===========1=================')
app = Flask(__name__)
CORS(app, resources={r'/api/*': {"origins": "*"}})
print(url)

app.config['SQLALCHEMY_DATABASE_URI'] = url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False

db.init_app(app)
api = Api(app)


@app.route('/api/minitest')
def minitest():
    with open('./mangotoeic/legacy/data/toeic_test.json', 'r', encoding='utf-8') as json_file:
        json_data = json.load(json_file)
        json_file.close()
    return json_data

@app.route('/api/diagnosis')
def diagnosis():
    with open('./mangotoeic/resource/data/diagnosis.json', 'r', encoding='utf-8') as json_file:
        json_data = json.load(json_file)
        json_file.close()
    return json_data

with app.app_context():
    db.create_all()
    legacy_count = LegacyDao.count()
    print(f'***** Legacies Total Count is {legacy_count} *****')
    if legacy_count[0] == 0:
        LegacyDao.bulk()

    vocab_count = VocabDao.count()
    print(f'***** Vocab Total Count is {vocab_count} *****')
    if vocab_count[0] == 0:
        VocabDao.bulk()

    user_count = UserDao.count()
    print(f'***** Users Total Count is {user_count} *****')
    if user_count[0] == 0:
        UserDao.bulk()

    review_count = ReviewDao.count()
    print(f'***** Review Total Count is {review_count} *****')
    if review_count[0] == 0 :
        ReviewDao.insert_many()


initialize_routes(api)
