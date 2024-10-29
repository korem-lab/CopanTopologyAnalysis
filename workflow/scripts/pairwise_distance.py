from gensim.models import KeyedVectors
from scipy.spatial.distance import pdist, squareform
import numpy as np
import pandas as pd
import sys
from scipy.spatial.distance import euclidean

EMBEDDING_F = sys.argv[1]
DISTANCES_F = sys.argv[2]  


def main():
    embedding_kv = KeyedVectors.load(EMBEDDING_F, mmap='r')

    # Step 1: Get all node names and their corresponding embeddings
    node_names = list(embedding_kv.key_to_index.keys())
    embedding_matrix = np.array([embedding_kv[node] for node in node_names])

    # print(embedding_matrix)

    # Step 2: Calculate pairwise distances
    distance_vector = pdist(embedding_matrix, metric='euclidean')
    distance_matrix = squareform(distance_vector)

    # `distance_matrix` is now a square matrix with pairwise distances

    # Step 3: Save as CSV using numpy
    distance_df = pd.DataFrame(distance_matrix, index=node_names, columns=node_names)

    # Save the distance matrix to a CSV file
    distance_df.to_csv(DISTANCES_F, float_format='%.6f')    

if __name__ == '__main__':
    main()
