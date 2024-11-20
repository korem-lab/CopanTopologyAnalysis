#!/bin/bash
#
#SBATCH --job-name=ss_batch
#SBATCH --output=job_out/ss_batch_%j.out  # Standard output
#SBATCH --error=job_out/ss_batch_%j.err    # Standard error
#SBATCH --time=48:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=10G
#SBATCH --account pmg

source /burg/pmg/users/korem_lab/miniforge3/etc/profile.d/conda.sh
conda activate snakemake

cd /burg/pmg/users/rc3710/CopanTopologyAnalysis

# distance_files=$(find workflow/out/pairwise_distances/ -type f -name "sample_1_0_02_*k_pairwiseDistances.csv")
species_f="workflow/out/taxonomy/sample_1_0_02_nodes_by_species_multilabel.csv"
ss_f="workflow/out/clustering_accuracy/silhouette_score.csv"

distance_files="pairwise_distances/sample_1_0_02_30Lw50Nw0.3p0.8q60k_pairwiseDistances.csv"

# Run compute_ari.py in parallel for each embedding file
for distance_file in $distance_files; do
    # Run the Python script in the background for each embedding file
    python3 workflow/scripts/multilabel_silhouette_score.py "$distance_file" "$species_f" "$ss_f" &
done

# Wait for all background processes to finish
wait

echo "All Silhouette Score computations completed."
