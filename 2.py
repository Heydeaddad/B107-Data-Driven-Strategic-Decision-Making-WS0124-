import pandas as pd

# Loading
df = pd.read_excel("path to trimmed")  

num_nodes = df['id'].nunique() # counting

print("Number of nodes (unique video IDs):", num_nodes)
