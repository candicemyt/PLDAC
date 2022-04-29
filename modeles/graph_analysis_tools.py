import networkx as nx
import numpy as np

def group_interactions(graph, groups, ants):
    """
    Retourne le graphe d'interactions entre chaque groupe de fourmis à partir du graphe d'intéractions entre fourmis
    input:  graph -> graphe d'intéractions entre fourmis
            groups -> dictionnaire Ant_ID : num_groupe
            ants -> liste des fourmis représentée sur le graphe
    """
    dict_ants = dict(zip(graph.nodes, ants))
    dict_weighted_egdes = dict()

    for (u, v) in graph.edges():
        edge = (groups[dict_ants[u]], groups[dict_ants[v]])
        if edge not in dict_weighted_egdes:     #le poids des arcs correspond au nombre d'interactions
            dict_weighted_egdes[edge] = 1
        else:
            dict_weighted_egdes[edge] += 1

    group_graph = nx.Graph()
    group_graph.add_nodes_from([0,1,2])
    weighted_edges = list(dict_weighted_egdes.items())
    weighted_edges = [(weighted_edges[i][0][0], weighted_edges[i][0][1], weighted_edges[i][1]) for i in range(len(weighted_edges))]
    group_graph.add_weighted_edges_from(weighted_edges)

    return group_graph


def add_queen(mat, pred, ants, metadata, day, col, df):
    """
    Ajoute la reine à mat, pred et ants
    input:  mat -> matrice d'interaction
            pred -> liste de predictions des groupes
            ants -> liste des Ant_ID correspondants aux prédictions
            metadata -> dataframe contenant toutes les infos sur le dataset
            day -> numero du jour d'enregistrement des interactions de la matrice mat
            col -> numero de la colonie d'enregistrement des interactions de la matrice mat
            df -> dataframe correspondant à la matrice d'interaction du jour day et de la colonie col
    output: mat -> matrice avec la reine ajoutée
            pred -> predictions avec la reine ajoutée
            ants -> liste des Ant_ID avec la reine ajoutée
    """
    num_period = int((day - 1.1) / 10) + 1
    df_by_col = metadata[metadata['colony_act'] == col]
    queen_id = list((df_by_col[df_by_col[f'group_period{num_period}'] == 'Q']['Ant_ID']))

    if queen_id:
        ants.append(queen_id[0])
        pred[queen_id[0]] = 4

        i = df.index[df['Unnamed: 0'] == queen_id[0]].tolist()
        df = df.drop(i)
        queen_row = np.array(df[queen_id[0]])
        queen_row = queen_row[:, np.newaxis]
        mat = np.hstack((mat, queen_row))
        queen_col = np.vstack((queen_row, np.zeros((1,1))))
        mat = np.vstack((mat, queen_col.T))
        return mat, pred, ants

    else:    #si aucune reine n'est enregistree pour ce jour et cette colonie on retourne des listes et dictionnaire vides
        print(f'Pas de reine enregistrée pour la colonie {col} et le jour {day}')
        return [], dict(), []