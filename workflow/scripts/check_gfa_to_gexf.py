import networkx as nx
import pandas as pd
from itertools import product
import os

GFA_F = "config/copangraphs/dummy.gfa"
GEXF_F = "config/copangraphs/dummy.gexf"

def main():
    gex = nx.read_gexf(GEXF_F)

    print("n nodes:" + str(len(gex.nodes)))
    print("n nodes:" + str(len(gex.edges)))



def get_gfa_features():
    with open(GFA_F, 'r') as f:
        gfa_nodes = []
        n_gfa_edges = 0
        for line in f:
            fields = line.strip().split('\t')

            if fields[0] == 'S':  # node line
                node = fields[1]
                if node not in gfa_nodes:
                    gfa_nodes.append(node)

            elif fields[0] == 'L':  # edge line
                n_gfa_edges += 1
    
    return gfa_nodes, n_gfa_edges

if __name__ == '__main__':
    main()
