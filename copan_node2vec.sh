#!/bin/bash
#
#SBATCH --job-name=copan_walks
#SBATCH --time=00:10:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=200G
#SBATCH --account pmg

# Load the Python module
module load python3

# Load configuration
source config.cfg

# Example graph ID; modify this as needed
GRAPH_ID="dummy_graph"

# Get graph links
INPUT_GRAPH="${graphDir}/${GRAPH_ID}.gfa"
OUTPUT_LINKS="${linksDir}/${GRAPH_ID}_links.json"

python3 scripts/copan_get_graph_link.py "$INPUT_GRAPH" "$OUTPUT_LINKS"

# Random sample walks
INPUT_LINKS="${linksDir}/${GRAPH_ID}_links.json"
OUTPUT_WALKS_ORIENTED="${walkDictsDir}/${GRAPH_ID}_${walk_length}Lw${n_walks}Nw${p}p${q}q_walks_oriented.json"
OUTPUT_WALKS_VECTORIZED="${walkListsDir}/${GRAPH_ID}_${walk_length}Lw${n_walks}Nw${p}p${q}q_walks_vectorized.txt"

python3 workflow/scripts/copan_node2vec_walks_vectorized_copy.py "$INPUT_LINKS" \
    "$walk_length" "$n_walks" "$p" "$q" "$seed" \
    "$OUTPUT_WALKS_ORIENTED" "$OUTPUT_WALKS_VECTORIZED"

# Vectorize walks
INPUT_WALKS="${walkListsDir}/${GRAPH_ID}_${walk_length}Lw${n_walks}Nw${p}p${q}q_walks_vectorized.txt"
OUTPUT_MODEL="${modelDir}/${GRAPH_ID}_${walk_length}Lw${n_walks}Nw${p}p${q}q_walks.model"
OUTPUT_EMBEDDINGS="${embeddingsDir}/${GRAPH_ID}_${walk_length}Lw${n_walks}Nw${p}p${q}q_walks.embeddings"
OUTPUT_EDGE_EMBEDDINGS="${edgeEmbeddingsDir}/${GRAPH_ID}_${walk_length}Lw${n_walks}Nw${p}p${q}q_walks.edge_embeddings"

python3 workflow/scripts/copan_node2vec_vectorization_copy.py \
    "$INPUT_WALKS" "$OUTPUT_MODEL" "$OUTPUT_EMBEDDINGS" "$OUTPUT_EDGE_EMBEDDINGS" \
    "$dimensions" "$window" "$min_count" "$sg"
