import logging
from flask import Blueprint
from flask_restful import Api
from mangotoeic.resource.user import User, Users, Auth, Access, Profile 
from mangotoeic.resource.preinfo import PreInfo,Count


user = Blueprint('user', __name__, url_prefix='/api/user')
users = Blueprint('users', __name__, url_prefix='/api/users')

profile = Blueprint('profile', __name__, url_prefix='/api/profile/<int:id>')

auth = Blueprint('auth', __name__, url_prefix='/api/auth')
access = Blueprint('access', __name__, url_prefix='/api/access')

preinfo = Blueprint('diagnosis', __name__, url_prefix='/api/preinfo')
count = Blueprint('diagnosis', __name__, url_prefix='/api/count')

api = Api(count)

api = Api(user)
api = Api(users)
api = Api(access)
api = Api(auth)

api = Api(preinfo)



def initialize_routes(api):
    
    api.add_resource(User, '/api/user')
    api.add_resource(Users, '/api/users')
   
    api.add_resource(Access, '/api/access')
    api.add_resource(Auth, '/api/auth')
   
    api.add_resource(PreInfo, '/api/preinfo')
    api.add_resource(Count, '/api/count')
    api.add_resource(Profile, '/api/profile/<int:id>')
   


    
