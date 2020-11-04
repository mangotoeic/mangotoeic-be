from typing import List
from flask import request
from flask_restful import Resource, reqparse   
 
from mangotoeic.ext.db import engine
from flask import jsonify
import keras
import numpy as np
 
from mangotoeic.ext.db import db, openSession
from mangotoeic.resource.user import UserDto
from sqlalchemy import func
import pandas as pd
import json




import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
basedir = os.path.dirname(os.path.abspath(__file__))
import re
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request

from mangotoeic.utils.file_helper import FileReader
from selenium import webdriver
import time
import matplotlib.pyplot as plt
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing import sequence 
from tensorflow.keras.optimizers import Adam

from keras.models import Sequential 
from keras.layers import Dense, LSTM, Embedding, SimpleRNN
from keras.utils import np_utils
from sklearn.model_selection import train_test_split
# from konlpy.tag import Kkma 시간 오래걸려


# ==============================================================
# ====================                     =====================
# ====================    Crawling         =====================
# ====================                     =====================
# ==============================================================

class WebCrawler():
    def __init__(self):
        self.driver = None
        self.reviews = []
    
    def hook_process(self):
        # df = wc.webdata_toCsv(urls)
        # self.add_sentiment(df)
        self.get_data()
         
    @staticmethod
    def strip_emoji(text):
        RE_EMOJI = re.compile(u'([\U00002600-\U000027BF])|([\U0001f300-\U0001f64F])|([\U0001f680-\U0001f6FF])')
        return RE_EMOJI.sub(r'', text)
        
    @staticmethod
    def cleanse(text):
        pattern = '[\r|\n]' # \r \n 제거
        text = re.sub(pattern,' ', text)
        RE_EMOJI = re.compile(u'([\U00002600-\U000027BF])|([\U0001f300-\U0001f64F])|([\U0001f680-\U0001f6FF])')
        text =  RE_EMOJI.sub(r'', text) # 이모티콘 제거
        pattern = '([ㄱ-ㅎㅏ-ㅣ])+' # 한글 자음모음 제거
        text = re.sub(pattern,' ', text)
        pattern = '[^\w\s]' # 특수기호 제거
        text = re.sub(pattern, ' ', text)
        pattern = re.compile(r'\d+') # 숫자제거
        text= re.sub(pattern, ' ', text) 
        pattern = re.compile('[^ ㄱ-ㅣ가-힣]+') #영어 제거, 한글만 남기기
        text = re.sub(pattern, '', text)
        pattern = re.compile(r'\s+') # 띄어쓰기 여러개 붙어있을 시 제거
        text = re.sub(pattern,' ', text)
        return text

    def webdata_toCsv(self,urls):
        self.driver = webdriver.Chrome('mangotoeic/resource/data/chromedriver86.0424.exe')
        for i in range(len(urls)):
            url = urls[i]
            self.driver.get(url)
            self.driver.maximize_window()
            time.sleep(2)
            n=0
            nomorebutton=0
            while n<30 and nomorebutton < 5: # 3200개 뽑아줌
                for i in range(4):
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(1)
                    try:
                        self.driver.find_element_by_xpath("//span[@class='RveJvd snByac']").click()
                        n += 1
                        nomorebutton = 0
                    except Exception:
                        nomorebutton += 1   
            mysoup = BeautifulSoup(self.driver.page_source, 'html.parser')

            allreviews = mysoup.find_all('div', {'class':'d15Mdf bAhLNe'})
            
            for review in allreviews:
                score = review.find('div', {'role':'img'})['aria-label']
                star = int(score.split(' ')[3][0]) - 1
                comment = review.find('span', {'jsname':"bN97Pc"}).get_text()
                text = WebCrawler.cleanse(comment)
                if len(text) > 3:
                    self.reviews.append((text,star))
        self.driver.quit()    
        df = pd.DataFrame(self.reviews, columns = ['review','star'])
        return df

    def add_sentiment(self,df):
        df.loc[(df['star']>=4), 'label'] = 1
        df['label'] = df['label'].fillna(0)
        df.to_csv('앱리뷰csv파일2.csv', index=False, encoding='utf-8-sig') 
        return df

    def get_data(self):
        reader = self.reader
        reader.context = basedir
        reader.fname = "앱리뷰csv파일2.csv"
        newfile=reader.new_file()
        review_data = reader.csv_to_dframe(newfile)
        return review_data.head(5)


