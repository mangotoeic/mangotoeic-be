from mangotoeic.item.item_api import ItemsApi
def initialize_routes(api):
    api.add_resource(ItemsApi, '/api/items')