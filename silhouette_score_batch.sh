#!/bin/bash
#
#SBATCH --job-name=ss_batch
#SBATCH --output=job_out/batches/ss_batch_%j.out  # Standard output
#SBATCH --error=job_out/batches/ss_batch_%j.err    # Standard error
#SBATCH --time=30:00:00
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

# Get the list of distance files passed as arguments
distance_files=("${@:1:$#-4}")  # Get all arguments except the last four
start_index=${!#-3}  # Second to last argument
end_index=${!#-2}    # Third to last argument
species_f=${!#-1}    # Last argument before the output file
ss_f=${!#}           # Output file

# Slice the distance files for this batch
batched_files=("${distance_files[@]:$start_index:$((end_index - start_index))}")

# Process the files
for file in "${batched_files[@]}"; do
    python3 workflow/scripts/multilabel_silhouette_score.py "$file" "$species_f" "$ss_f"
done