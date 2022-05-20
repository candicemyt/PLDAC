import random

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


def mat2graph(mat, titre, plot=True):
    """
    Creation du graphe correspondant à la matrice mat et à titre
    """
    rows, cols = np.where(mat > 0)
    edges = zip(rows.tolist(), cols.tolist())
    weighted_edges = []
    for r, c in edges:
        w = mat[r, c]
        if w != 1:
            weighted_edges.append((r, c, w))
    nodes = np.arange(np.shape(mat)[0])

    gr = nx.Graph()
    gr.add_nodes_from(nodes)
    gr.add_weighted_edges_from(weighted_edges)
    if plot:
        plot_graph(gr, titre, show=True)
    return gr


def plot_graph(gr, titre, show=False, self_loop=False, edge_labels=False):
    """
    Plot et enregistrement de la visualisation du graphe gr
    """
    if not self_loop:
        gr.remove_edges_from(nx.selfloop_edges(gr))
    plt.figure(figsize=(10,10))
    ax = plt.gca()
    ax.set_title(f"Graphe d'intéractions pour {titre}")
    pos = nx.spring_layout(gr, k=1/np.sqrt(len(gr.nodes)/4))
    dict_edge_labels = nx.get_edge_attributes(gr, 'weight')
    dict_edge_labels = {k : round(v,2) for k,v in dict_edge_labels.items()}
    if edge_labels:
        nx.draw_networkx_edge_labels(gr, edge_labels=dict_edge_labels, pos=pos)
    for edge in gr.edges(data='weight'):
        nx.draw_networkx_edges(gr, pos, edgelist=[edge], width=edge[2] / np.sum(list(dict_edge_labels.values())) * 20)
    nx.draw(gr, node_size=400, with_labels=True, labels={0:'F', 1:'C', 2:'N', 3:'Q'}, ax=ax, pos=pos)
    plt.savefig(f'out/graphe_interactions/graphe_interactions_{titre}.pdf')
    if show:
        plt.show()


def viz_traj(df, titre, show=False):
    """
    Visualisation de trajectoires pour le dataset1
    """
    ant_ids = set(df['ant_id'])
    dict_ids = ant_id2node_id(ant_ids)
    legends = []
    plt.figure()
    for i in ant_ids:
        ax = plt.gca()
        df_ant = df[df['ant_id'] == i]
        legends.append(ax.plot(list(df_ant['x']), list(df_ant['y']), color=f'#{str(random.randint(1, 999999)).zfill(6)}', label=dict_ids[i])[0])
    ax.set_title(f"Trajectoires pour {titre}")
    ax.legend(handles=legends)
    plt.savefig(f'out/trajectoires/trajectoires_{titre}.pdf')
    if show:
        plt.show()


if __name__ == '__main__':
    data = load_data('dataset1')
    for i in range(len(data)):
        mat = interaction_mat(100, 10, data[i])
        #print(f"Matrice du film {i+1}\n", mat)
        mat2graph(mat, f'video {i + 1}')
        viz_traj(data[i], f'video {i+1}')
    _, data = load_data('dataset2')
    mat = np.delete(data[0][0].to_numpy(), 0, axis=1)
#%%
    mat2graph(mat, 'dataset2_col1_day1')