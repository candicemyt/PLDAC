import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


df = pd.read_csv('data_ant.csv')
df = df.rename(columns={"file_name": "num_frame"})

df1 = df[df['colony'] == 'N2']
df1.pop('colony')
df2 = df[df['colony'] == 'N13']
df2.pop('colony')
df3 = df[df['colony'] == 'N4']
df3.pop('colony')

#todo merge les colonnes date et num_frame pour avoir des timestamp exploitables
df1_ant1 = df1[df1['ant_id'] == 1]
df1_ant1.sort_values(by=['num_frame'], ascending=False)
print(df1_ant1)
