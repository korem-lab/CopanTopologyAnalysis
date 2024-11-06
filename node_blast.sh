#!/bin/bash
#
#SBATCH --job-name=blast
#SBATCH --output=job_out/blast_%j.out  # Standard output
#SBATCH --error=job_out/blast_%j.err   # Standard error
#SBATCH --time=10:00:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=20G
#SBATCH --account pmg

# Activate the conda environment
source /burg/pmg/users/korem_lab/miniforge3/etc/profile.d/conda.sh  # Ensures conda is available in the script
conda activate blast

# Load configuration
source config/config_blast.cfg

blast_db="${dbDir}/${graphID}"
nodes_fasta="${copangraphDir}/${graphID}.fasta"
blast_out="${blastOutDir}/${graphID}_blast_results.out"

# Check if BLAST DB exists; if not, create it
if [ ! -f "${blast_db}.nhr" ]; then
    echo "Creating BLAST nucleotide database..."

    makeblastdb -in "${refGenome}" -dbtype nucl -out "${blast_db}" -title "${graphID}_Reference_Genome_DB"

else
    echo "BLAST nucleotide database already exists. Skipping creation."
fi

# Run BLAST of nodes against the reference database
if [ ! -f "${blast_out}" ]; then
    echo "Running BLAST search of nodes against reference genome database..."

    blastn -query "${nodes_fasta}" -db "${blast_db}" -out "${blast_out}" \
        -perc_identity "${percidThreshold}" -word_size "${wordSize}" -qcov_hsp_perc "${coverage}" -outfmt 6
    
    echo "BLAST search complete. Results saved to ${blast_out}"

else
    echo "BLAST output file already exists. Skipping BLAST search."
fi
