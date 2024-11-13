import numpy as np
import pandas as pd
from itertools import combinations
import sys

DISTANCES_F = sys.argv[1]
TAX_F = sys.argv[2]
DISTANCE_DEGREE_F = sys.argv[3]
TAX_LEVEL = sys.argv[4]

def main():
    # Load the distance matrix
    distance_matrix = pd.read_csv(DISTANCES_F, index_col=0)
    distance_matrix.columns = distance_matrix.columns.astype('int')
    
    # Load taxonomic information
    tax_df = pd.read_csv(TAX_F)
    
    # Build species map dictionary from tax_df
    species_map = dict(zip(tax_df['node'].astype(str), tax_df[TAX_LEVEL]))

    # Filter nodes in distance_matrix that are in species_map
    nodes = distance_matrix.index.tolist()
    filtered_nodes = [node for node in nodes if node in species_map]

    # Collect rows as a generator for memory efficiency
    distance_degree_df = (
        [i, species_map[i], j, species_map[j], distance_matrix.loc[i, j]]
        for i, j in combinations(filtered_nodes, 2)
        if i in distance_matrix.index and j in distance_matrix.columns
    )

    # Convert generator to DataFrame and save
    df = pd.DataFrame(distance_degree_df, columns=['node_i', 'species_i', 'node_j', 'species_j', 'distance'])
    df.to_csv(DISTANCE_DEGREE_F, index=False)
    print(f"Distance degree DataFrame saved to {DISTANCE_DEGREE_F}")

if __name__ == '__main__':
    main()
