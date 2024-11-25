import pandas as pd
import numpy as np
import random

DIST_F = "workflow/out/pairwise_distances/sample_1_0_02_30Lw50Nw1.0p1.0q60k_pairwiseDistances.csv"
SPECIES_DF = "workflow/out/taxonomy/pract_nodes_by_species_multilabel.csv"
OUTPUT_CSV = "workflow/out/clustering_accuracy/sample_1_0_02_30Lw50Nw1.0p1.0q60k_node_silhouetteScores.csv"

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
    dist_nodes = dist_matrix.index.to_list() # Nodes in dist_matrix

    # Find the common nodes
    dist_nodes = set(dist_nodes)

    ### SAMPLING FOR PRACT/TROUBLESHOOTING
    common_nodes = set(dist_matrix.index).intersection(species_dict.keys())

    sample_size = len(common_nodes)
    sampled_nodes = random.sample(list(common_nodes), sample_size)

    filtered_species_dict = {node: species_dict[node] for node in sampled_nodes}
    filtered_dist_matrix = dist_matrix.loc[sampled_nodes, sampled_nodes]

    node_scores = multi_label_silhouette(filtered_dist_matrix, filtered_species_dict)

    scores_df = pd.DataFrame(list(node_scores.items()), columns=['node', 'score'])
    scores_df.to_csv(OUTPUT_CSV, index=False)


def multi_label_silhouette(dist_matrix, species_dict):
    nodes = dist_matrix.index.to_list()
    node_scores = {}

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

        s_i = (min_b_i - a_i) / max(a_i, min_b_i) if a_i != 0 and min_b_i != 0 else 1
        node_scores[node] = s_i

    return node_scores

if __name__ == '__main__':
    main()