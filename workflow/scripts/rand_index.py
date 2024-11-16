import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
from gensim.models import KeyedVectors
import os
import re
import sys
import csv

EMBEDDING_F = sys.argv[1]
SPECIES_F = sys.argv[2]
ARI_CSV = sys.argv[3]

file_name = os.path.basename(EMBEDDING_F)
pattern = r"(sample_\d+_\d+_\d+)_([0-9]+)Lw([0-9]+)Nw([0-9.]+)p([0-9.]+)q([0-9]+)k_walks.embeddings"
match = re.match(pattern, file_name)

if match:
    graph_id = match.group(1)
    walk_length = match.group(2)
    n_walks = match.group(3)
    p = match.group(4)
    q = match.group(5)
    dimensions = match.group(6)
else:
    print(f"Warning: Unable to extract details from filename {file_name}")
    graph_id = walk_length = n_walks = p = q = dimensions = None

# Load embeddings
embedding_kv = KeyedVectors.load(EMBEDDING_F, mmap='r')
embeddings_df = pd.DataFrame(embedding_kv.vectors, index=embedding_kv.key_to_index)

# Load species data
species_df = pd.read_csv(SPECIES_F)
species_df = species_df.drop(columns=[species_df.columns[0]])  # Drop unnamed column
species_df = species_df.set_index('node')
species_df.index = species_df.index.astype(str)
species_df = species_df[~species_df['species'].str.contains(';')]

# Ensure node IDs in embeddings match species data
embeddings_df.index = embeddings_df.index.astype(str)

# Perform k-means clustering
k = species_df['species'].nunique()
kmeans = KMeans(n_clusters=k, random_state=0)
embeddings_df['cluster'] = kmeans.fit_predict(embeddings_df)

# Merge embeddings with species labels
filtered_embeddings_df = embeddings_df.merge(species_df, left_index=True, right_index=True, how='left')

# Drop rows without species
filtered_embeddings_df = filtered_embeddings_df.dropna(subset=['species'])

# Extract ground truth and predicted labels
ground_truth_labels = filtered_embeddings_df['species'].values
predicted_labels = filtered_embeddings_df['cluster'].values

# Calculate Adjusted Rand Index
ari = adjusted_rand_score(ground_truth_labels, predicted_labels)

# Prepare result as a dictionary
result = {
    'embedding_file': file_name,
    'graph_id': graph_id,
    'walk_length': walk_length,
    'n_walks': n_walks,
    'p': p,
    'q': q,
    'dimensions': dimensions,
    'ari': ari,
    'num_clusters': k
}

# Append result to CSV file
file_exists = os.path.isfile(ARI_CSV)
with open(ARI_CSV, mode='a', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=result.keys())
    if not file_exists:
        writer.writeheader()
    writer.writerow(result)

print(f"Processed {EMBEDDING_F} with ARI: {ari}")