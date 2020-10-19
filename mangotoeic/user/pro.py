import pandas as pd


# df = pd.read_csv('./mangotoeic/user/data/sample.csv')

# df2 = df.index.value_counts('content_id')
# df2 = df.value_counts()
# print(df2)
# df3 = df2.head(1000)
# df3.to_csv('./mangotoeic/user/data/sortbycontent.csv')

# print(df2)
# print(df2)
# df2.to_csv('./mangotoeic/user/data/sortbycontent.csv')

# df2.columns = ['user_id', 'user_count']
# df2 = df.sort_values('user_id')
# df3 = df2.head(10)
# df4 = df3.to_csv('./mangotoeic/user/data/sortbycontent.csv')
# df4 = df3[['user_id', 'content_id', 'user_answer', 'answered_correctly', 'prior_question_elapsed_time']]
# df2.to_csv('./mangotoeic/user/data/sortbycontent.csv')
# print(df3)

df = pd.read_csv('./mangotoeic/user/data/train.csv')
count_df = pd.DataFrame(df.user_id.value_counts())
new_index = count_df.merge(df[["content_id"]], left_index=True, right_on="content_id")
df['count'] = new_index['content_id_x']
df2 = df.sort_values(['count'], ascending=False)
df3 = df2.head(10000)
df3.to_csv('./mangotoeic/user/data/sortbycontent.csv')