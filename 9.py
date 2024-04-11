import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
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

hashtag_popularity = {hashtag: len(videos) for hashtag, videos in hashtags_map.items()}

# Sort the hashtags by their popularity in descending order
sorted_hashtags = sorted(hashtag_popularity.items(), key=lambda x: x[1], reverse=True)

# Print the top 10 most popular hashtags
print("Top 10 Most Popular Hashtags:")
for hashtag, count in sorted_hashtags[:10]:  # Only get the first 10 items
    print(f"{hashtag}: {count} videos")