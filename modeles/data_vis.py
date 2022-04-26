from loaddata import load_data
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


def interaction_ant2ant(df1, df2, distance, time):
    """
    Calcule le nombre d'interactions entre deux fourmis
    input : df1 (resp df2) -> dataframe de la fourmis 1 (resp 2)
            time -> temps entre deux instants pour lequel on considère une interaction
            distance -> distance pour laquelle on considère une interaction
    output : nb_interactions : int
    """
    nb_interactions = 0
    for index_df1, row_df1 in df1.iterrows():
        for index_df2, row_df2 in df2.iterrows():
            t1 = row_df1["time"]
            t2 = row_df2["time"]
            if abs(t1 - t2) <= time:
                dist_t1_t2 = np.sqrt((row_df1['x'] - row_df2['x']) ** 2 + (row_df1['y'] - row_df2['y']) ** 2)
                if dist_t1_t2 <= distance:
                    nb_interactions += 1
    return nb_interactions


def ant_id2node_id(ant_ids):
    """
    Crée un dictionnaire permettant de garder l'id des fourmis et de les associer à un id de noeud du graphe/ rang de matrice
    input : ant_ids : set -> ensemble des id des fourmis
    output : node_ids : dictionnaire -> key=ant_id , value=node_id
    """
    node_ids = dict()
    cpt = 0
    for i in ant_ids:
        node_ids[i] = cpt
        cpt += 1
    return node_ids


def interaction_mat(distance, time, df):
    """
    Creation de matrice de comptage du nombre d'interactions
    input:  time -> temps entre deux instants pour lequel on considère une interaction
            distance -> distance pour laquelle on considère une interaction
            df -> dataframe représentant les instants d'un film
    output: mat_interactions -> matrice triangulaire du nombre d'interactions entre les fourmis
    """
    ant_ids = set(df['ant_id'])
    dict_ids = ant_id2node_id(ant_ids)
    n = len(ant_ids)
    mat_interactions = np.zeros((n, n))
    list_df_ants = []

    for i in ant_ids:
        list_df_ants.append(df[df['ant_id'] == i])

    for i in range(len(list_df_ants) - 1):
        for j in range(i + 1, len(list_df_ants)):
            l = dict_ids[list(list_df_ants[i]['ant_id'])[0]]
            k = dict_ids[list(list_df_ants[j]['ant_id'])[0]]
            val = interaction_ant2ant(list_df_ants[i], list_df_ants[j], distance, time) + 1
            mat_interactions[l][k] = val
            mat_interactions[k][l] = val
    return mat_interactions


def mat2graph(mat,m):
    """
    Cretion du graphe correspondant à la matrice mat et à la video numero m
    """
    rows, cols = np.where(mat > 0)
    edges = zip(rows.tolist(), cols.tolist())
    weighted_edges = []
    for r, c in edges:
        w = mat[r,c]
        if w != 1:
            weighted_edges.append((r,c,w))
    nodes = np.arange(np.shape(mat)[0])

    gr = nx.Graph()
    gr.add_nodes_from(nodes)
    gr.add_weighted_edges_from(weighted_edges)
    dict_labels = ant_id2node_id(nodes)

    plt.figure()
    ax = plt.gca()
    ax.set_title(f"Graphe d'intéractions pour le film {m}")
    pos = nx.spring_layout(gr, k=1/np.sqrt(len(nodes)/4))
    edge_labels = nx.get_edge_attributes(gr, 'weight')
    nx.draw(gr, node_size=500, labels=dict_labels, with_labels=True, ax=ax, pos=pos)
    nx.draw_networkx_edge_labels(gr, edge_labels=edge_labels, pos=pos)
    plt.savefig(f'out/graphe_interactions_m{m}.pdf')
    plt.show()
    return gr

#todo finir la fonction
def viz_traj(df):
    ant_ids = set(df['ant_id'])
    list_df_ants = []
    for i in ant_ids:
        df_ant = df[df['ant_id'] == i]
        plt.plot(list(df_ant['x']), list(df_ant['y']), color=f'#77a{str(i).zfill(3)}')
    plt.show()

if __name__ == '__main__':
    data = load_data()
    viz_traj(data[0])
    # for i in range(len(data)):
    #     mat = interaction_mat(100, 10, data[i])
    #     print(f"Matrice du film {i+1}\n", mat)
    #     mat2graph(mat, i+1)
