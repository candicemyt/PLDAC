import pandas as pd


def load_data():
    data = []
    for i in range(1, 19):
        df = pd.read_csv(f'data/data_ant_m{i}.csv')
        df = df.rename(columns={"file_name": "time"})
        df['time'] = pd.to_numeric(df['time']) / 30
        df['ant_id'] = pd.to_numeric(df['ant_id'])
        df = df.sort_values(by='time', ascending=True)
        del df['date']
        del df['colony']
        data.append(df)
    return data
