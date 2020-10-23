import pandas as pd
class RecommendationPro:
    def __init__(self):
        ...
    def read_csv(self):
        df=pd.read_csv("./data/realdata.csv")
        return df
    def hook(self):
        df=self.read_csv()
        df=self.prepro(df)
        return df
    def prepro(self,df):
        
        print(df)
        
        df= df.rename(index={0:'id'},columns={'answered_correctly': "correctAvg"})
        print(df)
        return df


if __name__ == '__main__':
    pro = RecommendationPro()
    pro.hook()
    
