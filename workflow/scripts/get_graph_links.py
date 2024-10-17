import re
import json
import sys

GFA_F = sys.argv[1]
NODE_INFO_DICT = sys.argv[2]

def main():
    n_seg = 0
    n_links = 0
    n_node = 0
    node_dict = {}

    with open(GFA_F, 'r') as f:
        for line in f:

            line = re.split("\t|:", line)

            if line[0] == "S":
                node = line[1]
                seq = line[2]
                contig = line[5]
                sample = line[6]
                source_position = line[8]
                end_position = line[9]
                orientation = line[10].strip()
                n_seg +=1

                if node not in node_dict.keys():
                    node_dict[node]= {"seqs": [seq], 
                                    "contigs": [contig], 
                                    "samples": [sample], 
                                    "orientations": [orientation], 
                                    "links":{}}
                    n_node += 1
                elif node in node_dict.keys():
                    # possible issue: this allows for redundant info in the nested dictionaries if there are multiple seqs 
                    # belonging to the same node that also come from the same sample or contig
                    node_dict[node]["seqs"].append(seq)
                    node_dict[node]["contigs"].append(contig)
                    node_dict[node]["samples"].append(sample)
                    node_dict[node]["orientations"].append(orientation) 

            
            if line[0] == "L":
                n_links += 1
                node_1 = line[1]
                node_1_orientation = line[2]
                node_2 = line[3]
                node_2_orientation = line[4]

                if node_1 in node_dict.keys():
                    node_dict[node_1]["links"][node_2] = {"target_orientation": node_2_orientation, 
                                                            "source_orientation": node_1_orientation}
                if node_2 in node_dict.keys():
                    node_1_revcomp_orientation = reverse_complement(node_1_orientation)
                    node_2_revcomp_orientation = reverse_complement(node_2_orientation)
                    # orientation for the target and source are flipped because this represents the reverse complement link
                    node_dict[node_2]["links"][node_1] = {"target_orientation": node_1_revcomp_orientation, 
                                                            "source_orientation": node_2_revcomp_orientation}
    
    with open(NODE_INFO_DICT, 'w') as f:
        json.dump(node_dict, f, indent=4)


def reverse_complement(forward_orientation):
    if forward_orientation == "-":
        return "+"
    else:
        return "-"


if __name__ == '__main__':
    main()
