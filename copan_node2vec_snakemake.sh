#!/bin/bash
#
#SBATCH --job-name=copanmake
#SBATCH --output=job_out/copanmake_%j.out  # Standard output
#SBATCH --error=job_out/copanmake_%j.err    # Standard error
#SBATCH --time=48:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=20G
#SBATCH --account pmg

source /burg/pmg/users/korem_lab/miniforge3/etc/profile.d/conda.sh
conda activate snakemake

cd /burg/pmg/users/rc3710/CopanTopologyAnalysis

snakemake --unlock
snakemake -c 1 -j 1 --rerun-incomplete
