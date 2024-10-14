#!/bin/bash
#
#SBATCH --job-name=copan_walks
#SBATCH --output=/workflow/out/job_out/job_output_%j.txt  # Standard output
#SBATCH --error=/workflow/out/job_out/job_error_%j.txt    # Standard error
#SBATCH --time=00:10:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=200G
#SBATCH --account pmg

# Load the Python module
module load python3

# Load configuration
source config/config.cfg

# Example graph ID; modify this as needed
GRAPH_ID="dummy_graph"

# Get graph links
INPUT_GRAPH="${graphDir}/${GRAPH_ID}.gfa"
LINKS="${linksDir}/${GRAPH_ID}_links.json"

# python3 workflow/scripts/copan_get_graph_links.py "$INPUT_GRAPH" "$LINKS"

# Random sample walks
WALKS_ORIENTED="${walkDictsDir}/${GRAPH_ID}_${walk_length}Lw${n_walks}Nw${p}p${q}q_walks_oriented.json"
WALKS_VECTORIZED="${walkListsDir}/${GRAPH_ID}_${walk_length}Lw${n_walks}Nw${p}p${q}q_walks_vectorized.txt"

python3 workflow/scripts/copan_node2vec_walks_vectorized_copy.py "$LINKS" \
    "$walk_length" "$n_walks" "$p" "$q" "$seed" \
    "$WALKS_ORIENTED" "$WALKS_VECTORIZED"

# Vectorize walks
OUTPUT_MODEL="${modelDir}/${GRAPH_ID}_${walk_length}Lw${n_walks}Nw${p}p${q}q_walks.model"
OUTPUT_EMBEDDINGS="${embeddingsDir}/${GRAPH_ID}_${walk_length}Lw${n_walks}Nw${p}p${q}q_walks.embeddings"
OUTPUT_EDGE_EMBEDDINGS="${edgeEmbeddingsDir}/${GRAPH_ID}_${walk_length}Lw${n_walks}Nw${p}p${q}q_walks.edge_embeddings"

python3 workflow/scripts/copan_node2vec_vectorization_copy.py \
    "$WALKS_VECTORIZED" "$OUTPUT_MODEL" "$OUTPUT_EMBEDDINGS" "$OUTPUT_EDGE_EMBEDDINGS" \
    "$dimensions" "$window" "$min_count" "$sg"
