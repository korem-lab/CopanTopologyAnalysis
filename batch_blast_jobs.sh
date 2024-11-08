#!/bin/bash
#
#SBATCH --job-name=blast_batch
#SBATCH --output=job_out/blast_batch_%j.out  # Standard output
#SBATCH --error=job_out/blast_batch_%j.err   # Standard error
#SBATCH --time=40:00:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=10G
#SBATCH --account pmg

# Source the config file to load the refGenomes array and other config values
source config/config_blast.cfg

# Loop over each reference genome and submit a job
for refGenome in "${refGenomes[@]}"; do
    sbatch ./node_blast.sh "$refGenome"
    echo "Submitted job for $refGenome"
done