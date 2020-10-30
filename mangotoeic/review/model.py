
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
from tensorflow.keras.optimizers import Adam

from keras.models import Sequential 
from keras.layers import Dense, LSTM, Embedding, SimpleRNN
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
    
    
    


# Tk = Prepro()
# # Tk.hook_process() 


# from mangotoeic.review.fromweb import WebCrawler
# wc = WebCrawler() 
# # review = '오류가 너무 많이뜨네요 ;; 별로에요.. 돈줘도 안쓸듯합니다. 앱이 들어가지지도 않고 앱 이따구로 만들거면 때려치세요'
# review = '문제가 다양해서 좋아요. 계속 쓸것 같네요. 영어공부 관심있으신분들은 꼭 써보세요. 무조건 이득입니다!'
# review = wc.strip_emoji(review)
# review = wc.cleanse(review)
# review = Prepro.tokenize(review, Tk.get_stopwords())
# review = Prepro.encoding(review)
# review = Prepro.zeropadding(review)
# lstmmodel = keras.models.load_model('lstm_review_star_model.h5')
# rnnmodel = keras.models.load_model('RNN_review_star_model.h5')
# score = lstmmodel.predict(review)
# score2 = rnnmodel.predict(review)
# prob = score2[-1][np.argmax(score2[-1])] 
# star = int(np.argmax(score[-1])) + 1
# star2 = int(np.argmax(score2[-1])) + 1
# print(score[-1])
# print(prob)
# print(score2[-1])
# print(star)
# print(star2)