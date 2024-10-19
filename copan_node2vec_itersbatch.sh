#!/bin/bash
#
#SBATCH --job-name=get_links
#SBATCH --output=workflow/out/job_out/job_output_%j.txt  # Standard output
#SBATCH --error=workflow/out/job_out/job_error_%j.txt    # Standard error
#SBATCH --time=48:00:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=50G
#SBATCH --account pmg

# Load the Python module
# module load python3

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

# Loop over the combinations of parameters
for walk_length in "${walk_lengths[@]}"; do
  for n_walks in "${n_walks_values[@]}"; do
    for p in "${p_values[@]}"; do
      for q in "${q_values[@]}"; do
        
        echo "Scheduling job for walk_length=$walk_length, n_walks=$n_walks, p=$p, q=$q"

        # Submit each combination as a separate job
        sbatch --job-name="copan_w${walk_length}_n${n_walks}_p${p}_q${q}" \
       --output="workflow/out/job_out/w${walk_length}_n${n_walks}_p${p}_q${q}_output_%j.txt" \
       --error="workflow/out/job_out/w${walk_length}_n${n_walks}_p${p}_q${q}_error_%j.txt" \
       --export=ALL,GRAPH_ID=$GRAPH_ID,walk_length=$walk_length,n_walks=$n_walks,p=$p,q=$q,get_links=$get_links,generate_walks=$generate_walks,embed_nodes=$embed_nodes,visualize_embeddings=$visualize_embeddings <<'EOF'

#!/bin/bash
#SBATCH --time=10:00:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=10G
#SBATCH --account pmg

# Ensure conda is available and activate environment
source /burg/pmg/users/korem_lab/miniforge3/etc/profile.d/conda.sh
conda activate word2vec_env

# Load configuration
source config/config.cfg

# Use the variables passed through --export
GRAPH_ID=${GRAPH_ID}
walk_length=${walk_length}
n_walks=${n_walks}
p=${p}
q=${q}

# Define file paths
INPUT_GRAPH="${graphDir}/${GRAPH_ID}.gfa"
LINKS="${linksDir}/${GRAPH_ID}_links.json"
WALKS_ORIENTED="${walkDictsDir}/${GRAPH_ID}_${walk_length}Lw${n_walks}Nw${p}p${q}q_walks_oriented.json"
WALKS_VECTORIZED="${walkListsDir}/${GRAPH_ID}_${walk_length}Lw${n_walks}Nw${p}p${q}q_walks_vectorized.txt"

# Generate walks step
if [ "$generate_walks" = true ]; then
    if [ ! -f "$WALKS_ORIENTED" ] || [ ! -f "$WALKS_VECTORIZED" ]; then
        python3 workflow/scripts/generate_walks.py "$LINKS" \
        "$walk_length" "$n_walks" "$p" "$q" "$seed" \
        "$WALKS_ORIENTED" "$WALKS_VECTORIZED"
    fi
fi

# Vectorize walks
MODEL="${modelDir}/${GRAPH_ID}_${walk_length}Lw${n_walks}Nw${p}p${q}q_walks.model"
EMBEDDINGS="${embeddingsDir}/${GRAPH_ID}_${walk_length}Lw${n_walks}Nw${p}p${q}q_walks.embeddings"
EDGE_EMBEDDINGS="${edgeEmbeddingsDir}/${GRAPH_ID}_${walk_length}Lw${n_walks}Nw${p}p${q}q_walks.edge_embeddings"

if [ "$embed_nodes" = true ]; then
    if [ ! -f "$MODEL" ] || [ ! -f "$EMBEDDINGS" ] || [ ! -f "$EDGE_EMBEDDINGS" ]; then
        python3 workflow/scripts/vectorize_embed_nodes.py \
        "$WALKS_VECTORIZED" "$MODEL" "$EMBEDDINGS" "$EDGE_EMBEDDINGS" \
        "$dimensions" "$window" "$min_count" "$sg"
    fi
fi

# Check for visualization
PLOT_TITLE="${GRAPH_ID}: walk length ${walk_length}, ${n_walks} walks, p=${p}, q=${q}"
PLOT="${plotsDir}/${GRAPH_ID}_${walk_length}Lw${n_walks}Nw${p}p${q}q_embeddingPlot.png"

if [ "$visualize_embeddings" = true ]; then
    if [ ! -f "$PLOT" ]; then
        python3 workflow/scripts/visualize_embeddings.py \
        "$MODEL" "$EMBEDDINGS" "$LINKS" "$PLOT" "$PLOT_TITLE" \
        "$perplexity" "$n_iter" "$n_components" "$random_state"
    fi
fi
EOF

      done
    done
  done
done
