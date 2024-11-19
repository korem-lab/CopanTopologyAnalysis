from sklearn.metrics import silhouette_score, silhouette_samples
import pandas as pd
import numpy as np
import sys
import random


# DIST_F = sys.argv[1]
# SPECIES_DF = sys.argv[2]
# DIST_F = "workflow/out/pairwise_distances/sample_1_0_02_30Lw30Nw1.0p0.1q20k_pairwiseDistances.csv"
SPECIES_DF = "workflow/out/taxonomy/pract_nodes_by_species_multilabel.csv"
DIST_F = "workflow/out/pairwise_distances/pract_pairwiseDistances.csv"
# SPECIES_DF = "workflow/out/taxonomy/nodes_by_species_multilabel_pract.csv"

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
    species_nodes = set(species_dict.keys())
    print("n nodes in species dict: " + str(len(species_nodes)))

    dist_nodes = dist_matrix.index.to_list() # Nodes in dist_matrix
    print("n nodes in dist matrix before filtering: " + str(len(dist_nodes)))

    # Find the common nodes
    dist_nodes = set(dist_nodes)

    ### SAMPLING FOR PRACT/TROUBLESHOOTING
    common_nodes = set(dist_matrix.index).intersection(species_dict.keys())

    print("n nodes in both: " + str(len(common_nodes)))

    sample_size = 10
    sampled_nodes = random.sample(list(common_nodes), sample_size)

    print(f"Sampled nodes for testing: {sampled_nodes}")

    # Create the filtered species dictionary and distance matrix for the sampled nodes
    filtered_species_dict = {node: species_dict[node] for node in sampled_nodes}
    filtered_dist_matrix = dist_matrix.loc[sampled_nodes, sampled_nodes]

    print(filtered_dist_matrix)

    print("n nodes in species dict after filtering:" + str(len(filtered_species_dict.keys())))
    
    print("n nodes in dist matrix after filtering: " + str(len(filtered_dist_matrix.columns.to_list())))

    score = multi_label_silhouette(filtered_dist_matrix, filtered_species_dict)

    print(f"Silhouette Score: {score}")

    # filtered_species_df = species_df[species_df['node'].isin(common_nodes)]
    # Validation for nodes belonging to one species
    # validated_scores = validate_silhouette_score(filtered_dist_matrix, filtered_species_df)
    # sample_score = validated_scores[0]
    # overall_score = validated_scores[1]
    # print(f"Sklearn's Mean Sample Silhouette Score: {sample_score}")
    # print(f"Sklearn's Overall Silhouette Score: {overall_score}")

def multi_label_silhouette(dist_matrix, species_dict):

    nodes = dist_matrix.index.to_list()
    print("n nodes:" + str(len(nodes)))
    scores = []

    for node in nodes:
        # Intra-species distances (a(i)): Nodes sharing at least one species
        intra_distances = [
            dist_matrix.loc[node, other_node]
            for other_node in nodes
            if species_dict[node] & species_dict[other_node]
            and other_node != node
        ]

        a_i = np.mean(intra_distances) if intra_distances else 0

        # Inter-species distances (b(i)): Nodes with no shared species
        b_i_values = {}

        other_species = {species for species_list in species_dict.values()
                        for species in species_list} - species_dict[node]

        if other_species:
            for species in other_species:  # Iterate through each unique species in species_dict
                other_specie_nodes = [node for node in nodes if species in species_dict[node]]

                if other_specie_nodes:
                    # Calculate distances to nodes of different species
                    inter_distances = [
                        dist_matrix.loc[node, other_node]
                        for other_node in other_specie_nodes
                    ]
                    
                    # Compute the mean inter-cluster distance for the species
                    b_i_values[species] = np.mean(inter_distances) if inter_distances else 0

            # Find the minimum b_i value across all species
            min_b_i = min(b_i_values.values())
        
        else: 
            min_b_i = 0

        # Silhouette score for this node
        s_i = (min_b_i - a_i) / max(a_i, min_b_i) if a_i != 0 and min_b_i != 0 else 1

        print(f"Silhouette score for node {node}: {s_i}")
        scores.append(s_i)

    return np.mean(scores)

def validate_silhouette_score(dist_matrix, species_df):
    labels = species_df['species'].values

    # Convert the distance matrix to a NumPy array
    sub_dist_matrix = dist_matrix.to_numpy()

    # Calculate silhouette scores for each node
    silhouette_vals = silhouette_samples(sub_dist_matrix, labels, metric="precomputed")

    # Print silhouette score for each node
    for node, score in zip(dist_matrix.index, silhouette_vals):
        print(f"Validated silhouette score for node {node}: {score}")

    validated_score = silhouette_score(sub_dist_matrix, labels, metric="precomputed")

    # Calculate the mean silhouette score
    return np.mean(silhouette_vals), validated_score
    

if __name__ == '__main__':
    main()