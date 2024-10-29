import numpy as np
import pandas as pd
from itertools import pairwise
import sys

DISTANCES_F = "workflow/out/pairwise_distances/copan_0_30Lw50Nw1.0p0.1q140k_pairwiseDistances.csv"
DEGREE_F = "workflow/out/node_classification/copan_0_node_degree_classification.csv"

def main():

    distance_matrix = pd.read_csv(DISTANCES_F, index_col=0)
    distance_matrix.columns = distance_matrix.columns.astype('int')
    degree_df = pd.read_csv(DEGREE_F)

    nodes = distance_matrix.index.tolist() # node names, not indeces
    # Convert to a NumPy array
    
    node_degree_map = dict(zip(degree_df['node'], degree_df['degree']))
    
    distance_degree_df = []

    # trying to iterate from the distance matrix, not the degree df
    for i, j in pairwise(nodes):  # iterate through all node combinations in the list of nodes. i and j are node names, not indeces

        degree_i = node_degree_map[i]
        degree_j = node_degree_map[j]

        try:
            distance_ij = distance_matrix.loc[i, j]  # Access distance by label
        except KeyError as e:
            print(f"KeyError: {e} for nodes ({i}, {j})")
            continue  # Skip this pair if nodes are not found
        
        # Append the information as a row to the data list
        distance_degree_df.append([i, degree_i, j, degree_j, distance_ij])

    # Convert to a DataFrame
    df = pd.DataFrame(distance_degree_df, columns=['node_i', 'degree_i', 'node_j', 'degree_j', 'distance'])

    df.to_csv(DEGREE_F, index=False)


if __name__ == '__main__':
    main()