urls = ['https://play.google.com/store/apps/details?id=com.taling&showAllReviews=true',
'https://play.google.com/store/apps/details?id=com.mo.kosaf&showAllReviews=true',
'https://play.google.com/store/apps/details?id=com.qualson.superfan&showAllReviews=true',
'https://play.google.com/store/apps/details?id=com.belugaedu.amgigorae&showAllReviews=true',
'https://play.google.com/store/apps/details?id=co.riiid.vida&showAllReviews=true',
'https://play.google.com/store/apps/details?id=com.hackers.app&showAllReviews=true',
'https://play.google.com/store/apps/details?id=com.pallo.passiontimerscoped&showAllReviews=true',
'https://play.google.com/store/apps/details?id=me.mycake&showAllReviews=true',
'https://play.google.com/store/apps/details?id=com.coden.android.ebs&showAllReviews=true',
'https://play.google.com/store/apps/details?id=kr.co.ebse.player&showAllReviews=true',
'https://play.google.com/store/apps/details?id=com.adrock.driverlicense300&showAllReviews=true',
'https://play.google.com/store/apps/details?id=net.tandem&showAllReviews=true',
'https://play.google.com/store/apps/details?id=kr.co.influential.youngkangapp&showAllReviews=true',
'https://play.google.com/store/apps/details?id=egovframework.tcpotal.mobile.lur&showAllReviews=true',
'https://play.google.com/store/apps/details?id=com.hackers.app.hackersmp3',
'https://play.google.com/store/apps/details?id=kr.go.hrd.app',
'https://play.google.com/store/apps/details?id=net.pedaling.class101&showAllReviews=true',
'https://play.google.com/store/apps/details?id=com.cjkoreaexpress&showAllReviews=true',
'https://play.google.com/store/apps/details?id=com.hackers.app.toeicvoca'
]


# ==============================================================
# ====================                     =====================
# ====================    Modeling    =====================
# ====================                     =====================
# ==============================================================

