import sys
import numpy as np
import pandas as pd

DIST_F = sys.argv[1]
AVG_DIST_F = sys.argv[2]

def main():
    # Load the input CSV with pairwise distances and species
    df = pd.read_csv(DIST_F)

    # Ensure necessary columns exist
    required_columns = ['node_i', 'species_i', 'node_j', 'species_j', 'distance']

    # Calculate the average pairwise distances for same-species and cross-species pairs
    avg_distances_df = calculate_average_distances(df)

    # Save the result to a CSV file
    avg_distances_df.to_csv(AVG_DIST_F, index=False)

def calculate_average_distances(df):
    # Filter for same-species pairs (excluding node_i == node_j)
    same_species_df = df[(df['species_i'] == df['species_j']) & (df['node_i'] != df['node_j'])]
    
    # Filter for cross-species pairs (species_i != species_j)
    cross_species_df = df[(df['species_i'] != df['species_j'])]

    # Group by species and calculate the average pairwise distance for both cases
    avg_same_species = same_species_df.groupby('species_i')['distance'].agg(np.mean).reset_index()
    avg_same_species.columns = ['species', 'average_pw_euclidean_distance_same_species']

    avg_cross_species = cross_species_df.groupby('species_i')['distance'].agg(np.mean).reset_index()
    avg_cross_species.columns = ['species', 'average_pw_euclidean_distance_cross_species']

    # Merge both results on 'species'
    avg_distances_df = pd.merge(avg_same_species, avg_cross_species, on='species', how='outer')

    return avg_distances_df


if __name__ == '__main__':
    main()
