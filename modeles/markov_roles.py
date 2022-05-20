import numpy as np

def markov_chain(metadata, colony):

    grouptoindex = {'F':0, 'C' :1, 'N':2, 'Q':3}
    mat_A = np.zeros((4,4))
    df_by_col = metadata[metadata['colony_act'] == colony]

    for index, data in df_by_col.iterrows():

        if data['period1to2'] == 'same':
            group = data['group_period1']
            if group !='Nan':
                mat_A[grouptoindex[group]][grouptoindex[group]] += 1

        if data['period1to2'] == 'switch':
            group1 = data['group_period1']
            group2 = data['group_period2']
            if group1 != 'Nan' and group2 != 'Nan':
                mat_A[grouptoindex[group1]][grouptoindex[group2]] += 1

        if data['period2to3'] == 'same':
            group = data['group_period2']
            if group !='Nan':
                mat_A[grouptoindex[group]][grouptoindex[group]] += 1

        if data['period2to3'] == 'switch':
            group1 = data['group_period2']
            group2 = data['group_period3']
            if group1 != 'Nan' and group2 != 'Nan':
                mat_A[grouptoindex[group1]][grouptoindex[group2]] += 1

        if data['period3to4'] == 'same':
            group = data['group_period3']
            if group !='Nan':
                mat_A[grouptoindex[group]][grouptoindex[group]] += 1

        if data['period3to4'] == 'switch':
            group1 = data['group_period3']
            group2 = data['group_period4']
            if group1 != 'Nan' and group2 != 'Nan':
                mat_A[grouptoindex[group1]][grouptoindex[group2]] += 1

    for i in range(4):
        mat_A[i] = mat_A[i]/np.sum(mat_A[i])
    return mat_A

