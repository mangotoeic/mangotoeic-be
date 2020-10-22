from typing import List
from flask_restful import Resource, reqparse
from mangotoeic.corpus.dao import CorpusDao
from mangotoeic.corpus.dto import CorpusDto

class Corpus(Resource):
    def __init__(self):
        parser = reqparse.RequestParser()  # only allow price changes, no name changes allowed
        parser.add_argument('corId', type=float, required=True, help='This field cannot be left blank')
        parser.add_argument('corpus', type=int, required=True, help='Must enter the store id')
        self.dao = CorpusDao

    def get(self, id):
        item = self.dao.find_by_id(id)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    

class Corpuses(Resource):
    def get(self):
        ...