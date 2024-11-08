#!/bin/bash
#
#SBATCH --job-name=blast
#SBATCH --output=job_out/blast_%j.out  # Standard output
#SBATCH --error=job_out/blast_%j.err   # Standard error
#SBATCH --time=20:00:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=50G
#SBATCH --account pmg

# Load configuration
source config/config_blast.cfg

# Check if refGenome argument is provided
if [ -z "$1" ]; then
    echo "Error: No reference genome provided. Usage: ./blast_script.sh <refGenome.fasta>"
    exit 1
fi

# Reference genome (passed as argument)
refGenome=$1
refGenomeName=$(basename "${refGenome}" .fasta)

# Define the nodes fasta file (query file)
nodes_fasta="${copangraphDir}/${graphID}.fasta"

# Define the output directory for BLAST results
blast_out_dir="${blastOutDir}"

# Construct the full path for the current BLAST database
blast_db="${dbDir}/${refGenomeName}_blast_db"

# Define the output file for this BLAST run
blast_out="${blast_out_dir}/${graphID}_blast_results_${refGenomeName}.out"

# Check if BLAST DB exists; if not, create it
if [ ! -f "${blast_db}.nhr" ]; then
    echo "Creating BLAST nucleotide database for ${refGenomeName}..."

    makeblastdb -in "${refGenome}" -dbtype nucl -out "${blast_db}" -title "${refGenomeName}_Reference_Genome_DB"

    if [ $? -ne 0 ]; then
        echo "Error: Failed to create BLAST database for ${refGenomeName}"
        exit 1
    fi
else
    echo "BLAST nucleotide database for ${refGenomeName} already exists. Skipping creation."
fi

# Run BLAST of nodes against the current reference genome database
if [ ! -f "${blast_out}" ]; then
    echo "Running BLAST search of nodes against ${refGenomeName} database..."

    blastn -query "${nodes_fasta}" -db "${blast_db}" -out "${blast_out}" \
        -perc_identity "${percidThreshold}" -word_size "${wordSize}" -qcov_hsp_perc "${coverage}" -outfmt 6

    echo "BLAST search complete for ${refGenomeName}. Results saved to ${blast_out}"
else
    echo "BLAST output for ${refGenomeName} already exists. Skipping BLAST search."
fi
