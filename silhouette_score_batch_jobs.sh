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

# Path to the exclusion list file
exclude_file="config/silhouette_score_batchTrial2_files.txt"

# Find and filter distance files, excluding specified files
mapfile -t distance_files < <(find workflow/out/pairwise_distances/ -type f -name "sample_1_0_02_*k_pairwiseDistances.csv" \
    | grep -v -F -f "$exclude_file")

n_batches=40
total_files=${#distance_files[@]}
files_per_batch=$(( (total_files + n_batches - 1) / n_batches ))

# Define other parameters
species_f="workflow/out/taxonomy/sample_1_0_02_nodes_by_species_multilabel.csv"

# Generate and submit jobs for each batch
for batch_number in $(seq 0 $((n_batches - 1))); do
    start_index=$((batch_number * files_per_batch))
    end_index=$((start_index + files_per_batch))

    if [ $end_index -gt $total_files ]; then
        end_index=$total_files
    fi

    ss_f="workflow/out/clustering_accuracy/silhouette_score_batch${batch_number}_${start_index}to${end_index}_02.csv"

    # Check if the output file already exists
    if [ ! -f "$ss_f" ]; then
        echo "Output file $ss_f does not exist. Submitting batch $batch_number."

        sbatch silhouette_score_batch.sh $start_index $end_index $species_f $ss_f

    else
        echo "Output file $ss_f already exists. Skipping batch $batch_number."
    fi

done