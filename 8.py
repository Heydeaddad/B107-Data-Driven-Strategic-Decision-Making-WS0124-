import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable  # Corrected import
from mpl_toolkits.axes_grid1 import make_axes_locatable


# Load the dataset
df = pd.read_excel("C:\\Users\\Oleg\\OneDrive\\Рабочий стол\\Новая папка\\trimmed_dataset.xlsx")

hashtags_map = defaultdict(list)
video_hashtags = defaultdict(set)

# Populate the maps with data from the DataFrame
for index, row in df.iterrows():
    video_id = row['id']
    for i in range(2):  # Adjust if you have more hashtags per video
        hashtag_key = f'hashtags/{i}/name'
        if pd.notna(row[hashtag_key]):
            hashtag = row[hashtag_key].strip().lower()
            hashtags_map[hashtag].append(video_id)
            video_hashtags[video_id].add(hashtag)

# Create a set for edges to ensure uniqueness
edges = set()
for hashtag, videos in hashtags_map.items():
    for i in range(len(videos)):
        for j in range(i + 1, len(videos)):
            edge = frozenset([videos[i], videos[j]])
            edges.add(edge)

# Convert edges set to a list of tuples for NetworkX
edges = [tuple(e) for e in edges if len(e) == 2]

# Create the graph and add edges
G = nx.Graph()
G.add_edges_from(edges)

# Add 'diggCount' as an attribute to each node in the graph
diggCount_dict = pd.Series(df.diggCount.values,index=df.id).to_dict()
nx.set_node_attributes(G, diggCount_dict, 'diggCount')

# Visualization
plt.figure(figsize=(12, 12))
ax = plt.gca()
pos = nx.spring_layout(G)

# Get the 'diggCount' values for normalization
digg_counts = np.array([data['diggCount'] for node, data in G.nodes(data=True)])
norm = Normalize(vmin=digg_counts.min(), vmax=digg_counts.max())
cmap = plt.cm.Reds
sm = ScalarMappable(norm=norm, cmap=cmap)

# Apply the colormap to the 'diggCount' values for each node
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