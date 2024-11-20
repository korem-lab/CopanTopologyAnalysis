#!/bin/bash
#
#SBATCH --job-name=jobs_sub
#SBATCH --output=job_out/jobs_sub_%j.out  # Standard output
#SBATCH --error=job_out/jobs_sub_%j.err   # Standard error
#SBATCH --time=00:10:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=10G
#SBATCH --account pmg

# Activate the environment
source /burg/pmg/users/korem_lab/miniforge3/etc/profile.d/conda.sh
conda activate snakemake

# Navigate to the project directory
cd /burg/pmg/users/rc3710/CopanTopologyAnalysis

# Define input parameters
distance_files=$(find workflow/out/pairwise_distances/ -type f -name "sample_1_0_02_*k_pairwiseDistances.csv")
n_batches=50
total_files=${#distance_files[@]}
files_per_batch=$(( (total_files + n_batches - 1) / n_batches ))

# Generate and submit jobs for each batch
for batch_number in $(seq 0 $((n_batches - 1))); do
    start_index=$((batch_number * files_per_batch))
    end_index=$((start_index + files_per_batch))
    if [ $end_index -gt $total_files ]; then
        end_index=$total_files
    fi

    # Submit the shared batch script with arguments
    sbatch silhouette_score_batch.sh $batch_number $start_index $end_index "${distance_files[@]}"
done