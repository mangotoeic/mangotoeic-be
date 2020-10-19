from typing import List
from flask_restful import Resource, reqparse
from mangotoeic.recommendation.dao import RecommendationDao
from mangotoeic.recommendation.dto import RecommendationDto

class Recommendation(Resource):
    def __init__(self):
        parser = reqparse.RequestParser()  # only allow price changes, no name changes allowed
        self.dao = RecommendationDao

    def get(self, id):
        item = self.dao.find_by_id(id)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    

class Recommendations(Resource):
    def get(self):
        ...