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

connected_components = list(nx.connected_components(G))

# Number of connected components
num_connected_components = len(connected_components)

# Largest connected component
largest_cc = max(connected_components, key=len)
largest_cc_size = len(largest_cc)

print(f"Number of connected components: {num_connected_components}")
print(f"Size of the largest connected component: {largest_cc_size}")

largest_cc_subgraph = G.subgraph(largest_cc)

largest_cc_subgraph = G.subgraph(largest_cc).copy()

# draw lcc
plt.figure(figsize=(12, 8))
# You can choose between different layouts, here we use the spring layout
pos = nx.spring_layout(largest_cc_subgraph)
nx.draw_networkx(largest_cc_subgraph, pos, with_labels=False, node_size=20, width=0.1)
plt.title('Largest Connected Component')
plt.axis('off')  # Turn off the axis numbers/lines
plt.show()

pos = nx.spring_layout(G)

# Draw whole
plt.figure(figsize=(15, 15))  # Set the size of the figure
nx.draw_networkx_nodes(G, pos, node_size=10)  # Draw the nodes
nx.draw_networkx_edges(G, pos, alpha=0.1)  # Draw the edges
plt.title('Network Visualization')
plt.axis('off')  # Hide the axes
plt.show()
