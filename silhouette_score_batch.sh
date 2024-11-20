#!/bin/bash
#
#SBATCH --job-name=ss_batch
#SBATCH --output=job_out/bathces/ss_batch_%j.out  # Standard output
#SBATCH --error=job_out/batches/ss_batch_%j.err    # Standard error
#SBATCH --time=72:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=10G
#SBATCH --account pmg

source /burg/pmg/users/korem_lab/miniforge3/etc/profile.d/conda.sh
conda activate snakemake

cd /burg/pmg/users/rc3710/CopanTopologyAnalysis

# Parse arguments
batch_number=$1
start_index=$2
end_index=$3
distance_files=("${@:4}")  # Remaining arguments are the distance files

# Define other parameters
species_f="workflow/out/taxonomy/sample_1_0_02_nodes_by_species_multilabel.csv"
ss_f="workflow/out/clustering_accuracy/silhouette_score_batch_${batch_number}.csv"

# Slice the distance files for this batch
batched_files=("${distance_files[@]:$start_index:$((end_index - start_index))}")

# Process the files
for distance_file in "${batched_files[@]}"; do
    python3 workflow/scripts/multilabel_silhouette_score.py "$distance_file" "$species_f" "$ss_f"
done