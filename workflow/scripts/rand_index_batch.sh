#!/bin/bash

source /burg/pmg/users/korem_lab/miniforge3/etc/profile.d/conda.sh
conda activate snakemake

cd /burg/pmg/users/rc3710/CopanTopologyAnalysis

embedding_files=$(find workflow/out/vectorization_model/embeddings/ -type f -name "*k_walks.embeddings")

species_f="workflow/out/blast/sample_1_0_02_nodes_by_species_multilabel.csv"
ari_f="workflow/out/clustering/ari.csv"

# Run compute_ari.py in parallel for each embedding file
for embedding_file in $embedding_files; do
    # Run the Python script in the background for each embedding file
    python3 workflow/scripts/rand_index.py "$embedding_file" "$species_f" "$ari_f" &
done

# Wait for all background processes to finish
wait

echo "All ARI computations completed."