class Prepro():
    def __init__(self):
     
        self.reader = FileReader()
        self.okt = Okt()
        self.df = self.get_data() 
        self.stopwords_list = []   

    def hook_process(self): 
        df = self.df
        df = Prepro.drop_col(df, col = 'label')
        self.stopword_list = self.get_stopwords()
   
        X = df['review']
        y = df['star'] 

        # Prepro.graph_review_length_frequency(X)
 
        X_train, X_test, y_train, y_test = Prepro.split(X,y)

        X_train_word_tokens = Prepro.tokenize(data=X_train, stopword = self.stopword_list)
        X_test_word_tokens = Prepro.tokenize(data=X_test, stopword = self.stopword_list)
        vocabs = Prepro.vocab_size(tokenlist = X_train_word_tokens)
        X_train_encodedlist = Prepro.encoding(tokenlist = X_train_word_tokens)
        X_test_encodedlist = Prepro.encoding(tokenlist = X_test_word_tokens)
        # print('리뷰의 최대 길이 :',max(len(l) for l in X_train_encodedlist))
        # print('리뷰의 평균 길이 :',sum(map(len, X_train_encodedlist))/len(X_train_encodedlist))
        # plt.hist([len(s) for s in X_train_encodedlist], bins=50)
        # plt.xlabel('length of samples')
        # plt.ylabel('number of samples')
        # plt.show()
        X_train_padded = Prepro.zeropadding(X_train_encodedlist)
        X_test_padded = Prepro.zeropadding(X_test_encodedlist)
        y_train_onehot = Prepro.one_hot_encoding(y_train)
        y_test_onehot = Prepro.one_hot_encoding(y_test)


        Prepro.accuracy_by_keras_LSTM(X_train = X_train_padded, X_test=X_test_padded, y_train=y_train_onehot, y_test=y_test_onehot, vocab_size_for_embedding = vocabs)
        Prepro.accuracy_by_keras_RNN(X_train = X_train_padded, X_test=X_test_padded, y_train=y_train_onehot, y_test=y_test_onehot, vocab_size_for_embedding = vocabs)

    
        
    def get_stopwords(self):
        reader = self.reader
        reader.context = os.path.join(basedir, 'data')
        reader.fname = '불용어.txt'
        file = reader.new_file()
        f= open(file,'r', encoding='utf8')
        stopwords = f.read()
        f.close()
        stopword_list = stopwords.split('\n')
        return stopword_list


    def get_data(self): 
        reader = self.reader
        reader.context = os.path.join(basedir, 'data')
        reader.fname = '앱리뷰csv파일2.csv'
        reader.new_file()
        review_data = reader.csv_to_dframe()
        return review_data


    @staticmethod
    def tokenize(data,stopword):
        okt = Okt()
        wordtoken_list = []
        for line in data:
            onereview=[]
            word_tokens = okt.morphs(line)
            for word in word_tokens:
                if word not in stopword:
                    onereview.append(word)
            wordtoken_list.append(onereview) 
        return wordtoken_list

    @staticmethod
    def vocab_size (tokenlist):
        tokenizer = Tokenizer()
        tokenizer.fit_on_texts(tokenlist)
        vocabs = len(tokenizer.word_index)
        # print(f'총 단어 수 : {vocabs}')
        return vocabs

    @staticmethod
    def encoding(tokenlist): 
        tokenizer = Tokenizer()
        tokenizer.fit_on_texts(tokenlist)
 
        return tokenizer.texts_to_sequences(tokenlist)

    @staticmethod
    def one_hot_encoding(col):
        return np_utils.to_categorical(col) 

    @staticmethod
    def zeropadding(encodedlist):
        padded = pad_sequences(encodedlist, padding = 'post', maxlen = 80)
        return padded

    @staticmethod 
    def split(X,y):
        X_train, X_test, y_train, y_test = train_test_split(X,y, test_size = .2, random_state=2)
        return X_train, X_test, y_train, y_test

    @staticmethod
    def graph_review_length_frequency(X):
        print('리뷰 최대 길이 : {}'.format(max(len(l) for l in X))) 
        print('리뷰 평균 길이 : {}'.format(sum(map(len, X)) / len(X))) 
        plt.hist([len(s) for s in X], bins=50) 
        plt.xlabel('리뷰 길이') 
        plt.ylabel('number of Data') 
        plt.show()
    
    @staticmethod
    def drop_col(df, col):
        return df.drop([col], axis = 1)

    @staticmethod
    def accuracy_by_keras_LSTM(X_train,X_test,y_train,y_test,vocab_size_for_embedding):
        seq = Sequential()
        seq.add(Embedding(vocab_size_for_embedding+1,150))
        seq.add(LSTM(150,activation='softmax')) 
        seq.add(Dense(5, activation='softmax'))
        opt = Adam(learning_rate = .0001)
        seq.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])
        seq.fit(X_train, y_train, epochs=3, batch_size=10)
        seq.save("lstm_review_star_model.h5")
        print('테스트 정확도 : {:.2f}%'.format(seq.evaluate(X_test,y_test)[1]*100))

        return seq.evaluate(X_test,y_test)
    

    @staticmethod
    def accuracy_by_keras_RNN(X_train,X_test,y_train,y_test,vocab_size_for_embedding):
        seq = Sequential()
        seq.add(Embedding(vocab_size_for_embedding+1, 150))
        seq.add(SimpleRNN(256)) 
        seq.add(Dense(5, activation='softmax'))
        opt = Adam(learning_rate = .0001)
        seq.compile(optimizer='rmsprop',loss='categorical_crossentropy',metrics=['accuracy'])
        seq.fit(X_train, y_train, epochs=3, batch_size=10, validation_split=0.1)
        seq.save("RNN_review_star_model.h5")
        print('테스트 정확도 : {:.2f}%'.format(seq.evaluate(X_test,y_test)[1]*100))
        return seq.evaluate(X_test,y_test)


# ==============================================================
# =====================                  =======================
# ===================== DTO and Service  =======================
# =====================                  =======================
# ==============================================================
Session = openSession()
session = Session()

class ReviewDto(db.Model):
    __tablename__ = "reviews"
    __table_args__ = {'mysql_collate':'utf8_general_ci'}

    id: int = db.Column(db.Integer, primary_key=True, index=True)
    email : str = db.Column(db.String(20)) 
    review: str = db.Column(db.String(500))
    star: int = db.Column(db.Integer)  
    
    def __init__(self, id = None, email=None, review=None, star=None):
        self.id = id
        self.email = email
        self.review = review
        self.star = star 
    
        

    def __repr__(self):
        return f'Review(id=\'{self.id}\',email=\'{self.email}\',review=\'{self.review}\', star=\'{self.star}\',)'

    @property
    def json(self):
        return {
            'id' : self.id,
            'email' : self.email,
            'review' : self.review,
            'star' : self.star
        }

