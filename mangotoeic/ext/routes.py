from mangotoeic.user.api import User, Users
from mangotoeic.review.api import Review,Reviews
from mangotoeic.home.api import Home

def initialize_routes(api):
    api.add_resource(Home, '/api')
    api.add_resource(User, '/api/user/<string:id>')
    api.add_resource(Users, '/api/users')
    api.add_resource(Review, '/api/review/<string:id>')
    api.add_resource(Reviews, '/api/reviews/')