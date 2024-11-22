from gensim.models import KeyedVectors
from sklearn import decomposition
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

EMBEDDING_F = "workflow/out/vectorization_model/embeddings/sample_1_0_02_50Lw50Nw1.0p1.0q60k_walks.embeddings"
TAX_F = "workflow/out/taxonomy/sample_1_0_02_nodes_by_species.csv"

N_COMPONENTS = 2
ALPHA = 0.3

def main():
    embedding_kv = KeyedVectors.load(EMBEDDING_F, mmap='r')
    species_map = load_species_map(TAX_F)

    filtered_nodes = [node for node in embedding_kv.index_to_key if node in species_map]
    unique_species = list(set([species_map[node] for node in filtered_nodes]))

    for species in unique_species:
        
        species_nodes = [node for node in filtered_nodes if species_map[node] == species]
        species_vectors = np.array([embedding_kv[node] for node in species_nodes])

        # Run t-SNE
        pca_model = decomposition.PCA(n_components=N_COMPONENTS)
        pca_results = pca_model.fit_transform(species_vectors)

        # Plotting
        basename = os.path.basename(EMBEDDING_F)
        basename = basename.split(".")[0]
        title = basename + " , " + species

        plt.figure(figsize=(10, 10))
        x = pca_results[:, 0]
        y = pca_results[:, 1]
        plt.scatter(x, y, alpha=ALPHA, linewidth=0, c="black")
        plt.title(title)
        plt.grid(True)

        plot_f = "workflow/out/plots/single_species" + basename + "_" + species.replace(" ", "_") + ".csv"

        plt.savefig(plot_f, format='png', dpi=150, bbox_inches='tight')

def load_species_map(species_csv_file):
    """Load the node-to-species mapping from a CSV file using pandas."""
    df = pd.read_csv(species_csv_file)
    species_map = dict(zip(df['node'].astype(str), df["species"]))

    return species_map

if __name__ == '__main__':
    main()
