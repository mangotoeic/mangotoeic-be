import pandas as pd

class OdapPro:
    def __init__(self):
        self.fpath =''
    
    def hook(self):
        df=self.fileread()
        print(df.head())
        return df

    def fileread(self):
        df= pd.read_csv(self.fpath,index_col=False,)
        df = df.drop('Unnamed: 0', axis=1)
        df = df.rename(index ={0:'vocabId'})
        
        return df

if __name__ == '__main__':
    prepro = OdapPro()
    prepro.hook()