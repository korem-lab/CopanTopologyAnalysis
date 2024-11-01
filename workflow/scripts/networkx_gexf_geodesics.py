import networkx as nx
import pandas as pd
from itertools import product
import os

GFA_F = "config/copangraphs/copan_0.gfa"
# GFA_F = "config/copangraphs/dummy.gfa"
GEXF_F = GFA_F.replace("gfa", "gexf")  # Desired output GEXF file path

OUTDIR = "workflow/out/geodesics/"
basename = os.path.basename(GFA_F)
GEODESICS_F = OUTDIR + os.path.splitext(basename)[0] + "_geodesics.csv"

def main():
    G = make_digraph()
    print("Done with creating GEXF.")
    # G = nx.read_gexf(GEXF_F)

    get_geodesics(G)
    print("Done with geodesics.")


def make_digraph():
    G = nx.DiGraph()

    with open(GFA_F, 'r') as f:
        for line in f:
            fields = line.strip().split('\t')

            if fields[0] == 'S':  # Segment line
                node = fields[1]
                # print("node" + str(node))

                G.add_node(node)
            elif fields[0] == 'L':  # Link line
                src, src_ori = fields[1], fields[2]
                targ, targ_ori = fields[3], fields[4]
                
                # REDUNDANT -- does this actuallyh encode for bidirectionality????
                # Add directed edges based on the specified orientation
                if src_ori == '+' and targ_ori == '+':
                    G.add_edge(src, targ)   # forward-forward direction
                elif src_ori == '+' and targ_ori == '-':
                    G.add_edge(src, targ)   # forward-reverse direction
                elif src_ori == '-' and targ_ori == '+':
                    G.add_edge(targ, src)   # reverse-forward direction
                elif src_ori == '-' and targ_ori == '-':
                    G.add_edge(targ, src)   # reverse-reverse direction
    
    nx.write_gexf(G, GEXF_F)
                
    return G


def get_geodesics(G):
    geodesic_data = []
    nodes = list(G.nodes)

    for node_i, node_j in product(nodes, repeat=2):
        try:
            geodesic_ij = nx.shortest_path_length(G, source=node_i, target=node_j)
        except nx.NetworkXNoPath:
            geodesic_ij = "NA"  # No path exists in the directed graph

        geodesic_data.append({'node_i': node_i, 'node_j': node_j, 'geodesic_ij': geodesic_ij})

    df = pd.DataFrame(geodesic_data)
    df.to_csv(GEODESICS_F, index=False)


if __name__ == '__main__':
    main()

