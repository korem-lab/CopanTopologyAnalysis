from gensim.models import KeyedVectors
from sklearn import decomposition
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from collections import Counter
import re
import glob

TAX_F = "workflow/out/taxonomy/sample_1_0_02_nodes_by_species.csv"

N_COMPONENTS = 2
ALPHA = 0.3

def main():

    file_pattern = "workflow/out/vectorization_model/embeddings/sample_1_0_02_50Lw50Nw*60k_walks.embeddings"
    matching_files = glob.glob(file_pattern)

    species_map = load_species_map(TAX_F)

    # Print the matching files
    for file in matching_files:

        embedding_kv = KeyedVectors.load(file, mmap='r')

        filtered_nodes = [node for node in embedding_kv.index_to_key if node in species_map]

        # Count the nodes for each species using Counter
        species_count = Counter([species_map[node] for node in filtered_nodes])
        
        most_common_species, max_count = species_count.most_common(1)[0]

        species_nodes = [node for node in filtered_nodes if species_map[node] == most_common_species]
        species_vectors = np.array([embedding_kv[node] for node in species_nodes])

        pca_model = decomposition.PCA(n_components=N_COMPONENTS)
        pca_results = pca_model.fit_transform(species_vectors)

        file_name = os.path.basename(file)
        pattern = r"(sample_\d+_\d+_\d+)_([0-9]+)Lw([0-9]+)Nw([0-9.]+)p([0-9.]+)q([0-9]+)k_walks\.embeddings"
        match = re.match(pattern, file_name)

        if match:
            graph_id = match.group(1)
            walk_length = match.group(2)
            n_walks = match.group(3)
            p = match.group(4)
            q = match.group(5)
            dimensions = match.group(6)
        
        title = (f"{graph_id}: walk length={walk_length}, {n_walks} walks, "
                f"p={p}, q={q}, k={dimensions}, "
                f"species={most_common_species}")

        plt.figure(figsize=(10, 10))
        x = pca_results[:, 0]
        y = pca_results[:, 1]
        plt.scatter(x, y, alpha=ALPHA, linewidth=0, c="black")
        plt.title(title)
        plt.grid(True)

        basename = os.path.basename(file).rsplit(".", 1)[0]
        plot_f = "workflow/out/plots/" + basename + "_single_species_" + most_common_species.replace(" ", "_") + ".png"

        plt.savefig(plot_f, format='png', dpi=150, bbox_inches='tight')
        plt.close()
        

def load_species_map(species_csv_file):
    """Load the node-to-species mapping from a CSV file using pandas."""
    df = pd.read_csv(species_csv_file)
    species_map = dict(zip(df['node'].astype(str), df["species"]))

    return species_map

if __name__ == '__main__':
    main()
