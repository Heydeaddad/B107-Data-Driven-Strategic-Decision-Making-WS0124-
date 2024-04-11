import pandas as pd

# Load your dataset
df = pd.read_excel("C:\\Users\\Oleg\\OneDrive\\Рабочий стол\\Новая папка\\trimmed_dataset.xlsx")  # Make sure to update this path to the location of your dataset

# Count unique video IDs
num_nodes = df['id'].nunique()

print("Number of nodes (unique video IDs):", num_nodes)