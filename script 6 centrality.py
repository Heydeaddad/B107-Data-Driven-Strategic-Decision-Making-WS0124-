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


degree_centrality = nx.degree_centrality(G)

max_degree_node = max(degree_centrality, key=degree_centrality.get)
print(f"Node with highest degree centrality: {max_degree_node}")


betweenness_centrality = nx.betweenness_centrality(G)

max_betweenness_node = max(betweenness_centrality, key=betweenness_centrality.get)
print(f"Node with highest betweenness centrality: {max_betweenness_node}")


closeness_centrality = nx.closeness_centrality(G)

max_closeness_node = max(closeness_centrality, key=closeness_centrality.get)
print(f"Node with highest closeness centrality: {max_closeness_node}")
