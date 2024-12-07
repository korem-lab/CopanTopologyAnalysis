import json
import numpy as np
import sys

NODE_INFO_DICT_F = sys.argv[1]
walk_length = int(sys.argv[2]) # number of nodes in walk (doesn't include starting node)
n_walks = int(sys.argv[3]) # number of walks to perform per node
SEED = int(sys.argv[4])
NEIGHBORS_DICT = sys.argv[5]

# Iter through nodes in node_dict
def main():
    with open(NODE_INFO_DICT_F, 'r') as f:
        node_dict = json.load(f)

    neighbors_dict = {node: set() for node in node_dict}

    for start_node in node_dict.keys():
        for walk_counter in range(n_walks):
            # Set seed for reproducibility
            np.random.seed(SEED + walk_counter)

            take_walk(node_dict, start_node, neighbors_dict)

    neighbors_dict = {node: list(neighbors) for node, neighbors in neighbors_dict.items()}

    with open(NEIGHBORS_DICT, 'w') as f:
        json.dump(neighbors_dict, f, indent=4)

def take_walk(node_dict, start_node, neighbors_dict):
    step = 0
    current_node = start_node
    current_orientation = None  # First step ignores orientation

    while step < walk_length:
        # Get neighbors based on orientation
        neighbors = [
            neighbor for neighbor, link in node_dict[current_node]["links"].items()
            if current_orientation is None or link["source_orientation"] == current_orientation
        ]

        # Update neighbors dictionary
        neighbors_dict[start_node].update(neighbors)

        # Terminate if no neighbors
        if not neighbors:
            break

        # Choose the next node randomly
        next_node = np.random.choice(neighbors)
        next_orientation = node_dict[current_node]["links"][next_node]["target_orientation"]

        # Update current state and increment step count
        current_node = next_node
        current_orientation = next_orientation
        step += 1
        

if __name__ == '__main__':
    main()
    
