import json
import numpy as np
import sys

NODE_INFO_DICT_F = sys.argv[1]

# set walk params
walk_length = int(sys.argv[2]) # number of nodes in walk (doesn't include starting node)
n_walks = int(sys.argv[3]) # number of walks to perform per node
p = float(sys.argv[4])
q = float(sys.argv[5])
SEED = int(sys.argv[6])

WALKS_DICT_F = sys.argv[7]
WALKS_LIST_F = sys.argv[8]

# Iter through nodes in node_dict
def main():
    with open(NODE_INFO_DICT_F, 'r') as f:
        node_dict = json.load(f)

    walks_dict_wOrientation = {}
    walks_list_noOrientation = []

    for start_node in node_dict.keys():
        seed = SEED  # set seed for later use of random.choice() for reproducibility 

        walk_counter = 0
        walks_dict_wOrientation[start_node] = []
        

        walks = take_walk(node_dict, walks_dict_wOrientation, start_node, walk_counter, seed, walks_list_noOrientation)
        walks_dict_wOrientation = walks[0]
        walks_list_noOrientation = walks[1]
    
    
    with open(WALKS_DICT_F, 'w') as f:
        json.dump(walks_dict_wOrientation, f, indent=4)
    
    with open(WALKS_LIST_F, 'w') as f:
        for walk in walks_list_noOrientation:
            # Join the elements of the nested list into a single string
            line = ','.join(map(str, walk))  # Convert each element to a string and join with a comma
            f.write(line + '\n')  # Write the line to the file and add a newline
        

def take_walk(node_dict, walks_dict_wOrientation, start_node, walk_counter, seed, walks_list_noOrientation):
    while walk_counter < n_walks:
        seed += 1  # don't want to replicate walks, so changing seed for each walk
        node_counter = 0

        # pick random link from list of links for this start node
        neighbors = list(node_dict[start_node]["links"].keys())

        if len(neighbors) == 0:
            break

        else: 
            # for the first step in the path, we can ignore the orientation of the first node. hence, why we call take_step here
            # np.random.seed(seed)
            next_node = np.random.choice(neighbors)
            next_node_orientation = node_dict[start_node]["links"][next_node]["target_orientation"]

            start_node_orientation = node_dict[start_node]["links"][next_node]["source_orientation"]

            path_wOrientation = [[start_node, start_node_orientation], [next_node, next_node_orientation]]
            path_noOrientation = [start_node, next_node]

            node_counter += 1

            paths = take_step(node_dict, next_node, next_node_orientation, node_counter, walk_counter, start_node, start_node_orientation, path_wOrientation, path_noOrientation, p, q, seed)
            path_wOrientation = paths[0]
            path_noOrientation = paths[1]
            walk_counter = paths[2]

        walks_dict_wOrientation[start_node].append(path_wOrientation)
        walks_list_noOrientation.append(path_noOrientation)

    return [walks_dict_wOrientation, walks_list_noOrientation]
    

def take_step(node_dict, curr_node, curr_orientation, node_counter, walk_counter, prev_node, prev_orientation, path_wOrientation, path_noOrientation, p, q, seed):
    while node_counter < walk_length -1:
        transition_probabilities = {}

        curr_node_neighbors = [linked_node for linked_node in node_dict[curr_node]["links"] if node_dict[curr_node]["links"][linked_node]["source_orientation"] == curr_orientation]
        prev_node_neighbors = [linked_node for linked_node in node_dict[prev_node]["links"] if node_dict[prev_node]["links"][linked_node]["source_orientation"] == prev_orientation]


        if len(curr_node_neighbors) == 0:
            walk_counter += 1

            return [path_wOrientation, path_noOrientation, walk_counter]

        else: 
            for neighbor in curr_node_neighbors:
                if neighbor == prev_node:
                    # return to previous node
                    transition_probabilities[neighbor] = 1/p
                elif neighbor in prev_node_neighbors:
                    # neighbor of current node is also neighbor to previous node
                    transition_probabilities[neighbor] = 1.0
                else:
                    # neighbor is not previous node and not neighbor to previous node
                    transition_probabilities[neighbor] = 1/q

            # normalize probabilities
            total_probabilities = sum(transition_probabilities.values())  # also referred to as "Z" value in the literature
            normalized_transition_probabilities = {k: v / total_probabilities for k, v in transition_probabilities.items()}

            # np.random.seed(seed)
            next_node = np.random.choice(list(normalized_transition_probabilities.keys()), p=list(normalized_transition_probabilities.values()))
            next_orientation = node_dict[curr_node]["links"][next_node]["target_orientation"]

            path_wOrientation.append([next_node, next_orientation])
            path_noOrientation.append(next_node)

            node_counter += 1

            prev_node = curr_node
            prev_orientation = curr_orientation

            curr_node = next_node
            curr_orientation = next_orientation

    walk_counter += 1

    return [path_wOrientation, path_noOrientation, walk_counter]


if __name__ == '__main__':
    main()
    
