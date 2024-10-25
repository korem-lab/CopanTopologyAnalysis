from gensim.models import KeyedVectors
from scipy.spatial.distance import pdist, squareform
import numpy as np
import sys

EMBEDDING_F = sys.argv[1]

DISTANCES_F = sys.argv[2]  


def main():
    embedding_kv = KeyedVectors.load(EMBEDDING_F, mmap='r')

    # Step 1: Get all node names and their corresponding embeddings
    node_names = list(embedding_kv.key_to_index.keys())
    embedding_matrix = np.array([embedding_kv[node] for node in node_names])

    # Step 2: Calculate pairwise distances
    distance_vector = pdist(embedding_matrix, metric='euclidean')
    distance_matrix = squareform(distance_vector)

    # `distance_matrix` is now a square matrix with pairwise distances

    # Step 3: Save as CSV using numpy
    # Create a header for the CSV
    header = [''] + node_names

    # Save the distance matrix to a CSV file
    np.savetxt(DISTANCES_F, distance_matrix, delimiter=',', header=','.join(header), comments='', fmt='%.6f')
    

if __name__ == '__main__':
    main()
