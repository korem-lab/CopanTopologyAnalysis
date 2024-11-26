#!/bin/bash
#
#SBATCH --job-name=validation
#SBATCH --output=job_out/genus_ss_%j.out  # Standard output
#SBATCH --error=job_out/genus_ss_%j.err    # Standard error
#SBATCH --time=02:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=10G
#SBATCH --account pmg

source /burg/pmg/users/korem_lab/miniforge3/etc/profile.d/conda.sh  # Ensures conda is available in the script
conda activate snakemake

cd /burg/pmg/users/rc3710/CopanTopologyAnalysi

distance_f="workflow/out/pairwise_distances/sample_1_0_02_50Lw50Nw0.3p0.1q60k_pairwiseDistances.csv"
genus_f="workflow/out/taxonomy/sample_1_0_02_nodes_by_species_multilabel.csv"
out_f="workflow/out/clustering_accuracy/sample_1_0_02_50Lw50Nw0.3p0.1q60k_genus_level_silhouette_score.csv"

python3 workflow/scripts/multilabel_silhouette_score.py $distance_f $genus_f $out_f
