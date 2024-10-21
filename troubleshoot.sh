#!/bin/bash
#
#SBATCH --job-name=troubleshoot
#SBATCH --output=workflow/out/job_out/troubleshoot_%j.out  # Standard output
#SBATCH --error=workflow/out/job_out/troubleshoot_%j.err    # Standard error
#SBATCH --time=00:05:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=10G
#SBATCH --account pmg

# Load configuration
source config/config.cfg

GRAPH_ID="copan_0"

WALKS_ORIENTED="${walkDictsDir}/${GRAPH_ID}_${walk_length}Lw${n_walks}Nw${p}p${q}q_walks_oriented.json"
WALKS_VECTORIZED="${walkListsDir}/${GRAPH_ID}_${walk_length}Lw${n_walks}Nw${p}p${q}q_walks_vectorized.txt"

echo "graph $GRAPH_ID"

echo "walkListsDir: $walkListsDir"
echo "GRAPH_ID: $GRAPH_ID"
echo "walk_length: $walk_length"
echo "n_walks: $n_walks"
echo "p: $p"
echo "q: $q"

echo $WALKS_ORIENTED
echo $WALKS_VECTORIZED
<<<<<<< HEAD

=======
>>>>>>> addc90a (bash script edits)
# Define parameter values for looping
p_values=(0.5)
q_values=(0.5)
walk_lengths=(30)
n_walks_values=(10)

# Loop over the combinations of parameters
for walk_length in "${walk_lengths[@]}"; do
    for n_walks in "${n_walks_values[@]}"; do
        for p in "${p_values[@]}"; do
            for q in "${q_values[@]}"; do

                WALKS_ORIENTED="${walkDictsDir}/${GRAPH_ID}_${walk_length}Lw${n_walks}Nw${p}p${q}q_walks_oriented.json"
                WALKS_VECTORIZED="${walkListsDir}/${GRAPH_ID}_${walk_length}Lw${n_walks}Nw${p}p${q}q_walks_vectorized.txt"

                if [ "$generate_walks" = true ]; then
                    if [ ! -f "$WALKS_ORIENTED" ] || [ ! -f "$WALKS_VECTORIZED" ]; then
                        echo hi
                        echo "path $WALKS_ORIENTED"
		echo hi
		echo $WALKS_ORIENTED
		echo $WALKS_VECTORIZED
                if [ "$generate_walks" = true ]; then
                    if [ ! -f "$WALKS_ORIENTED" ] || [ ! -f "$WALKS_VECTORIZED" ]; then
                        echo hi again
			echo "path $WALKS_ORIENTED"
                    fi 
                fi 
            done 
        done 
    done
done


