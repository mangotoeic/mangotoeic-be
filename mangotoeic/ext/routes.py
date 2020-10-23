# from mangotoeic.item.api import Item, Items
from mangotoeic.user.api import User, Users, Auth, Access
# from mangotoeic.article.api import Article, Articles
from mangotoeic.home.api import Home

def initialize_routes(api):
    print('========== 2 ==========')
    api.add_resource(Home, '/api')
    # api.add_resource(Item, '/api/item/<string:id>')
    # api.add_resource(Items,'/api/items')
    api.add_resource(User, '/api/user/<string:id>')
    api.add_resource(Users, '/api/users')
    api.add_resource(Access, '/api/access')
    print('===========2-2============')
    # api.add_resource(Article, '/api/article/<string:id>')
    # api.add_resource(Articles, '/api/articles/')