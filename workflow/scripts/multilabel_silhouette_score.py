from sklearn.metrics import silhouette_score
import pandas as pd
import numpy as np
import sys

# DIST_F = sys.argv[1]
# SPECIES_DF = sys.argv[2]
DIST_F = "workflow/out/pairwise_distances/sample_1_0_02_30Lw30Nw1.0p0.1q20k_pairwiseDistances.csv"
# SPECIES_DF = "workflow/out/taxonomy/pract_nodes_by_species_multilabel.csv"
SPECIES_DF = "workflow/out/taxonomy/sample_1_0_02_nodes_by_species_multilabel.csv"

# OUTPUT_CSV = sys.argv[3]

def main():
    dist_matrix = pd.read_csv(DIST_F, index_col=0)
    dist_matrix.index = dist_matrix.index.astype(int)
    dist_matrix.columns = dist_matrix.columns.astype(int)

    species_df = pd.read_csv(SPECIES_DF)
    species_df['node'] = species_df['node'].astype(int)
    species_dict = {}
    for _, row in species_df.iterrows():
        species_dict[row['node']] = set(row['species'].split(';'))

    # Filter the distance matrix and species_dict to only include nodes that are in species_df
    # species_nodes = set(species_df['nodes'])
    species_nodes = set(species_dict.keys())
    print("n nodes in species dict: " + str(len(species_nodes)))
    # print(species_nodes)

    dist_nodes = dist_matrix.index.to_list() # Nodes in dist_matrix
    # print(dist_nodes[0:5])
    print("n nodes in dist matrix before filtering: " + str(len(dist_nodes)))

    # Find the common nodes
    dist_nodes = set(dist_nodes)
    common_nodes = dist_nodes.intersection(species_nodes)

    print("n nodes in both: " + str(len(common_nodes)))

    filtered_species_dict = {node: species_dict[node] for node in common_nodes}

    print("n nodes in species dict after filtering:" + str(len(filtered_species_dict.keys())))

    # Filter the distance matrix to only include rows and columns for nodes in species_df
    filtered_dist_matrix = dist_matrix.loc[dist_matrix.index.intersection(common_nodes), 
                                  dist_matrix.columns.intersection(common_nodes)]
    
    filtered_dist_file = "workflow/out/pairwise_distances/pract_pairwiseDistances.csv"
    dist_matrix.to_csv(filtered_dist_file)
    
    print("n nodes in dist matrix after filtering: " + str(len(filtered_dist_matrix.columns.to_list())))

    # print("nodes in either set but not in both: " + str(species_nodes.symmetric_difference(set(dist_matrix.columns.to_list()))))

    
    score = multi_label_silhouette(filtered_dist_matrix, filtered_species_dict)
    print(f"Silhouette Score: {score}")

    # Validation for nodes belonging to one species
    validate_silhouette_score(filtered_dist_matrix, filtered_species_dict)

def multi_label_silhouette(dist_matrix, species_dict):
    """
    Calculate a silhouette-like score for multi-label clusters using precomputed pairwise distances.
    
    Parameters:
    - dist_matrix (pd.DataFrame): Square matrix of pairwise distances with nodes as both index and columns.
    - species_dict (dict): Dictionary mapping node to a set of species (multiple species separated by semicolon).
    
    Returns:
    - float: The silhouette-like score.
    """

    # Check if the nodes in dist_matrix and species_dict match
    dist_nodes = set(dist_matrix.index)
    species_nodes = set(species_dict.keys())

    # Find nodes that are in one set but not the other
    missing_in_dist = species_nodes - dist_nodes  # Species nodes not in dist_matrix
    missing_in_species = dist_nodes - species_nodes  # Dist_matrix nodes not in species_dict

    # If there are any mismatches, print them in a readable way
    if missing_in_dist or missing_in_species:
        print(f"Error: Mismatch between nodes in dist_matrix and species_dict.")
        
        if missing_in_dist:
            print(f"Nodes in species_dict but not in dist_matrix: {list(missing_in_dist)[:10]}... ({len(missing_in_dist)} total)")
        
        if missing_in_species:
            print(f"Nodes in dist_matrix but not in species_dict: {list(missing_in_species)[:10]}... ({len(missing_in_species)} total)")
        
        return None  # Or raise an exception if you prefer

    nodes = dist_matrix.index.to_list()
    print("n nodes:" + str(len(nodes)))
    scores = []

    # Precompute species membership mask for each node
    # species_masks = {node: {other_node: bool(species_dict[node] & species_dict[other_node]) 
    #                        for other_node in nodes if node != other_node} for node in nodes}
    
    # species_masks = {node: {other_node: bool(species_dict.get(node, set()) & species_dict.get(other_node, set())) 
    #                        for other_node in nodes if node != other_node} 
    #                  for node in nodes}

    for node in nodes:
        # Intra-species distances (a(i)): Nodes sharing at least one species
        intra_distances = [
            dist_matrix.loc[node, other_node] 
            for other_node in nodes if species_dict[node] & species_dict[other_node]
        ]
        a_i = np.mean(intra_distances) if intra_distances else 0

        # Inter-species distances (b(i)): Nodes with no shared species
        inter_distances = [
            dist_matrix.loc[node, other_node] 
            for other_node in nodes if not species_dict[node] & species_dict[other_node]
        ]
        b_i = np.mean(inter_distances) if inter_distances else np.inf

        # Silhouette score for this node
        s_i = (b_i - a_i) / max(a_i, b_i) if a_i != 0 or b_i != np.inf else 0
        # print(f"Silhouette score for node {node}: {s_i}")
        scores.append(s_i)

    return np.mean(scores)

def validate_silhouette_score(dist_matrix, species_dict):
    # Get nodes that belong to exactly one species
    single_species_nodes = [node for node, species in species_dict.items() if len(species) == 1]

    if not single_species_nodes:
        print("No nodes belong to exactly one species.")
        return

    print(f"Validating silhouette score for nodes with a single species: {len(single_species_nodes)} nodes.")

    # Create a submatrix of distances for nodes that belong to exactly one species
    sub_dist_matrix = dist_matrix.loc[single_species_nodes, single_species_nodes]

    # Assign the single species label for all these nodes (since they belong to only one species)
    labels = [next(iter(species_dict[node])) for node in single_species_nodes]  # Get the first species label for each node

    # Calculate silhouette score using sklearn for validation
    sklearn_score = silhouette_score(sub_dist_matrix, labels)
    print(f"Silhouette Score from sklearn for single-species nodes: {sklearn_score}")

    # Calculate silhouette score using your custom method for validation
    custom_score = multi_label_silhouette(sub_dist_matrix, {node: species_dict[node] for node in single_species_nodes})
    print(f"Custom Silhouette Score for single-species nodes: {custom_score}")

    # Compare the scores
    if np.isclose(sklearn_score, custom_score, atol=1e-6):
        print("Validation successful: The silhouette scores match.")
    else:
        print(f"Validation failed: The silhouette scores do not match (sklearn: {sklearn_score}, custom: {custom_score}).")


if __name__ == '__main__':
    main()