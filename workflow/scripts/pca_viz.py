from gensim.models import KeyedVectors
from sklearn import decomposition
import matplotlib.pyplot as plt
import sys
import numpy as np

# Adjusted sys.argv to start from index 1
EMBEDDING_F = sys.argv[1]  # The embeddings file

EMBEDDING_PLOT = sys.argv[2]  # Output plot file

GRAPH_ID = str(sys.argv[3])   
WALK_LENGTH = str(sys.argv[4])  
N_WALKS = str(sys.argv[5])      
P_VAL = str(sys.argv[6])        
Q_VAL = str(sys.argv[7])       

N_COMPONENTS = int(sys.argv[8]) 
DIMENSION = str(sys.argv[9])  # Dimension (k)
ALPHA = 0.2

def main():
    embedding_kv = KeyedVectors.load(EMBEDDING_F, mmap='r')
    nodes = embedding_kv.index_to_key
    filtered_vectors = np.array([embedding_kv[node] for node in nodes])

    # Run t-SNE
    pca_model = decomposition.PCA(n_components=N_COMPONENTS)
    pca_results = pca_model.fit_transform(filtered_vectors)

    # Plotting
    title = (f"{GRAPH_ID}: walk length={WALK_LENGTH}, {N_WALKS} walks, "
             f"p={P_VAL}, q={Q_VAL}, k={DIMENSION}")

    plt.figure(figsize=(10, 10))
    x = pca_results[:, 0]
    y = pca_results[:, 1]
    plt.scatter(x, y, alpha=ALPHA, linewidth=0, c="black")
    plt.title(title)
    plt.grid(True)

    if EMBEDDING_PLOT:
        plt.savefig(EMBEDDING_PLOT, format='png', dpi=150, bbox_inches='tight')

if __name__ == '__main__':
    main()
