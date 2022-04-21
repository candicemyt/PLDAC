import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


df1 = pd.read_csv('data_ant_m1.csv')
df2 = pd.read_csv('data_ant_m2.csv')
print(df1.columns)
print(df2.columns)
# df = df.rename(columns={"file_name": "num_frame"})
# df['num_frame'] = df['num_frame']/30
# dates = set(df['date'])
# colonies = set(df['colony'])
# data = []
# for d in dates:
#     df_date = df[df['date'] == d]
#     df_date.pop('date')
#     for c in colonies:
#         df_col = df_date[df_date['colony'] == c]
#         df_col.pop('colony')
#         data.append(df_col)
# print(data[0])



# #todo merge les colonnes date et num_frame pour avoir des timestamps exploitables
# df1_ant1 = df1[df1['ant_id'] == 1]
# df1 = df1.sort_values(by=['num_frame'], ascending=True)
# df1['num_frame'] = df1['num_frame']/30
# print(df1)


#xls = pd.ExcelFile()
# data = []
# for i in range(1,19):
#     file = pd.read_excel('data_ant.xlsx', f"m{i}")
#     file.to_csv(f"data/m{i}.csv", header=True)
#     df = pd.read_csv(f"data/m{i}.csv")
#     df = df.rename(columns={"file_name": "num_frame"})
#     print(df.columns)
#     print(df.head())
#     data.append(df)


# file = pd.read_excel('m1.xlsx')
# file.to_csv('m1.csv', header=True)
# df = pd.read_csv('m1.csv')
# print(df.columns)
#
#
# file = pd.read_excel('m2.xlsx')
# file.to_csv('m2.csv', header=True)
# df = pd.read_csv('m2.csv')
# print(df.columns)