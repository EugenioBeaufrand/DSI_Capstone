from igraph import *
import pandas as pd
import random

g_df = pd.read_csv('../FullNetwork.csv')
g = Graph.DataFrame(g_df, directed=True)
e_count = g.ecount()
print('Number of edges:', e_count)
v_count = g.vcount()
print('Number of vertices:', v_count)
# vertex names
vseq = g.vs()
# maximum degree
print('Maximum degree:', g.maxdegree(vseq, mode='all', loops=True))

named_vertex_list = g.vs()["name"]
# calculate degree
gd = g.degree(vseq, mode='all')
vertex_degree = list(zip(named_vertex_list, gd))
pd.DataFrame(vertex_degree).to_csv('vertex_deg.csv', index=False)

# calculate raw betweenness centrality
gb = g.betweenness()
vertex_between = list(zip(named_vertex_list, gb))
pd.DataFrame(vertex_between).to_csv('vertex_bet_raw.csv', index=False)

# calculate normalized betweenness centrality
def normalize_betweenness(a):
    return (2 * a) / (v_count * v_count - 3 * v_count + 2)

gb_n = list(map(normalize_betweenness, gb))
vertex_between_n = list(zip(named_vertex_list, gb_n))
pd.DataFrame(vertex_between_n).to_csv('vertex_bet_norm.csv', index=False)

# calculate raw eigen centrality
g_ec_raw = g.eigenvector_centrality(directed=True, scale=False, weights=None, return_eigenvalue=False)
vertex_ec_raw= list(zip(named_vertex_list, g_ec_raw))
pd.DataFrame(vertex_ec_raw).to_csv('vertex_ec_raw.csv', index=False)

# calculate normalized eigen centrality
g_ec = g.eigenvector_centrality(directed=True, scale=True, weights=None, return_eigenvalue=False)
vertex_ec_scaled = list(zip(named_vertex_list, g_ec))
pd.DataFrame(vertex_ec_scaled).to_csv('vertex_ec_norm.csv', index=False)

# transitivity
gt = g.transitivity_local_undirected(vertices=None, mode='nan', weights=None)
vertex_trans = list(zip(named_vertex_list, gt))
pd.DataFrame(vertex_trans).to_csv('vertex_trans.csv', index=False)


# Subgraphs for plotting
sample_size = 50000
subgraph_vertex_list = [v.index for v in random.sample(list(vseq), sample_size)]
sg1 = Graph.subgraph(g, subgraph_vertex_list)
