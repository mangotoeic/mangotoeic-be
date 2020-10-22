import pandas as pd
class CorpusPro:
    def __init__(self):

        self.fpath ='./data/problemcorpus.csv'
    def hook(self):
        df=self.fileread()
        print(df.head(30))
        return df
    def fileread(self):
        df= pd.read_csv(self.fpath,index_col=False,)
        df= df.set_index(['corId'])
    
        print(df)
        return df
    




if __name__ == '__main__':
    prepro = CorpusPro()
    prepro.hook()
    
    
