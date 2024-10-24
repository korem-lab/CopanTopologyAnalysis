#!/bin/bash
#
#SBATCH --job-name=validation
#SBATCH --output=workflow/out/job_out/validation_%j.out  # Standard output
#SBATCH --error=workflow/out/job_out/validation_%j.err    # Standard error
#SBATCH --time=10:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=10G
#SBATCH --account pmg

source /burg/pmg/users/korem_lab/miniforge3/etc/profile.d/conda.sh  # Ensures conda is available in the script
conda activate snakemake

cd /burg/pmg/users/rc3710/CopanTopologyAnalysis

python3 workflow/scripts/validate_node2vec_pipeline.py
