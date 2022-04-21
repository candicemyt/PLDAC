import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


# #todo merge les colonnes date et num_frame pour avoir des timestamps exploitables


data = []
for i in range(1,19):
    df = pd.read_csv(f'data/data_ant_m{i}.csv')
    df = df.rename(columns={"file_name": "num_frame"})
    df['num_frame'] = pd.to_numeric(df['num_frame']) / 30
    df = df.sort_values(by='num_frame', ascending=True)
    del df['date']
    print(df.head())
    data.append(df)
