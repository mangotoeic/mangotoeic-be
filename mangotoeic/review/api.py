from typing import List
from flask import request
from flask_restful import Resource, reqparse
from mangotoeic.review.dao import ReviewDao
from mangotoeic.review.fromweb import WebCrawler
from mangotoeic.review.model import Prepro
from mangotoeic.review.dto import ReviewDto, ReviewVo
import json
import pandas as pd
from mangotoeic.ext.db import engine
from flask import jsonify
import keras
import numpy as np

parser = reqparse.RequestParser()
parser.add_argument('email', type = str, required = True, help = 'This field should be email, cannot be left blank')
parser.add_argument('review', type = str, required = True, help = 'This field should be review, cannot be left blank') 

class Review(Resource):

    @staticmethod
    def post():
        args = parser.parse_args() 
        review_vo = ReviewVo()    
        review_vo.email = args.email
        review_vo.email = args.review

        reviewtext = WebCrawler.strip_emoji(args.review)
        reviewtext = WebCrawler.cleanse(reviewtext)
        reviewtext = Prepro.tokenize(reviewtext, Prepro.get_stopwords())
        reviewtext = Prepro.encoding(reviewtext)
        reviewtext = Prepro.zeropadding(reviewtext)


        rnnmodel = keras.models.load_model('RNN_review_star_model')
        predictions = rnnmodel.predict(reviewtext)
        star = np.argmax(predictions[0])

        print(f'예측 별점은 {star}입니다')
        
        return {'star':int(star)}, 200 
    
    def get(self,id):
        review = ReviewDao.find_by_id(id)
        if review:
            return review.json()
        return {'message': 'review not found'}, 404 


    def put(self, id):
        data = Review.parser.parse_args()
        searched = ReviewDao.find_by_id(id)

        searched.email = searched['email']
        searched.review = searched['review']      
        searched.star = searched['star']
        searched.save()
        return searched.json()

class Reviews(Resource): 

    def get(self):
        df = pd.read_sql_table('reviews', engine.connect())
        return json.loads(df.to_json(orient = 'records'))


        # return {'reviews': list(map(lambda review: review.json(), ReviewDao.find_all()))}
  
    # def post(self):
    #     rd = ReviewDao()
    #     rd.insert_many('reviews')
        
    #     print('===============6=========================')

    