import numpy as np
import pandas as pd
from itertools import pairwise
import sys

DISTANCES_F = "workflow/out/pairwise_distances/copan_0_30Lw50Nw1.0p0.1q140k_pairwiseDistances.csv"
DEGREE_F = "workflow/out/node_classification/copan_0_node_degree_classification.csv"

def main():

    distance_matrix_df = pd.read_csv(DISTANCES_F, index_col=0, nrows=2, usecols=[0] + list(range(1, 3)))
    degree_df = pd.read_csv(DEGREE_F)

    nodes = distance_matrix_df.index.tolist() # node names, not indeces
    # Convert to a NumPy array
    distance_matrix = distance_matrix_df.values
    #print(combinations(nodes, 2))
    node_degree_map = dict(zip(degree_df['node'], degree_df['degree']))

    # # Create only unique pairs (i, j) of nodes and get the degree and distance for each pair
    distance_degree_df = []

    # trying to iterate from the distance matrix, not the degree df
    for i, j in nodes:  # iterate through all node combinations in the list of nodes. i and j are node names, not indeces

        print("i name:" + str(i))
        print("j name:" + str(j))

        degree_i = node_degree_map[i]
        degree_j = node_degree_map[j]

        print("i degree:" + str(degree_i))
        print("j degree:" + str(degree_j))

                # Attempt to access the distance
        try:
            distance_ij = distance_matrix_df.loc[i, j]  # Access distance by label
        except KeyError as e:
            print(f"KeyError: {e} for nodes ({i}, {j})")
            continue  # Skip this pair if nodes are not found
        
        # Append the information as a row to the data list
        distance_degree_df.append([i, degree_i, j, degree_j, distance_ij])


    # for i, j in combinations(range(len(degree_df)), 2):  # Only (i, j) where i < j

    #     print("i index:" + str(i))
    #     print("j index:" + str(j))

    #     node_i = degree_df['node'].iloc[i]
    #     node_j = degree_df['node'].iloc[j]

    #     print("i name:" + str(node_i))
    #     print("j name:" + str(node_j))

    #     degree_i = node_degree_map[node_i]
    #     degree_j = node_degree_map[node_j]

    #     print("i degree:" + str(degree_i))
    #     print("j degree:" + str(degree_j))
        
        # Attempt to access the distance
    # #     try:
    # #         distance_ij = distance_matrix_df.loc[node_i, node_j]  # Access distance by label
    # #     except KeyError as e:
    # #         print(f"KeyError: {e} for nodes ({node_i}, {node_j})")
    # #         continue  # Skip this pair if nodes are not found
        
    # #     Append the information as a row to the data list
    # #     distance_degree_df.append([node_i, degree_i, node_j, degree_j, distance_ij])

    # # Convert to a DataFrame
    # # df = pd.DataFrame(distance_degree_df, columns=['node_i', 'degree_i', 'node_j', 'degree_j', 'distance'])

    # # df.to_csv(DEGREE_F, index=False)


if __name__ == '__main__':
    main()
