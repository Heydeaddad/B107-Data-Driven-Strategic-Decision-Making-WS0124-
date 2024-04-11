import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict # for handling missing data


df = pd.read_excel("path to trimmed") 
hashtags_map = defaultdict(list)  # default value is []
video_hashtags = defaultdict(set)  # default value is {}


for index, row in df.iterrows():
    video_id = row['id']
    for i in range(2):  # we have two hashtags specified to each video
        hashtag_key = f'hashtags/{i}/name'
        if pd.notna(row[hashtag_key]): # checking existence
            hashtag = row[hashtag_key].strip().lower()  # we also need to be not case-sensitive
            hashtags_map[hashtag].append(video_id)  # adding hashtags as keys
            video_hashtags[video_id].add(hashtag)  # same


edges = set() # defining set for edges
for hashtag, videos in hashtags_map.items():
    for i in range(len(videos)): # going through each ID for the current hashtag
        for j in range(i + 1, len(videos)):
            edge = frozenset([videos[i], videos[j]]) # using frozenset to have unique edges
            edges.add(edge)


edges = [tuple(e) for e in edges if len(e) == 2]


G = nx.Graph() # Create the graph

G.add_edges_from(edges)





# original network
original_clustering_coefficient = 0.7967911642366363
original_density = 0.07143362664842294
original_average_degree = 62.36155606407323
num_nodes = len(G.nodes())
average_degree = int(original_average_degree / 2)  # for use in WS model where each node is connected to k nearest neighbors

# Erdős-Rényi 
p = original_density  # probability of edge creation
er_graph = nx.erdos_renyi_graph(n=num_nodes, p=p)
er_clustering_coefficient = nx.average_clustering(er_graph)
er_density = nx.density(er_graph)

# Barabási-Albert 
m = average_degree  # number of edges to attach from a new node to existing nodes
ba_graph = nx.barabasi_albert_graph(n=num_nodes, m=m)
ba_clustering_coefficient = nx.average_clustering(ba_graph)
ba_density = nx.density(ba_graph)

# Watts-Strogatz 
k = average_degree * 2  # each node is connected to k nearest neighbors in ring topology
beta = 0.1  # probability of rewiring each edge
ws_graph = nx.watts_strogatz_graph(n=num_nodes, k=k, p=beta)
ws_clustering_coefficient = nx.average_clustering(ws_graph)
ws_density = nx.density(ws_graph)


comparison = {
    'Original': {
        'Clustering Coefficient': original_clustering_coefficient,
        'Density': original_density,
    },
    'ER': {
        'Clustering Coefficient': er_clustering_coefficient,
        'Density': er_density,
    },
    'BA': {
        'Clustering Coefficient': ba_clustering_coefficient,
        'Density': ba_density,
    },
    'WS': {
        'Clustering Coefficient': ws_clustering_coefficient,
        'Density': ws_density,
    }
}

print(comparison)