class ReviewVo:
    id: int = 1
    email : str = ''
    review: str = ''
    star: int = 1
    

    
class ReviewService(object):

    @staticmethod
    def predict(input):
        wc = WebCrawler()
        model = Prepro()
        reviewtext = wc.strip_emoji(input)
        reviewtext = wc.cleanse(reviewtext)
        reviewtext = model.tokenize(reviewtext, model.get_stopwords())
        reviewtext = model.encoding(reviewtext)
        reviewtext = model.zeropadding(reviewtext)
        print(os.path)
        rnnmodel = keras.models.load_model(os.path.join('mangotoeic','model','RNN_review_star_model.h5'))
        predictions = rnnmodel.predict(reviewtext)
        prob = predictions[-1][np.argmax(predictions[-1])]*100
        prob = round(prob, 2)
        star = int(np.argmax(predictions[-1])) + 1
        return [prob,star]
        


# ==============================================================
# =====================                  =======================
# =====================    Dao    =======================
# =====================                  =======================
# ==============================================================


Session = openSession()
session = Session()

class ReviewDao(ReviewDto):
    
    @staticmethod
    def find_all():
        return session.query(ReviewDto).all()

    @classmethod 
    def find_by_email(cls,email):
        return session.query(ReviewDto).filter(ReviewDto.email.like(f'%{email}%')).all() 
      

    @classmethod
    def find_by_id(cls,id):
        return session.query(ReviewDto).filter(ReviewDto.email.like(f'%{id}%')).one()

    @classmethod
    def find_by_star(cls,star):
        return session.query(ReviewDto).filter(ReviewDto.email.like(f'%{star}%')).all()

    @classmethod
    def find_by_review(cls,review):
        return session.query(ReviewDto).filter(ReviewDto.email.like(f'%{review}%')).all()

    @staticmethod
    def save(review):
        session.add(review)
        session.commit()
        
    @staticmethod
    def update(review):
        session.add(review)
        session.commit()

    @classmethod
    def delete(cls,id):
        data = cls.query.get(id)
        session.delete(data)
        session.commit()
    
    @staticmethod
    def count():
        return session.query(func.count(ReviewDto.id)).one()

    @staticmethod
    def insert_many():
        service = Prepro()
        df = service.get_data()
        df = df.iloc[10408:12408,:]
        session.bulk_insert_mappings(ReviewDto, df.to_dict(orient = 'records'))
        session.commit()
        session.close()
        print('done') 

     


# ==============================================================
# =====================                  =======================
# =====================    Resourcing    =======================
# =====================                  =======================
# ==============================================================


parser = reqparse.RequestParser()
 
class Review(Resource):

    @staticmethod
    def post():
       
        parser.add_argument('email', type = str, required = True, help = 'This field should be email, cannot be left blank')
        parser.add_argument('review', type = str, required = True, help = 'This field should be review, cannot be left blank') 
        args = parser.parse_args()
        print(f'[ Review Write with {args.email} ]')

        probstar = ReviewService.predict(args.review)
        print(f'예측 별점은 {probstar[0]}% 의 확률로 {probstar[1]}입니다')
        new_review = ReviewDto(email=args.email, review=args.review, star=probstar[1])
        print(new_review)
        try:
            ReviewDao.save(new_review) 
            return {'star': probstar[1], 'prob':probstar[0]}, 200
        except:
            return {'message' : ' an error occured while inserting review'}, 500 

    @staticmethod 
    def get(review: str):
        print(review)
        try:
            reviews = ReviewDao.find_by_review(review)
            if reviews:
                print('get여기까지왔어')
                print(f'{reviews}')
                print(reviews.json())
                print(json.dumps(reviews))
                print('================================')
                return {'review':review.json()}, 200
        except Exception as e:
            return {'message': 'review not found'}, 404 


    @staticmethod
    def update():
        args = parser.parse_args()
        print(f'Review {args.email} updated')
        return {'code' :0, 'message' : 'Success'}, 200

    @staticmethod
    def delete():
        args = parser.parse_args()
        print(f'Review posted by {args.email} deleted')
        return {'code' :0, 'message' : 'Success'}, 200

 

class Reviews(Resource): 

    @staticmethod
    def get():
        df = pd.read_sql_table('reviews', engine.connect()) 
        return json.loads(df.to_json(orient = 'records'))

    @staticmethod
    def post():
        rd = ReviewDao()
        rd.insert_many('reviews')
        