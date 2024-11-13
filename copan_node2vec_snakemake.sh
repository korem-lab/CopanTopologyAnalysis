#!/bin/bash
#
#SBATCH --job-name=copanmake
#SBATCH --output=job_out/copanmake_%j.out  # Standard output
#SBATCH --error=job_out/copanmake_%j.err    # Standard error
#SBATCH --time=05:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=3
#SBATCH --mem=100G
#SBATCH --account pmg

source /burg/pmg/users/korem_lab/miniforge3/etc/profile.d/conda.sh
conda activate snakemake

cd /burg/pmg/users/rc3710/CopanTopologyAnalysis

snakemake --unlock
snakemake -c 3 -j 3 --rerun-incomplete