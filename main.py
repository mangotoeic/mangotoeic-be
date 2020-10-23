from flask import Flask, request
from flask_restful import Api
from flask_cors import CORS
from mangotoeic.ext.db import url, db
from mangotoeic.ext.routes import initialize_routes
from mangotoeic.user.api import User, Users
from mangotoeic.corpus.api import Corpus, Corpuses
from mangotoeic.legacy.api import Legacy, Legacyes
from mangotoeic.newq.api import NewQ, NewQs
from mangotoeic.recommendation.api import Recommendation, Recommendations
from mangotoeic.reviewboard.api import Review, Reviews
from mangotoeic.odap.api import Odap, Odaps
from mangotoeic.vocab.api import Vocab, Vocabs
from mangotoeic.user.dto import UserDto
from mangotoeic.user import user
from mangotoeic.ext.routes import initialize_routes

print('========== 1 ==========')
app = Flask(__name__)
CORS(app)
app.register_blueprint(user)

print(url)
app.config['SQLALCHEMY_DATABASE_URI'] = url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
api = Api(app)

# @app.before_first_request
# def create_tables():
#     db.create_all()

initialize_routes(api)

# with app.app_context():
#     db.create_all()


@app.route('/api/test')
def test():
    return {
    "1": {
        "1": "suffer",
        "2": "suffers",
        "3": "suffering",
        "4": "suffered",
        "anwser": "suffered",
        "question": "The assets of Marble Faun Publishing Company ___ last quarter when one of their main local distributors went out of business."
    },
    "2": {
        "1": "him",
        "2": "his",
        "3": "himself",
        "4": "he",
        "anwser": "his",
        "question": "lndie film director Luke Steele will be in London for the premiere of ___ new movie."
    },
    "3": {
        "1": "full",
        "2": "complete",
        "3": "all",
        "4": "total",
        "anwser": "all",
        "question": "Laboratory employees are expected to wear a name tag and carry identification at ___ times."
    },
    "4": {
        "1": "method",
        "2": "guide",
        "3": "staff",
        "4": "role",
        "anwser": "guide",
        "question": "The latest training ___ contains tips on teaching a second language to international students:"
    },
    "5": {
        "1": "qualified",
        "2": "qualifications",
        "3": "qualify",
        "4": "qualifying",
        "anwser": "qualifications",
        "question": "Once you have your resume with references and ___ , please submit it to the Human Resources Department on the 3rd floor."
    },
    "6": {
        "1": "soon",
        "2": "shortly",
        "3": "recently",
        "4": "yet",
        "anwser": "recently",
        "question": "Ursa Major Corp. has ___ negotiated a deal with a Russian competitor in surveying the Kamchatka Peninsula."
    },
    "7": {
        "1": "having",
        "2": "will have",
        "3": "was having",
        "4": "has",
        "anwser": "was having",
        "question": "Ms. Cho relayed her concerns about the company's financial situation while she ___ a meeting with the manager."
    },
    "8": {
        "1": "necessary",
        "2": "necessarily",
        "3": "necessitate",
        "4": "necessity",
        "anwser": "necessary",
        "question": "Whether it is ___ to register for a student discount card depends on the needs of the individual."
    },
    "9": {
        "1": "materials",
        "2": "sessions",
        "3": "experiences",
        "4": "positions",
        "anwser": "sessions",
        "question": "Even experienced clerks are encouraged to attend training ___ to keep them updated on new ideas in the world of banking."
    },
    "10": {
        "1": "they",
        "2": "them",
        "3": "their",
        "4": "themselves",
        "anwser": "themselves",
        "question": "Workers are advised not to operate certain machines by ___ ."
    }
}

# @app.route('/api/test2', methods=['POST'])
# def registerUser():
#     data = request.data
#     user_name = data['user_name']
#     password = data['password']
#     email = data['email']
#     return data
