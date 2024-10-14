#!/bin/bash
#
#SBATCH --job-name=copan_walks
#SBATCH --time=00:10:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=200G
#SBATCH --account pmg

module load python3

python3 scripts/copan_get_graph_link.py {input} {output}
python3 /manitou/pmg/projects/korem_lab/Projects/CopanTopologyAnalysis/Node2Vec/copan_node2vec_walks_addedNoOrientation.py