#!/bin/bash

# Load configuration
source config/config.cfg

# Example graph ID; modify this as needed
GRAPH_ID="copan_0"

# Get graph links
INPUT_GRAPH="${graphDir}/${GRAPH_ID}.gfa"
LINKS="${linksDir}/${GRAPH_ID}_links.json"

# python3 workflow/scripts/copan_get_graph_links.py "$INPUT_GRAPH" "$LINKS"

# Random sample walks
WALKS_ORIENTED="${walkDictsDir}/${GRAPH_ID}_${walk_length}Lw${n_walks}Nw${p}p${q}q_walks_oriented.json"
WALKS_VECTORIZED="${walkListsDir}/${GRAPH_ID}_${walk_length}Lw${n_walks}Nw${p}p${q}q_walks_vectorized.txt"

# python3 workflow/scripts/copan_node2vec_walks_vectorized.py "$LINKS" \
#     "$walk_length" "$n_walks" "$p" "$q" "$seed" \
#     "$WALKS_ORIENTED" "$WALKS_VECTORIZED"

# Vectorize walks
MODEL="${modelDir}/${GRAPH_ID}_${walk_length}Lw${n_walks}Nw${p}p${q}q_walks.model"
EMBEDDINGS="${embeddingsDir}/${GRAPH_ID}_${walk_length}Lw${n_walks}Nw${p}p${q}q_walks.embeddings"
EDGE_EMBEDDINGS="${edgeEmbeddingsDir}/${GRAPH_ID}_${walk_length}Lw${n_walks}Nw${p}p${q}q_walks.edge_embeddings"

# python3 workflow/scripts/copan_node2vec_vectorization_copy.py \
#     "$WALKS_VECTORIZED" "$MODEL" "$EMBEDDINGS" "$EDGE_EMBEDDINGS" \
#     "$dimensions" "$window" "$min_count" "$sg"

PLOT="${plotsDir}/${GRAPH_ID}_${walk_length}Lw${n_walks}Nw${p}p${q}q_embeddingPlot.png"
PLOT_TITLE="${GRAPH_ID}: ${walk_length} walk length, ${n_walks} walks, ${p} p, ${q} q"

# Visualize embeddings
python3 workflow/scripts/visualize_embeddings.py \
    "$MODEL" "$EMBEDDINGS" "$LINKS" "$PLOT" "$PLOT_TITLE" \
    "$perplexity" "$n_iter" "$n_components" "$random_state"

