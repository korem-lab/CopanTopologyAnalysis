import numpy as np
import pandas as pd
from itertools import combinations
import sys

DISTANCES_F = sys.argv[1]
TAX_F = sys.argv[2]
DISTANCE_DEGREE_F = sys.argv[3]
TAX_LEVEL = sys.argv[4]

def main():

    distance_matrix = pd.read_csv(DISTANCES_F, index_col=0)
    distance_matrix.columns = distance_matrix.columns.astype('int')
    species_map = load_species_map(TAX_F)

    nodes = distance_matrix.index.tolist() # node names, not indeces

    # filtered_nodes = [node for node in nodes if node in species_map]
    # Convert to a NumPy array
    
    distance_degree_df = []

    # trying to iterate from the distance matrix, not the degree df
    for i, j in combinations(nodes, 2):  # iterate through all node combinations in the list of nodes. i and j are node names, not indeces

        # species_i = species_map[i]
        # species_j = species_map[j]

        # Assign species; default to "No BLAST hit" if the node is not in species_map
        species_i = species_map.get(i, "No BLAST hit")
        species_j = species_map.get(j, "No BLAST hit")

        try:
            distance_ij = distance_matrix.loc[i, j]  # Access distance by label
        except KeyError as e:
            print(f"KeyError: {e} for nodes ({i}, {j})")
            continue  # Skip this pair if nodes are not found
        
        # Append the information as a row to the data list
        distance_degree_df.append([i, species_i, j, species_j, distance_ij])

    # Convert to a DataFrame
    df = pd.DataFrame(distance_degree_df, columns=['node_i', 'species_i', 'node_j', 'species_j', 'distance'])

    df.to_csv(DISTANCE_DEGREE_F, index=False)

def load_species_map(species_csv_file):
    """Load the node-to-species mapping from a CSV file using pandas."""
    df = pd.read_csv(species_csv_file)
    # Convert to dictionary (node -> species)
    species_map = dict(zip(df['node'].astype(int), df[TAX_LEVEL]))
    return species_map


if __name__ == '__main__':
    main()
