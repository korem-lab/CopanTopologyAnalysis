#!/bin/bash
#
#SBATCH --job-name=silscore
#SBATCH --output=workflow/out/job_out/silscore_%j.out  # Standard output
#SBATCH --error=workflow/out/job_out/silscore_%j.err    # Standard error
#SBATCH --time=24:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=20G
#SBATCH --account pmg

source /burg/pmg/users/korem_lab/miniforge3/etc/profile.d/conda.sh  # Ensures conda is available in the script
conda activate snakemake

cd /burg/pmg/users/rc3710/CopanTopologyAnalysis

python3 workflow/scripts/multilabel_silhouette_score.py \
    workflow/out/pairwise_distances/sample_1_0_02_30Lw30Nw1.0p0.1q20k_pairwiseDistances.csv \
    workflow/out/taxonomy/sample_1_0_02_nodes_by_species_multilabel.csv