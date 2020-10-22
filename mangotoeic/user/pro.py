import pandas as pd

# df = pd.read_csv('./mangotoeic/user/data/sortbycontentid.csv')
# count_df = pd.DataFrame(df.content_id.value_counts())
# new_index = count_df.merge(df[["content_id"]], left_index=True, right_on="content_id")
# # print(new_index)
# df['count'] = new_index['content_id_x']
# df2 = df.sort_values(['count'], ascending=False)
# # print(df)
# df2.to_csv('./mangotoeic/user/data/sortbycontentid2.csv')

# df = pd.read_csv('./mangotoeic/user/data/sortbycontentid2.csv')
# df = df.drop(['count', 'Unnamed: 0', 'Unnamed: 0.1'], axis=1)
# df.to_csv('./mangotoeic/user/data/sortbycontentid3.csv')
# print(df)

df = pd.read_csv('./mangotoeic/user/data/sortbycontentid3.csv')
# print(df.dtypes)
# print(df)
n= len(df['content_id'].unique())
# print(n)
series1 = [x for x in range(1, n+1)]
# print(type(series1))
# print(len(series1))
series2 = [x for x in df['content_id'].unique()]
# print(type(series2))
# print(type(df['content_id']))
# print(len(series2))
# print(series2)
# print(series1)
df['content_id'] = df['content_id'].replace(series2, series1)
print(df['content_id'])
# print(series3)
# print(series2)
# s_to_d=series2.to_frame()
# df=df.drop(['content_id'], axis=1)
# newdf=pd.merge(s_to_d, df, left_index=True , right_index=True ,how='left')
# print(newdf)
# print(df)
# series1 = df['content_id'].replace([x for x in df['content_id'].unique()],[x for x in range(1,n+1)])
# # print(df)
# print(series1)


# used_data_types_dict = {
#     'row_id': 'int64',
#     'timestamp': 'int64',
#     'user_id': 'int32',
#     'content_id': 'int16',
#     'answered_correctly': 'int8',
#     'prior_question_elapsed_time': 'float16',
#     'prior_question_had_explanation': 'boolean'
# }

# train_df = pd.read_csv(
#     './mangotoeic/user/data/train.csv',
#     usecols = used_data_types_dict.keys(),
#     dtype=used_data_types_dict, 
#     index_col = 0
# )

# features_df = train_df.iloc[:int(9 /10 * len(train_df))]
# train_df = train_df.iloc[int(9 /10 * len(train_df)):]

# train_questions_only_df = features_df[features_df['answered_correctly']!=-1]
# grouped_by_user_df = train_questions_only_df.groupby('user_id')
# user_answers_df = grouped_by_user_df.agg({'answered_correctly': ['mean', 'count', 'std', 'median', 'skew']}).copy()
# user_answers_df.columns = ['mean_user_accuracy', 'questions_answered', 'std_user_accuracy', 'median_user_accuracy', 'skew_user_accuracy']

# user_answers_df.to_csv('./mangotoeic/user/data/user_answer_df.csv')
# user_answers_df['median_user_accuracy'].value_counts()

# grouped_by_content_df = train_questions_only_df.groupby('content_id')
# content_answers_df = grouped_by_content_df.agg({'answered_correctly': ['mean', 'count', 'std', 'median', 'skew'] }).copy()
# content_answers_df.columns = ['mean_accuracy', 'question_asked', 'std_accuracy', 'median_accuracy', 'skew_accuracy']

# content_answers_df['median_accuracy'].value_counts()