#!/bin/bash
#
#SBATCH --job-name=copan_walks
#SBATCH --output=workflow/out/job_out/job_output_%j.txt  # Standard output
#SBATCH --error=workflow/out/job_out/job_error_%j.txt    # Standard error
#SBATCH --time=10:00:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=10G
#SBATCH --account pmg

# Load the Python module
#module load python3

# Activate the conda environment
source /burg/pmg/users/korem_lab/miniforge3/etc/profile.d/conda.sh  # Ensures conda is available in the script
conda activate word2vec_env

# Load configuration
source config/config.cfg

# Example graph ID; modify this as needed
GRAPH_ID="copan_0"
echo "input graph: " $GRAPH_ID

get_links=true
generate_walks=true
embed_nodes=true
visualize_embeddings=true

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

# Define parameter values for looping
p_values=(0.5 2.0 1.0)
q_values=(0.5 2.0 1.0)
walk_lengths=(30 80)
n_walks_values=(10 50)

# Define ranges for perplexity and n_iter
perplexity_values=(5 10 30 50 100)  # Adjust as needed
n_iter_values=(500 1000 3000 5000)  # Adjust as needed

# Loop over the combinations of parameters
for walk_length in "${walk_lengths[@]}"; do
  for n_walks in "${n_walks_values[@]}"; do
    for p in "${p_values[@]}"; do
      for q in "${q_values[@]}"; do
        
        echo "Running for walk_length=$walk_length, n_walks=$n_walks, p=$p, q=$q"

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

        # Loop over perplexity and n_iter values
        for perplexity in "${perplexity_values[@]}"; do
          for n_iter in "${n_iter_values[@]}"; do

            PLOT_TITLE="${GRAPH_ID}: walk length ${walk_length}, ${n_walks} walks, p=${p}, q=${q}, perplexity=${perplexity}, iterations=${n_iter}"
            PLOT="${plotsDir}/${GRAPH_ID}_${walk_length}Lw${n_walks}Nw${p}p${q}q_${perplexity}perp_${n_iter}iter_embeddingPlot.png"
            CLUSTER_DICT="${clustersDir}/${GRAPH_ID}_${walk_length}Lw${n_walks}Nw${p}p${q}q_${perplexity}perp_${n_iter}iter_clusters.json"

            if [ "$visualize_embeddings" = true ]; then
                echo "visualize_embeddings is true. Checking for plot file..."
                if [ ! -f "$PLOT" ] || [ ! -f "$CLUSTER_DICT" ]; then
                    echo "Plot files do not exist. Running the visualize_embeddings script."
                    python3 workflow/scripts/visualize_embeddings.py \
                    "$MODEL" "$EMBEDDINGS" "$LINKS" "$PLOT" "$PLOT_TITLE" "$CLUSTER_DICT" \
                    "$perplexity" "$n_iter" "$n_components" "$random_state"
                else
                    echo "Plot files already exist."
                fi
            else
                echo "visualize_embeddings is false. Skipping the visualize_embeddings step."
            fi
          done
        done

      done
    done
  done
done

