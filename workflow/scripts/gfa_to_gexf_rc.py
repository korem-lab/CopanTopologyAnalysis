import os
import sys
import tqdm
import math
import networkx as nx
import pandas as pd
import numpy as np
from collections import defaultdict
import workflow.scripts.parse_seq as ps

GFA_F = "copan_0.gfa"
GEXF_F = GFA_F.replace("gfa", "gexf")  # Desired output GEXF file path

def main():
     # noi = pd.read_pickle(os.path.join(DATA, 'nodes_of_interest.pkl'))
    with open(GFA_F, 'r') as f:
        gfa = list(ps.parse_gfa(f))

    G = nx.DiGraph()
    node_lengths = get_seq_length([e for e in gfa if e.type == ps.GFATypes.S])

    # Filter node info to only include nodes present in the GFA
    node_info = pd.DataFrame({e for e in gfa if e.type == ps.GFATypes.S}, columns=["node"])

    print('Build initial graph')
    G = build_initial_graph(gfa, node_info)
    
    edges = 0
    for e in tqdm.tqdm(gfa):
        if e.type != ps.GFATypes.L:
            edges += 1

    print(edges)

    print('Expand graph')
    G = expand_graph(G, node_info, node_lengths)  # Expand the graph

    print('Write')
    nx.write_gexf(G, GEXF_F)  # Save the graph to a GEXF file


def get_seq_length(segments, summary=np.max):
    """
    Calculate the length of sequences in segments and apply a summary function (default is max).
    Returns a dictionary mapping node IDs to their sequence lengths.
    """
    node_groups = defaultdict(list)  # Create a dictionary to group sequence lengths by node ID
    length = dict()  # This will hold the final lengths per node

    # Group sequence lengths by node ID
    for s in segments:
        node_groups[s.nid].append(len(s.seq))

    # Apply the summary function to each group's lengths
        for k, v in node_groups.items():
            length[k] = summary(v)

        return length

def build_initial_graph(gfa, node_info):
    """
    Build an initial directed graph (DiGraph) from GFA entries and node info.
    Edges are assigned weights based on whether both nodes are 'interesting'.
    """

    G = nx.DiGraph()  # Create a directed graph
    for e in tqdm.tqdm(gfa):
        if e.type != ps.GFATypes.S:  # Only consider 'S' entries for nodes
            continue
        G.add_node(e.nid)  # Add nodes to the graph

    # Create edges between nodes based on 'L' entries
    for e in tqdm.tqdm(gfa):
        if e.type != ps.GFATypes.L:  # Only consider 'L' entries for edges
            continue
        len(ps.GFATypes.L)
        G.add_edge(
            e.l_nid, 
            e.r_nid, 
            weight=1
        )

    return G

def expand_graph(G, node_info, node_lengths, keep_self_loops=True, block_size=2500):
    """
    Expand the existing graph by breaking nodes into chains based on their lengths.
    Each node is replaced by a chain of smaller nodes.
    """
    H = G.copy()  # Create a copy of the original graph
    print('Number of nodes before: ', H.number_of_nodes())

    # Iterate through node information to expand nodes into chains
    for i in tqdm.tqdm(node_info.index):
        node = node_info.loc[i, 'node']
        if node not in H:
            continue  # Skip nodes not in the graph

        # Break the node into smaller chains based on its length
        length = node_lengths[node]
        n_blocks = math.ceil(length / block_size)  # Calculate number of blocks
        chain = [f'{node}_{i}' for i in range(n_blocks)]  # Create a chain of node identifiers

        # Get adjacent nodes for the current node
        in_adj = list(H.predecessors(node))  # Incoming edges
        out_adj = list(H.successors(node))  # Outgoing edges
        self_loop = node in out_adj  # Check for self-loops

        # Determine the weight for the edges
        w = 1

        # Remove the original node and add the new chain of nodes
        H.remove_node(node)
        for n in chain:
            H.add_node(n)  # Add each new node in the chain

        # Reconnect the chain with adjacent nodes
        for i_node in in_adj:
            H.add_edge(i_node, chain[0], weight=w)
        for o_node in out_adj:
            H.add_edge(chain[-1], o_node, weight=w)
        for i in range(len(chain) - 1):
            H.add_edge(chain[i], chain[i + 1], weight=w)

        # Optionally keep self-loops if specified
        if keep_self_loops and self_loop:
            H.add_edge(chain[0], chain[1], weight=w)

    print('Number of nodes after: ', H.number_of_nodes())

    return H  # Return the expanded graph


if __name__ == '__main__':
    main()

