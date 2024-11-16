import pandas as pd
import numpy as np
import sys

DIST_F = sys.argv[1]
SPECIES_DF = sys.argv[2]
OUTPUT_CSV = sys.argv[3]

def main():
    dist_matrix = pd.read_csv(DIST_F, index_col=0)
    dist_matrix.index = dist_matrix.index.astype(int)
    dist_matrix.columns = dist_matrix.columns.astype(int)

    species_df = pd.read_csv(SPECIES_DF)
    species_df['node'] = species_df['node'].astype(int)
    species_dict = {}
    for _, row in species_df.iterrows():
        species_dict[row['node']] = set(row['species'].split(';'))

    score = multi_label_silhouette(dist_matrix, species_dict)
    print(f"Silhouette Score: {score}")

def multi_label_silhouette(dist_matrix, species_dict):
    """
    Calculate a silhouette-like score for multi-label clusters using precomputed pairwise distances.
    
    Parameters:
    - dist_matrix (pd.DataFrame): Square matrix of pairwise distances with nodes as both index and columns.
    - species_dict (dict): Dictionary mapping node to a set of species (multiple species separated by semicolon).
    
    Returns:
    - float: The silhouette-like score.
    """

    nodes = dist_matrix.index
    scores = []

    # Precompute species membership mask for each node
    species_masks = {node: {other_node: bool(species_dict[node] & species_dict[other_node]) 
                           for other_node in nodes if node != other_node} for node in nodes}

    for node in nodes:
        # Intra-species distances (a(i)): Nodes sharing at least one species
        intra_distances = [dist_matrix.loc[node, other_node] 
                           for other_node in nodes if species_masks[node][other_node]]
        a_i = np.mean(intra_distances) if intra_distances else 0

        # Inter-species distances (b(i)): Nodes with no shared species
        inter_distances = [dist_matrix.loc[node, other_node] 
                           for other_node in nodes if not species_masks[node][other_node]]
        b_i = np.mean(inter_distances) if inter_distances else np.inf

        # Silhouette score for this node
        s_i = (b_i - a_i) / max(a_i, b_i) if a_i != 0 or b_i != np.inf else 0
        scores.append(s_i)

    return np.mean(scores)
