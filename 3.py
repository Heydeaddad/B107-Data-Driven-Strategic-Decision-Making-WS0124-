import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict # for handling missing data


df = pd.read_excel("C:\\Users\\Oleg\\OneDrive\\Рабочий стол\\Новая папка\\trimmed_dataset.xlsx")  # file location and reading
hashtags_map = defaultdict(list)  # default value is []
video_hashtags = defaultdict(set)  # default value is {}

# Populate the maps
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


degree_sequence = [G.degree(node) for node in G.nodes()]

# Degree Distribution (Histogram)
plt.figure(figsize=(8, 6))
plt.hist(degree_sequence, bins=50)
plt.title('Degree Distribution')
plt.xlabel('Degree')
plt.ylabel('Number of Nodes')
plt.show()

# Degree Distribution on a Log-Log scale
degree_counts = defaultdict(int)
for degree in degree_sequence:
    degree_counts[degree] += 1

# Prepare data for log-log plot
degrees = np.array(list(degree_counts.keys()))
counts = np.array(list(degree_counts.values()))

# Filter out degrees with 0 counts to avoid log(0)
degrees = degrees[counts > 0]
counts = counts[counts > 0]

log_degrees = np.log(degrees)
log_counts = np.log(counts)

# Plotting
plt.figure(figsize=(8, 6))
plt.plot(log_degrees, log_counts, 'bo', markersize=5)
plt.title('Degree Distribution on Log-Log Scale')
plt.xlabel('Log(Degree)')
plt.ylabel('Log(Number of Nodes)')
plt.grid(True)
plt.show()