import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from tslearn.utils import to_time_series
from tslearn.clustering import TimeSeriesKMeans
from sklearn.model_selection import train_test_split

data = pd.read_csv('jaguar_movement_data.csv',parse_dates=True,index_col='timestamp',usecols=[1,2,3,6])
print(data.columns)
data_i1 = data[data['individual.local.identifier (ID)'] == 1]
data_i1.pop('individual.local.identifier (ID)')
print(data_i1)
#X_train, y_train, X_test, y_test = train_test_split(data)
# km = TimeSeriesKMeans(n_clusters=3, metric="dtw", max_iter=10)
# km.fit(data[0:1000])
# pred = km.predict(data[1001:1101])
# print(pred)
#
