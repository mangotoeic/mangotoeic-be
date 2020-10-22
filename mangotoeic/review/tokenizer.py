
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from konlpy.tag import Okt

from mangotoeic.utils.file_helper import FileReader
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
basedir = os.path.dirname(os.path.abspath(__file__))
from tensorflow import keras

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing import sequence 

from keras.models import Sequential 
from keras.layers import Dense, LSTM, Embedding
from keras.utils import np_utils
 
# from konlpy.tag import Kkma 시간 오래걸려


from sklearn.model_selection import train_test_split

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

        word_tokens = Prepro.tokenize(data=X, stopword = self.stopword_list)
        vocabs = Prepro.vocab_size(tokenlist = word_tokens)
        encodedlist = Prepro.encoding(tokenlist = word_tokens)
        padded = Prepro.zeropadding(encodedlist)
 

        X = padded
        y = Prepro.one_hot_encoding(y)
        X_train, X_test, y_train, y_test = Prepro.split(X,y)
        print(X_test)
        print(y_test)

        Prepro.accuracy_by_keras_LSTM(X_train, X_test, y_train, y_test, vocab_size_for_embedding = vocabs)

    
        
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
        reader.fname = "앱리뷰csv파일.csv"
        reader.new_file()
        review_data = reader.csv_to_dframe()

        review_data['user_id'] = ''
        review_data = review_data[ ['user_id'] + [ col for col in review_data.columns if col != 'user_id' ] ]
        
        return review_data.iloc[10409:12400,:]


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
        print(f'총 단어 수 : {vocabs}')
        return vocabs

    @staticmethod
    def encoding(tokenlist): 
        tokenizer = Tokenizer()
        tokenizer.fit_on_texts(tokenlist)
        return tokenizer.texts_to_sequences(tokenlist)

    

    @staticmethod
    def zeropadding(encodedlist):
        padded = pad_sequences(encodedlist, padding = 'post', maxlen = 250)
        return padded

    @staticmethod 
    def split(X,y):
        X_train, X_test, y_train, y_test = train_test_split(X,y, test_size = .2, random_state=42)
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
        seq.add(Embedding(vocab_size_for_embedding+1,100))
        seq.add(LSTM(150))
        seq.add(Dense(6, activation='softmax'))
        seq.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        run = seq.fit(X_train, y_train, epochs=4, batch_size=10, validation_split=0.1)
        seq.save("review_star_model")
        print('테스트 정확도 : {:.2f}%'.format(seq.evaluate(X_test,y_test)[1]*100))

        return seq.evaluate(X_test,y_test)
 
    @staticmethod
    def one_hot_encoding(col):
        return np_utils.to_categorical(col)
    




# Tk = Prepro()
# Tk.hook_process() 
# review = '이 앱은 정말 너무 좋은 앱입니다. 제 마음을 훔쳐갔어요'
# review = Prepro.tokenize(review, Tk.get_stopwords())
# review = Prepro.encoding(review)
# review = Prepro.zeropadding(review)
# model = keras.models.load_model('review_star_model')
# score = model.predict(review)
# print(score)