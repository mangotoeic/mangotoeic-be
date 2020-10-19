from typing import List
from flask_restful import Resource, reqparse
from mangotoeic.vocab.dto import VocabDto
from mangotoeic.vocab.dao import VocabDao

def Vocab(Resrouce):
    def __init__(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=False, help='This field cannot be left blank')
        parser.add_argument('user_id', type=int, required=False, help='This field cannot be left blank')
        parser.add_argument('vocabid', type=int, required=False, help='This field cannot be left blank')
        parser.add_argument('answer', type=str, required=False, help='This field cannot be left blank')
        parser.add_argument('Qid', type=int, required=False, help='This field cannot be left blank')
    
    def post(self):
        data = self.parser.parse_args()
        vocab = VocabDto(data['user_id'], data['vocabid'], data['answer'], data['Qid'])
        try:
            vocab.save()
        except:
            return {'message': 'An error occured inserting the vocabulary'}, 500
        return vocab.json(), 201
    
    def get(self, id):
        vocab = Vocab.find_by_id(id)
        if vocab:
            return vocab.json()
        return {'message': 'Vocabulary not found'}, 404

    def put(self, id):
        data = Vocab.parser.parse_args()
        vocab = VocabDao.find_by_id(id)

        vocab.vocab_id = data['vocabid']
        vocab.answer = data['answer']
        vocab.save()
        return vocab.json()

class Vocabs(Resource):
    def get(self):
        return {'vocabs': list(map(lambda vocab: vocab.json(), VocabDao.find_all()))}