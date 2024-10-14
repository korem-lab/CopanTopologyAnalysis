import random
import json
import numpy as np

NODE_INFO_DICT_F = "copan_0_links.json"
OUTPUT_DIR = "walks"
    
# set walk params
walk_length = 3 # number of nodes in walk (doesn't include starting node)
n_walks = 1 # number of walks to perform per node
p = 1
q = 1

# name output file for walks_dict to include the walk length ("Lw") and number of walks ("Nw")
path_addon = str(walk_length) + "Lw" + str(n_walks) + "Nw" + "_walks"

WALKS_DICT_F = OUTPUT_DIR + "/" + NODE_INFO_DICT_F.replace("links", path_addon)


# Iter through nodes in node_dict
def main():
    with open(NODE_INFO_DICT_F, 'r') as f:
        node_dict = json.load(f)

    walks_dict = {}

    for start_node in node_dict.keys():
        walk_counter = 0
        walks_dict[start_node] = []

        walks_dict = take_walk(node_dict, walks_dict, start_node, walk_counter)
    
    
    with open(WALKS_DICT_F, 'w') as f:
        json.dump(walks_dict, f, indent=4)


def take_walk(node_dict, walks_dict, start_node, walk_counter):
    while walk_counter < n_walks:
        node_counter = 0

        # pick random link from list of links for this start node
        neighbors = list(node_dict[start_node]["links"].keys())

        if len(neighbors) == 0:
            break

        else: 
            # for the first step in teh path, we can ignore the orientation of the first node. hence, why we call take_step here
            next_node = random.choice(neighbors)
            next_node_orientation = node_dict[start_node]["links"][next_node]["target_orientation"]

            start_node_orientation = node_dict[start_node]["links"][next_node]["source_orientation"]

            path = [[start_node, start_node_orientation], [next_node, next_node_orientation]]

            node_counter += 1

            path_result = take_step(node_dict, walks_dict, next_node, next_node_orientation, node_counter, walk_counter, start_node, start_node_orientation, path, p, q)
            path = path_result[0]
            walk_counter = path_result[1]

        walks_dict[start_node].append(path)

    return walks_dict
    

def take_step(node_dict, walks_dict, curr_node, curr_orientation, node_counter, walk_counter, prev_node, prev_orientation, path, p, q):
    while node_counter < walk_length -1:
        transition_probabilities = {}

        curr_node_neighbors = [linked_node for linked_node in node_dict[curr_node]["links"] if node_dict[curr_node]["links"][linked_node]["source_orientation"] == curr_orientation]
        prev_node_neighbors = [linked_node for linked_node in node_dict[prev_node]["links"] if node_dict[prev_node]["links"][linked_node]["source_orientation"] == prev_orientation]


        if len(curr_node_neighbors) == 0:
            walk_counter += 1
            return [path, walk_counter]

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


            next_node = np.random.choice(list(normalized_transition_probabilities.keys()), p=list(normalized_transition_probabilities.values()))
            next_orientation = node_dict[curr_node]["links"][next_node]["target_orientation"]

            path.append([next_node, next_orientation])

            node_counter += 1

            prev_node = curr_node
            prev_orientation = curr_orientation

            curr_node = next_node
            curr_orientation = next_orientation

    walk_counter += 1
    return [path, walk_counter]


if __name__ == '__main__':
    main()
    
