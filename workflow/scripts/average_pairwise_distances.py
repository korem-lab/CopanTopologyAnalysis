import sys
import numpy as np
import pandas as pd

DIST_F = sys.argv[1]
AVG_DIST_F = sys.argv[2]

def main():
    # Load the input CSV with pairwise distances and species
    df = pd.read_csv(DIST_F)

    # Calculate the average pairwise distance within each species
    avg_distances_df = calculate_average_distance(df)

    # Save the result to a CSV file
    avg_distances_df.to_csv(AVG_DIST_F, index=False)

def calculate_average_distance(df):
    # Pre-filter rows: Exclude same node pairs (i.e., node_i == node_j) and ensure nodes are in the same species
    df_filtered = df[(df['species_i'] == df['species_j']) & (df['node_i'] != df['node_j'])]

    # Group by species and calculate the average distance using numpy's efficient operations
    avg_distances = df_filtered.groupby('species_i')['distance'].agg(np.mean).reset_index()

    # Rename the columns for clarity
    avg_distances.columns = ['species', 'average_pw_euclidean_distance']

    return avg_distances

if __name__ == '__main__':
    main()
