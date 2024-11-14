import pandas as pd
import sys

# Load command-line arguments based on the updated order
DISTANCE_F = sys.argv[1]        # Input CSV file with distances
DISTRIBUTION_F = sys.argv[2]     # Output CSV file for statistics
DIMENSIONS = sys.argv[3]
WALK_LENGTH = sys.argv[4]
N_WALKS = sys.argv[5]
P_VAL = sys.argv[6]
Q_VAL = sys.argv[7]
GRAPH_ID = sys.argv[8]

# Load the CSV file
df = pd.read_csv(DISTANCE_F)

# Define the columns to calculate statistics for
columns_of_interest = ['average_pw_euclidean_distance_cross_species', 'average_pw_euclidean_distance_same_species']

# Initialize a list to store results for each column
results = []

# Calculate statistics for each column
for column in columns_of_interest:
    stats = {
        'variable_type': column,
        'mean': df[column].mean(),
        'std_dev': df[column].std(),
        'median': df[column].median(),
        'spread': df[column].max() - df[column].min(),
        'min': df[column].min(),
        'max': df[column].max(),
        'DIMENSIONS': DIMENSIONS,
        'WALK_LENGTH': WALK_LENGTH,
        'N_WALKS': N_WALKS,
        'P_VAL': P_VAL,
        'Q_VAL': Q_VAL,
        'GRAPH_ID': GRAPH_ID
    }
    results.append(stats)

# Convert results to a DataFrame
results_df = pd.DataFrame(results)

# Save to CSV
results_df.to_csv(DISTRIBUTION_F, index=False)

