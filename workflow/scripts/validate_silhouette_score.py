from sklearn.metrics import silhouette_score, silhouette_samples
import pandas as pd
import numpy as np
import sys
import random

# DIST_F = sys.argv[1]
# SPECIES_DF = sys.argv[2]
DIST_F = "workflow/out/pairwise_distances/sample_1_0_02_30Lw30Nw1.0p0.1q20k_pairwiseDistances.csv"
# SPECIES_DF = "workflow/out/taxonomy/pract_nodes_by_species_multilabel.csv"
SPECIES_DF = "workflow/out/taxonomy/sample_1_0_02_nodes_by_species_multilabel.csv"

# OUTPUT_CSV = sys.argv[3]

# Load the species DataFrame (adjust file path as needed)
species_df = pd.read_csv(SPECIES_DF)

# Filter for rows where nodes have exactly one species
single_species_df = species_df[species_df['species'].str.count(';') == 0]

# Check how many nodes have only one species
print(f"Number of nodes with a single species: {len(single_species_df)}")

# Load the pairwise distance matrix (adjust file path as needed)
dist_matrix = pd.read_csv(DIST_F, index_col=0)

# Ensure that the 'node' column in species_df and the indices/columns of dist_matrix are of the same type
single_species_df['node'] = single_species_df['node'].astype(int)
dist_matrix.index = dist_matrix.index.astype(int)
dist_matrix.columns = dist_matrix.columns.astype(int)

# Find the common nodes between the distance matrix and species dataframe
common_nodes = set(single_species_df['node']).intersection(dist_matrix.index)

# Filter the species DataFrame and distance matrix for these common nodes
filtered_species_df = single_species_df[single_species_df['node'].isin(common_nodes)]
filtered_dist_matrix = dist_matrix.loc[common_nodes, common_nodes]

# Check the filtered data
print(f"Filtered distance matrix size: {filtered_dist_matrix.shape}")
print(f"Filtered species dataframe size: {filtered_species_df.shape}")

# Get the labels (species) for each node
# Here we assume there's a single species per node (because we filtered for that)
labels = filtered_species_df['species'].values

# Convert the distance matrix to a NumPy array
sub_dist_matrix = filtered_dist_matrix.to_numpy()

# Calculate silhouette scores for each node
silhouette_vals = silhouette_samples(sub_dist_matrix, labels)

# Print silhouette score for each node
for node, score in zip(filtered_dist_matrix.index, silhouette_vals):
    print(f"Silhouette score for node {node}: {score}")

# Calculate the mean silhouette score
mean_silhouette_score = np.mean(silhouette_vals)
print(f"Mean Silhouette Score: {mean_silhouette_score}")