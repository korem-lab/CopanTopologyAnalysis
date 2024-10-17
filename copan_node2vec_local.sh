#!/bin/bash

# Load configuration
source config/config.cfg

# Example graph ID; modify this as needed
GRAPH_ID="copan_0"
echo "input graph: " $GRAPH_ID

get_links=true
generate_walks=true
embed_nodes=true
visualize_embeddings=false

# Get graph links
INPUT_GRAPH="${graphDir}/${GRAPH_ID}.gfa"
LINKS="${linksDir}/${GRAPH_ID}_links.json"

# Get graph links step
if [ "$get_links" = true ]; then
    echo "get_links is true. Checking for links file..."
    # Check if links file exists
    if [ ! -f "$LINKS" ]; then
        echo "Links file does not exist. Running the get_links script."
        python3 workflow/scripts/get_graph_links.py "$INPUT_GRAPH" "$LINKS"
    else
        echo "Links file already exists."
    fi
else
    echo "get_links is false. Skipping the get_links step."
fi

# Random sample walks
WALKS_ORIENTED="${walkDictsDir}/${GRAPH_ID}_${walk_length}Lw${n_walks}Nw${p}p${q}q_walks_oriented.json"
WALKS_VECTORIZED="${walkListsDir}/${GRAPH_ID}_${walk_length}Lw${n_walks}Nw${p}p${q}q_walks_vectorized.txt"

# Generate walks step
if [ "$generate_walks" = true ]; then
    echo "generate_walks is true. Checking for walks files..."
    if [ ! -f "$WALKS_ORIENTED" ] || [ ! -f "$WALKS_VECTORIZED" ]; then
        echo "One or both walks files do not exist. Running the generate_walks script."
        python3 workflow/scripts/generate_walks.py "$LINKS" \
        "$walk_length" "$n_walks" "$p" "$q" "$seed" \
        "$WALKS_ORIENTED" "$WALKS_VECTORIZED"
    else
        echo "Walks files already exist."
    fi
else
    echo "generate_walks is false. Skipping the generate_walks step."
fi

# Vectorize walks
MODEL="${modelDir}/${GRAPH_ID}_${walk_length}Lw${n_walks}Nw${p}p${q}q_walks.model"
EMBEDDINGS="${embeddingsDir}/${GRAPH_ID}_${walk_length}Lw${n_walks}Nw${p}p${q}q_walks.embeddings"
EDGE_EMBEDDINGS="${edgeEmbeddingsDir}/${GRAPH_ID}_${walk_length}Lw${n_walks}Nw${p}p${q}q_walks.edge_embeddings"

# Check if model files do not exist
if [ "$embed_nodes" = true ]; then
    echo "embed_nodes is true. Checking for model files..."
    if [ ! -f "$MODEL" ] || [ ! -f "$EMBEDDINGS" ] || [ ! -f "$EDGE_EMBEDDINGS" ]; then
        echo "Model files do not exist. Running the vectorize_embed_nodes script."
        python3 workflow/scripts/vectorize_embed_nodes.py \
        "$WALKS_VECTORIZED" "$MODEL" "$EMBEDDINGS" "$EDGE_EMBEDDINGS" \
        "$dimensions" "$window" "$min_count" "$sg"
    else
        echo "Model files already exist."
    fi
else
    echo "embed_nodes is false. Skipping the embed_nodes step."
fi

# Check if plot file exists
if [ "$visualize_embeddings" = true ]; then
    echo "visualize_embeddings is true. Checking for plot file..."
    if [ ! -f "$PLOT" ]; then
        echo "Plot files do not exist. Running the visualize_embeddings script."
        python3 workflow/scripts/visualize_embeddings.py \
        "$MODEL" "$EMBEDDINGS" "$LINKS" "$PLOT" "$PLOT_TITLE" \
        "$perplexity" "$n_iter" "$n_components" "$random_state"
    else
        echo "Plot files already exist."
    fi
else
    echo "visualize_embeddings is false. Skipping the visualize_embeddings step."
fi
