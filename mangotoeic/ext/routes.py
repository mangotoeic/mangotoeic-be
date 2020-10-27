from mangotoeic.user.api import User, Users, Auth, Access
print('===============initialize===================')
from mangotoeic.user.api import User, Users
from mangotoeic.review.api import Review,Reviews
from mangotoeic.home.api import Home
from mangotoeic.legacy.api import Legacy ,Legacies
from mangotoeic.vocab.api import Vocab, Vocabs

def initialize_routes(api):
    print('===============initialize===================')
    api.add_resource(Home, '/api')
    api.add_resource(User, '/api/user/<string:id>')
    api.add_resource(Users, '/api/users')
    api.add_resource(Review, '/api/review/<string:id>')
    api.add_resource(Reviews, '/api/reviews/')
    api.add_resource(Legacy, '/api/legacy')
    api.add_resource(Legacies, '/api/legacies')
    # api.add_resource(Vocab, '/api/vocab/')
    api.add_resource(Vocabs, '/api/vocabs/')
