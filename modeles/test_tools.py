import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score

def trainset(col, period, metadata):
    metadata_wo_col1 = metadata[metadata['colony_act'] != col] #on entraine sur toutes les colonies sauf col

    df_datax_train = pd.DataFrame().assign(nb_foraging_events=metadata_wo_col1["nb_foraging_events"],
                                           visits_to_brood=metadata_wo_col1["visits_to_brood"],
                                           visits_to_nest_entrance=metadata_wo_col1['visits_to_nest_entrance'],
                                           visits_to_rubbishpile=metadata_wo_col1['visits_to_rubbishpile'],
                                           nb_interactions_queen=metadata_wo_col1['nb_interaction_queen'])
    df_datax_train = df_datax_train.dropna()
    datax_train = df_datax_train.to_numpy()

    df_datay_train = pd.DataFrame().assign(group_period1=metadata_wo_col1[f"group_period{period}"])
    df_datay_train = df_datay_train.dropna()
    datay_train = df_datay_train.to_numpy()
    datay_train = datay_train.reshape(datay_train.shape[0])

    return datax_train, datay_train


def testset(col, period, metadata):
    metadata_col1 = metadata[metadata['colony_act'] == col] #on teste sur la colonie 1

    df_datax_test = pd.DataFrame().assign(nb_foraging_events=metadata_col1["nb_foraging_events"],
                                          visits_to_brood=metadata_col1["visits_to_brood"],
                                          visits_to_nest_entrance=metadata_col1['visits_to_nest_entrance'],
                                          visits_to_rubbishpile=metadata_col1['visits_to_rubbishpile'],
                                          nb_interactions_queen=metadata_col1['nb_interaction_queen'])
    df_datax_test = df_datax_test.dropna()
    datax_test = df_datax_test.to_numpy()

    df_datay_test = pd.DataFrame().assign(group_period1=metadata_col1[f"group_period{period}"])
    df_datay_test = df_datay_test.dropna()
    datay_test = df_datay_test.to_numpy()
    datay_test = datay_test.reshape(datay_test.shape[0])

    return datax_test, datay_test


def crossvalidation(clf, metadata, val='test'):
    accuracy = []
    precision = []
    recall = []
    for col in range(1,7):
        datax_train, datay_train = trainset(col, 1, metadata)
        datax_test, datay_test = testset(col, 1, metadata)
        clf.fit(datax_train, datay_train)
        if val == 'test':
            yhat = clf.predict(datax_test)
            accuracy.append(accuracy_score(datay_test, yhat))
            precision.append(precision_score(datay_test, yhat, average='micro'))
            recall.append(recall_score(datay_test, yhat, average='micro'))

        else:
            yhat = clf.predict(datax_train)
            accuracy.append(accuracy_score(datay_train, yhat))
            precision.append(precision_score(datay_train, yhat, average='micro'))
            recall.append(recall_score(datay_train, yhat, average='micro'))

    return accuracy, precision, recall

