#!/bin/bash
#
#SBATCH --job-name=ss_batch
#SBATCH --output=job_out/batches/ss_batch_%j.out  # Standard output
#SBATCH --error=job_out/batches/ss_batch_%j.err    # Standard error
#SBATCH --time=00:05:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=10G
#SBATCH --account pmg

source /burg/pmg/users/korem_lab/miniforge3/etc/profile.d/conda.sh
conda activate snakemake

cd /burg/pmg/users/rc3710/CopanTopologyAnalysis

# # Slice the distance files for this batch
# distance_files=($1)
# start_index=$2
# end_index=$3
# species_f=$4
# ss_f=$5

# batched_files=("${distance_files[@]:$start_index:$((end_index - start_index))}")

# # Process the files
# for file in "${batched_files[@]}"; do
#     python3 workflow/scripts/multilabel_silhouette_score.py "$file" "$species_f" "$ss_f"
# done

mapfile -t distance_files < <(find workflow/out/pairwise_distances/ -type f -name "sample_1_0_02_*100k_pairwiseDistances.csv")

# Get the list of distance files passed as arguments
start_index=$1  # Second to last argument
files_per_batch=$2    # Third to last argument
species_f=$3    # Last argument before the output file
ss_f=$4           # Output file

echo $start_index
echo $files_per_batch
echo $species_f
echo $ss_f

echo $distance_files

# Slice the distance files for this batch
batched_files=("${distance_files[@]:$start_index:$files_per_batch}")

echo $batched_files

# Process the files
# for file in "${batched_files[@]}"; do
#     python3 workflow/scripts/multilabel_silhouette_score.py "$file" "$species_f" "$ss_f"
# done