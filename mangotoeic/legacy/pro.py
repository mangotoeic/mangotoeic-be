import pandas as pd

class LegacyPro:
    def __init__(self):

        self.fpath ='./data/toeic_test.json'
    def hook(self):
        df=self.fileread()
        df=self.filerename(df)
        return df
    def fileread(self):
        df= pd.read_json(self.fpath)
        print(df.transpose())
        # df=df.rename(columns={"Unnamed: 0": "index"})
        # print(df)
        # df=df.set_index(['index'])
        # print(df)
        return df.transpose()
    def filerename(self,df):
        df= df.rename(columns={'1':"ansA","2":"ansB","3":"ansC","4":"ansD","question":"question","anwser":"answer"})
        print(df)
        df.index.name= 'qId'
        print(df)
        return df




if __name__ == '__main__':
    prepro = LegacyPro()
    prepro.hook()