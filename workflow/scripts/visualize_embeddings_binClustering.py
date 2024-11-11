from gensim.models import KeyedVectors
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import sys
import pandas as pd
import seaborn as sns

# Adjusted sys.argv to start from index 1
EMBEDDING_F = sys.argv[1]  # The embeddings file
TAX_F = sys.argv[2]        # The species CSV file

EMBEDDING_PLOT = sys.argv[3]  # Output plot file

GRAPH_ID = str(sys.argv[4])   
WALK_LENGTH = str(sys.argv[5])  
N_WALKS = str(sys.argv[6])      
P_VAL = str(sys.argv[7])        
Q_VAL = str(sys.argv[8])       

PERPLEXITY = int(sys.argv[9])  # Perplexity for t-SNE
N_ITER = int(sys.argv[10])     # Number of iterations for t-SNE
N_COMPONENTS = int(sys.argv[11])  # Number of components for t-SNE (usually 2 for 2D)
RAND_STATE = int(sys.argv[12])  # Random state for reproducibility
DIMENSION = str(sys.argv[13])  # Dimension (for example, k for the graph)
ALPHA = float(sys.argv[14])    # Alpha value for scatter plot transparency

TAX_LEVEL = str(sys.argv[15])

def main():
    embedding_kv = KeyedVectors.load(EMBEDDING_F, mmap='r')
    species_map = load_species_map(TAX_F)

    # Filter nodes in embedding vectors based on presence in species_map
    filtered_nodes = [node for node in embedding_kv.index_to_key if node in species_map]
    filtered_vectors = np.array([embedding_kv[node] for node in filtered_nodes])
    node_species = [species_map[node] for node in filtered_nodes]

    # Map species to colors
    unique_species = list(set(node_species))
    num_species = len(unique_species)
    species_to_color = {species: sns.color_palette("hls", num_species)[i] for i, species in enumerate(unique_species)}
    colors = [species_to_color[species] for species in node_species]

    # Run t-SNE
    tsne_model = TSNE(perplexity=PERPLEXITY, n_components=N_COMPONENTS, init='pca', n_iter=N_ITER, random_state=RAND_STATE)
    tsne_results = tsne_model.fit_transform(filtered_vectors)

    # Plotting
    title = (f"{GRAPH_ID}: walk length={WALK_LENGTH}, {N_WALKS} walks, "
             f"p={P_VAL}, q={Q_VAL}, k={DIMENSION}, "
             f"perplexity={PERPLEXITY}, iterations={N_ITER}, tax_level={TAX_LEVEL}")

    plt.figure(figsize=(10, 10))
    x = tsne_results[:, 0]
    y = tsne_results[:, 1]
    plt.scatter(x, y, alpha=ALPHA, linewidth=0, c=colors)
    plt.title(title)
    plt.grid(True)

    if EMBEDDING_PLOT:
        plt.savefig(EMBEDDING_PLOT, format='png', dpi=150, bbox_inches='tight')

def load_species_map(species_csv_file):
    """Load the node-to-species mapping from a CSV file using pandas."""
    df = pd.read_csv(species_csv_file)
    # Convert to dictionary (node -> species)
    species_map = dict(zip(df['node'], df[TAX_LEVEL]))
    return species_map

if __name__ == '__main__':
    main()
