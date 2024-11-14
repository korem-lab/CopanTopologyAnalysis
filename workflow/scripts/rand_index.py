import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
from gensim.models import KeyedVectors
import os

EMBEDDING_F = "workflow/out/vectorization_model/embeddings/sample_1_0_02_80Lw50Nw1.0p1.0q60k_walks.embeddings"
SPECIES_F = "workflow/out/node_classification/sample_1_0_02_nodes_by_species.csv"

# Ensure files exist
if not os.path.isfile(EMBEDDING_F) or not os.path.isfile(SPECIES_F):
    raise FileNotFoundError("One or both input files are missing.")

# Load embeddings
embedding_kv = KeyedVectors.load(EMBEDDING_F, mmap='r')
embeddings_df = pd.DataFrame(embedding_kv.vectors, index=embedding_kv.key_to_index)

# Load species data
species_df = pd.read_csv(SPECIES_F)
species_df = species_df.drop(columns=[species_df.columns[0]])  # Drop unnamed column
species_df = species_df.set_index('node')
species_df.index = species_df.index.astype(str)

# Ensure node IDs in embeddings match species data
embeddings_df.index = embeddings_df.index.astype(str)
common_nodes = embeddings_df.index.intersection(species_df.index)

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

# Output the result
print(f"Adjusted Rand Index: {ari}")
