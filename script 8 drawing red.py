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

# Add likes as an attribute 
diggCount_dict = pd.Series(df.diggCount.values,index=df.id).to_dict()
nx.set_node_attributes(G, diggCount_dict, 'diggCount')

# Drawing
plt.figure(figsize=(12, 12))
ax = plt.gca()
pos = nx.spring_layout(G)

# setting up color change
digg_counts = np.array([data['diggCount'] for node, data in G.nodes(data=True)])
norm = Normalize(vmin=digg_counts.min(), vmax=digg_counts.max())
cmap = plt.cm.Reds
sm = ScalarMappable(norm=norm, cmap=cmap)

# Apply the colormap 
node_colors = [sm.to_rgba(data['diggCount']) for node, data in G.nodes(data=True)]

nx.draw_networkx_edges(G, pos, alpha=0.2, ax=ax)
nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=20, ax=ax)

# Create a colorbar
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.05)
plt.colorbar(sm, cax=cax, label='Digg Count')

ax.set_title('Network Visualization by Digg Count')
plt.axis('off')
plt.show()
