from sklearn.metrics import accuracy_score, mutual_info_score, rand_score, homogeneity_score, completeness_score, fowlkes_mallows_score
from itertools import permutations
import numpy as np
from sklearn.cluster import SpectralClustering
import pandas as pd

def acc_score(groups, pred_groups):
    """
    Calcul du score d'accuracy et renvoie les prédictions modifiées avec 0=F, 1=C et 2=N
    input:  groups -> liste des labels des groupes (ground truth)
            pred_groups -> liste des labels prédits
    output: score_res -> score d'accuracy
            yhat_mod -> liste des prédictions modifiées
    """
    score_res = 0
    yhat_mod = []
    for ind_pred in permutations('012', 3):
        ind_pred = [int(i) for i in list(ind_pred)]
        corresp_groups = dict(zip([0,1,2], list(ind_pred)))
        pred_groups_mod = [corresp_groups[g] for g in pred_groups]
        score = accuracy_score(groups, pred_groups_mod)
        if score > score_res:
            score_res = score
            yhat_mod = pred_groups_mod

    return score_res, yhat_mod


def df2mat(colonies, days, metadata, data, queen=False):
    """
    Retourne les matrices du comptage du nombre d'interactions pour les jours days des colonies colonies à partir des dataframes
    input:  colonies -> liste des numeros des colonies
            days -> liste de numeros des jours
            metadata -> datdframe avec (entre autres) les labels du groupe de chaque fourmi
            data -> liste de liste des dataframes représentant les matrices de comptages des interactions selon une colonie et un jour
            queen -> prendre en compte la reine ou non
    output: matrices -> liste des matrices
            ground_truth -> liste des dictionnaire Ant_ID : num_groupe
            list_ants -> liste des Ant_ID des fourmis de chaque matrice (ordre correspondant aux rangs de la matrice (rang[0] = anst[0]))
    """
    matrices = []
    ground_truth = []
    list_ants = []

    for c in colonies:
        df_by_col = metadata[metadata['colony_act'] == c]
        for d in days:
            df_by_day = data[c - 1][d - 1]
            ants = (df_by_day.columns[1::]).tolist()
            num_period = int((d - 1.1) / 10) + 1    #groupe différent pour chaque période (1 période = 10 jours)

            if not queen:   #on supprime la reine de la dataframe
                queen_id = list((df_by_col[df_by_col[f'group_period{num_period}'] == 'Q']['Ant_ID']))
                if queen_id[0] in ants:
                    df_by_day = df_by_day.drop(columns=queen_id)
                    i = df_by_day.index[df_by_day['Unnamed: 0'] == queen_id[0]].tolist()
                    df_by_day = df_by_day.drop(i)
                    ants.remove(queen_id[0])

            mat = np.delete(df_by_day.to_numpy(), 0, axis=1)
            matrices.append(mat)
            list_ants.append(ants)

            #création du dictionnaire de labels des fourmis
            y_true = dict()
            for a in (df_by_col[df_by_col[f'group_period{num_period}'] == 'F'])['Ant_ID']:
                if a in ants:   #si la fourmi est bien enregistrée le jour qu'on traite
                    y_true[a] = 0
            for a in (df_by_col[df_by_col[f'group_period{num_period}'] == 'C'])['Ant_ID']:
                if a in ants:
                    y_true[a] = 1
            for a in (df_by_col[df_by_col[f'group_period{num_period}'] == 'N'])['Ant_ID']:
                if a in ants:
                    y_true[a] = 2
            if queen:
                for a in (df_by_col[df_by_col[f'group_period{num_period}'] == 'Q'])['Ant_ID']:
                    if a in ants:
                        y_true[a] = 3   #on label la reine 3
            ground_truth.append(y_true)

    return matrices, ground_truth, list_ants


def clustering(matrices, ground_truth, list_ants, scoring='acc'):
    """
    Spectral clustering depuis les matrices de comptage des interactions
    input:  matrices -> liste des matrices
            ground_truth -> liste des dictionnaire Ant_ID : num_groupe
            list_ants -> liste des Ant_ID des fourmis de chaque matrice (ordre correspondant aux rangs de la matrice (rang[0] = anst[0]))
    output: scores -> liste des scores d'accuracy des clustering
            predictions -> liste des dictionnaires de prédictions Ant_ID : num groupe
    """
    predictions = []
    df_scores = pd.DataFrame(columns=['accuracy', 'mutual information', 'rand index', 'homogeneity', 'completeness', 'fmi'])

    for mat, y_true, ants in zip(matrices, ground_truth, list_ants):
        mat = mat + np.ones((mat.shape[0], mat.shape[1])) #l'algo de sklearn requiert un graphe complet
        #clustering en 3 groupes -> F, C, N
        clustering = SpectralClustering(n_clusters=3,assign_labels='discretize',affinity='precomputed')
        yhat = clustering.fit_predict(mat)
        y_pred = dict(zip(ants, yhat))
        y_pred = dict(sorted(y_pred.items(), key=lambda item: item[0]))
        y_true = dict(sorted(y_true.items(), key=lambda item: item[0]))

        score_acc, y_pred_sort = acc_score(list(y_true.values()), list(y_pred.values()))
        predictions.append(dict(zip(ants, y_pred_sort)))


        df_scores.loc[len(df_scores.index)] = [score_acc, mutual_info_score(list(y_true.values()), list(y_pred.values())),
                                               rand_score(list(y_true.values()), list(y_pred.values())),
                                               homogeneity_score(list(y_true.values()), list(y_pred.values())),
                                               completeness_score(list(y_true.values()), list(y_pred.values())),
                                               fowlkes_mallows_score(list(y_true.values()), list(y_pred.values()))]

    return df_scores, predictions
