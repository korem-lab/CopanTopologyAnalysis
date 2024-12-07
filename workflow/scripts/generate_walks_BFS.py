import json
import numpy as np
import sys

NODE_INFO_DICT_F = sys.argv[1]
NEIGHBORS_DICT = sys.argv[2]

# set walk params
walk_length = int(sys.argv[3]) # number of nodes in walk (doesn't include starting node)
n_walks = int(sys.argv[4]) # number of walks to perform per node
p = float(sys.argv[5])
q = float(sys.argv[6])
SEED = int(sys.argv[7])

WALKS_LIST_F = sys.argv[8]

# Iter through nodes in node_dict
def main():
    with open(NODE_INFO_DICT_F, 'r') as f:
        node_dict = json.load(f)

    with open(NEIGHBORS_DICT, 'r') as f:
        neighbors_dict = json.load(f)

    walks_list_noOrientation = []

    for start_node in node_dict.keys():
        for walk_counter in range(n_walks):
            # Set seed for reproducibility
            np.random.seed(SEED + walk_counter)

            path_noOrientation = take_walk(node_dict, start_node, neighbors_dict, p, q, walk_length, walks_list_noOrientation)
            
            walks_list_noOrientation.append(path_noOrientation)

    with open(WALKS_LIST_F, 'w') as f:
        for walk in walks_list_noOrientation:
            # Join the elements of the nested list into a single string
            line = ','.join(map(str, walk))  # Convert each element to a string and join with a comma
            f.write(line + '\n')  # Write the line to the file and add a newline
        
def take_walk(node_dict, start_node, neighbors_dict, p, q, walk_length):
    path_noOrientation = []

    curr_node = start_node
    curr_orientation = None  # Starting orientation is irrelevant
    prev_node = None

    for step in range(walk_length):
        # Get valid neighbors
        curr_node_neighbors = [
            neighbor for neighbor, link in node_dict[curr_node]["links"].items()
            if curr_orientation is None or link["source_orientation"] == curr_orientation
        ]

        # Update paths
        if step == 0:  # First step
            path_noOrientation.append(curr_node)
        else:
            path_noOrientation.append(curr_node)

        # Terminate if no neighbors
        if not curr_node_neighbors:
            break

        # Calculate transition probabilities
        transition_probabilities = {}
        for neighbor in curr_node_neighbors:
            distant_neighbors = neighbors_dict[neighbor]

            if neighbor == prev_node:
                transition_probabilities[neighbor] = 1 / p
            elif prev_node in distant_neighbors:
                transition_probabilities[neighbor] = 1 / p
            else:
                transition_probabilities[neighbor] = 1 / q

        # Normalize probabilities
        total_probabilities = sum(transition_probabilities.values())
        normalized_transition_probabilities = {
            k: v / total_probabilities for k, v in transition_probabilities.items()
        }

        # Select next node
        next_node = np.random.choice(
            list(normalized_transition_probabilities.keys()),
            p=list(normalized_transition_probabilities.values())
        )
        next_orientation = node_dict[curr_node]["links"][next_node]["target_orientation"]

        # Update for next step
        prev_node = curr_node
        curr_node = next_node
        curr_orientation = next_orientation

    return path_noOrientation


if __name__ == '__main__':
    main()
    
