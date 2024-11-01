import json
import pandas as pd
import numpy as np

NODE_INFO_DICT_F = "workflow/out/link_dicts/dummy_graph_links.json"
GEODESICS_F = "workflow/out/geodesics/dummy_shortGeodesic.csv"

def main():
    with open(NODE_INFO_DICT_F, 'r') as f:
        links_dict = json.load(f)

    # Iterate over each node and its links
    rows = []

    for node_1 in links_dict.keys():
        # FOR GEODESICS = 1
        neighbors = list(links_dict[node_1]["links"].keys())

        # print("node 1: ", str(node_1))
        # print("neighbors: ", str(neighbors))

        for node_2 in neighbors:
            # Append the pair with geodesic distance 1
            geodesic  = 1
            rows.append([node_1, node_2, geodesic])

            node_2_or = links_dict[node_1]["links"][node_2]["target_orientation"]

            # GEODESICS = 2
            # get neighbors of node 2 that match bidirected orientation
            second_neighbors = [linked_node for linked_node in links_dict[node_2]["links"] if links_dict[node_2]["links"][linked_node]["source_orientation"] == node_2_or]

            if len(second_neighbors) == 0:
                # print("no second neighbors!")
                continue
            # print("node 2: ", str(node_2))
            # print("node 2 orientation:" + str(node_2_or))
            # print("2nd neighbors: ", str(second_neighbors))
    
            # filter second_neighbors for ones that are in the first neighbors (don't need to pay attention to bidirectionlity)
            second_neighbors_not_in_original_neighbors = list(set(second_neighbors) - set(neighbors))

            for node_3 in second_neighbors_not_in_original_neighbors:
                # print("node3:" + node_3)
                geodesic = 2
                rows.append([node_1, node_3, geodesic])

                node_3_or = links_dict[node_2]["links"][node_3]["target_orientation"]

                # GEODESICS = 2
                # get neighbors of node 2 that match bidirected orientation
                third_neighbors = [linked_node for linked_node in links_dict[node_3]["links"] if links_dict[node_3]["links"][linked_node]["source_orientation"] == node_3_or]

                if len(third_neighbors) == 0:
                    # print("no second neighbors!")
                    continue
                # print("node 2: ", str(node_2))
                # print("node 2 orientation:" + str(node_2_or))
                # print("2nd neighbors: ", str(second_neighbors))
        
                # filter second_neighbors for ones that are in the first neighbors (don't need to pay attention to bidirectionlity)
                third_neighbors_not_in_previous_neighbors = list(set(third_neighbors) - set(second_neighbors) - set(neighbors))

                for node_4 in third_neighbors_not_in_previous_neighbors:
                    # print("node3:" + node_3)
                    geodesic = 3
                    rows.append([node_1, node_4, geodesic])

    
    df = pd.DataFrame(rows, columns=["node_1", "node_2", "geodesic_distance"])
    df.to_csv(GEODESICS_F, index=False)


if __name__ == '__main__':
    main()

    
