#!/bin/bash
#
#SBATCH --job-name=ss_batch
#SBATCH --output=job_out/batches/ss_batch_%j.out  # Standard output
#SBATCH --error=job_out/batches/ss_batch_%j.err    # Standard error
#SBATCH --time=72:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=10G
#SBATCH --account pmg

source /burg/pmg/users/korem_lab/miniforge3/etc/profile.d/conda.sh
conda activate snakemake

cd /burg/pmg/users/rc3710/CopanTopologyAnalysis

# Path to the exclusion list file
exclude_file="config/silhouette_score_batchTrial5_files.txt"

# Find and filter distance files, excluding specified files
mapfile -t distance_files < <(find workflow/out/pairwise_distances/ -type f -name "sample_1_0_02_*k_pairwiseDistances.csv" \
    | grep -v -F -f "$exclude_file")

# Get the list of distance files passed as arguments
start_index=$1  # Second to last argument
end_index=$2    # Third to last argument
species_f=$3    # Last argument before the output file
ss_f=$4           # Output file

length=$((end_index - start_index))

# Slice the distance files for this batch
batched_files=("${distance_files[@]:$start_index:$length}")

# echo "batched files: ${batched_files[@]}"

# Process the files
for file in "${batched_files[@]}"; do
    echo $file
    python3 workflow/scripts/multilabel_silhouette_score.py "$file" "$species_f" "$ss_f"
done