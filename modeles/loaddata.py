import pandas as pd

def load_dataset1():
    data = []
    for i in range(1, 19):
        df = pd.read_csv(f'data/dataset1/data_ant_m{i}.csv')
        df = df.rename(columns={"file_name": "time"})
        df['time'] = pd.to_numeric(df['time']) / 30
        df['ant_id'] = pd.to_numeric(df['ant_id'])
        df = df.sort_values(by='time', ascending=True)
        del df['date']
        del df['colony']
        data.append(df)
    return data


def load_dataset2():
    data = []
    metadata = pd.read_csv('data/dataset2/metadata.csv')
    for j in range(1,7):
        col = []
        for i in range(1,42):
            col.append(pd.read_csv(f'data/dataset2/Colony{j}/day{i}.csv'))
        data.append(col)
    return metadata, data


def load_data(dataset):
    if dataset == 'dataset1':
        return load_dataset1()
    elif dataset == 'dataset2':
        return load_dataset2()


