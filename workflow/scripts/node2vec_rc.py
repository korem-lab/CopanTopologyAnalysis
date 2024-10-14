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

def main():
    with open(GFA_F, 'r') as f:


        # gfa = list(ps.parse_gfa(f))
        parse_gfa(f)

        # node_info = pd.DataFrame({e for e in gfa if e.type == ps.GFATypes.S}, columns=["node"])

    # print(node_info.head(4))

def parse_gfa(fs, as_fasta=False):
    for line in fs:
        print(line)
        if line[0] == GFATypes.H:
            continue
        if line[0] == GFATypes.S:
            segment = split
            
    


# def parse_gfa(fs, as_fasta=False):
#     for line in fs:
#         if line[0] == GFATypes.H:
#             continue
#         if not as_fasta:
#             yield get_gfa_element(line)
#         else:
#             e = get_gfa_element(line)
#             if e.type == GFATypes.S:
#                 yield Fasta(e.nid, e.seq)


# def get_gfa_element(line):
#     if line[0] == GFATypes.S:
#         return GFASegment(*line.strip().split())
#     elif line[0] == GFATypes.L:
#         return GFALine(*line.strip().split())
    

class GFATypes:
    S = 'S'
    L = 'L'
    H = 'H'

if __name__ == '__main__':
    main()