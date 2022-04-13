import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv('jaguar_movement_data.csv',parse_dates=True,index_col='timestamp',usecols=[1,2,3,6])
print(data.head())
print(data.index)
