import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
basedir = os.path.dirname(os.path.abspath(__file__))
import glob
import sqlite3
import json
import re
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request

from mangotoeic.utils.file_helper import FileReader
from selenium import webdriver
import time

class WebCrawler():
    def __init__(self):
        self.driver = webdriver.Chrome('C:/Users/jongm/Desktop/chromedriver.exe')
        self.reviews = []
    
    def hook_process(self):
        # df = wc.webdata_toCsv(urls)
        # self.add_sentiment(df)
        self.get_data()
         

    def strip_emoji(self,text):
        RE_EMOJI = re.compile(u'([\U00002600-\U000027BF])|([\U0001f300-\U0001f64F])|([\U0001f680-\U0001f6FF])')
        return RE_EMOJI.sub(r'', text)

    def cleanse(self,text):
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
                star = score.split(' ')[3][0]
                comment = review.find('span', {'jsname':"bN97Pc"}).get_text()
                text = wc.cleanse(comment)
                if len(text) > 3:
                    self.reviews.append((text,star))
        self.driver.quit()    
        df = pd.DataFrame(self.reviews, columns = ['review','star'])
        return df

    def add_sentiment(self,df):
        df.loc[(df['star']>=4), 'label'] = 1
        df['label'] = df['label'].fillna(0)
        df.to_csv('앱리뷰csv파일.csv', index=False, encoding='utf-8-sig') 
        return df

    def get_data(self):
        reader = self.reader
        reader.context = basedir
        reader.fname = "앱리뷰csv파일.csv"
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


# if __name__ == "__main__":
#     wc = WebCrawler()
#     wc.hook_process()