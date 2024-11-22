from gensim.models import KeyedVectors
from sklearn import decomposition
import matplotlib.pyplot as plt
import sys
import pandas as pd
import seaborn as sns
import numpy as np

# Adjusted sys.argv to start from index 1
EMBEDDING_F = sys.argv[1]  # The embeddings file
TAX_F = sys.argv[2]        # The species CSV file

EMBEDDING_PLOT = sys.argv[3]  # Output plot file

GRAPH_ID = str(sys.argv[4])   
WALK_LENGTH = str(sys.argv[5])  
N_WALKS = str(sys.argv[6])      
P_VAL = str(sys.argv[7])        
Q_VAL = str(sys.argv[8])       

N_COMPONENTS = int(sys.argv[9]) 
DIMENSION = str(sys.argv[10])  # Dimension (k)
ALPHA = float(sys.argv[11])    # Alpha value for scatter plot

TAX_LEVEL = str(sys.argv[12])

def main():
    embedding_kv = KeyedVectors.load(EMBEDDING_F, mmap='r')
    species_map = load_species_map(TAX_F)

    # Filter nodes in embedding vectors based on presence in species_map
    filtered_nodes = [node for node in embedding_kv.index_to_key if node in species_map]
    filtered_vectors = np.array([embedding_kv[node] for node in filtered_nodes])
    node_species = [species_map[node] for node in filtered_nodes]

    print("num filtered vectors:" + str(len(filtered_vectors)))
    print("num filtered nodes:" + str(len(filtered_nodes)))
    print("num species:" + str(len(node_species)))

    species_not_in_embedding = set(species_map.keys()) - set(embedding_kv.index_to_key)
    embedding_not_in_species = set(embedding_kv.index_to_key) - set(species_map.keys())

    print(f"Number of nodes in species_map but not in embedding_kv: {len(species_not_in_embedding)}")
    print(f"Number of nodes in embedding_kv but not in species_map: {len(embedding_not_in_species)}")

        # Writing species_not_in_embedding to a file
    with open("job_out/species_not_in_embedding.txt", "w") as f:
        for node in species_not_in_embedding:
            f.write(f"{node}\n")

    # Writing embedding_not_in_species to a file
    with open("job_out/embedding_not_in_species.txt", "w") as f:
        for node in embedding_not_in_species:
            f.write(f"{node}\n")

    # Map species to colors
    unique_species = list(set(node_species))
    num_species = len(unique_species)
    species_to_color = {species: sns.color_palette("hls", num_species)[i] for i, species in enumerate(unique_species)}
    colors = [species_to_color[species] for species in node_species]

    # Run t-SNE
    pca_model = decomposition.PCA(n_components=N_COMPONENTS)
    pca_results = pca_model.fit_transform(filtered_vectors)

    # Plotting
    title = (f"{GRAPH_ID}: walk length={WALK_LENGTH}, {N_WALKS} walks, "
             f"p={P_VAL}, q={Q_VAL}, k={DIMENSION}, "
             f"tax_level={TAX_LEVEL}")

    plt.figure(figsize=(10, 10))
    x = pca_results[:, 0]
    y = pca_results[:, 1]
    plt.scatter(x, y, alpha=ALPHA, linewidth=0, c=colors)
    plt.title(title)
    plt.grid(True)

    if EMBEDDING_PLOT:
        plt.savefig(EMBEDDING_PLOT, format='png', dpi=150, bbox_inches='tight')

def load_species_map(species_csv_file):
    """Load the node-to-species mapping from a CSV file using pandas."""
    df = pd.read_csv(species_csv_file)
    # Convert to dictionary (node -> species)
    species_map = dict(zip(df['node'].astype(str), df[TAX_LEVEL]))
    return species_map

if __name__ == '__main__':
    main()
