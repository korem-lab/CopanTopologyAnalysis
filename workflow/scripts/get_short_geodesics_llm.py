import json
import pandas as pd

NODE_INFO_DICT_F = "workflow/out/link_dicts/dummy_graph_links.json"
GEODESICS_F = "workflow/out/geodesics/dummy_shortGeodesic_llm.csv"

def main():
    with open(NODE_INFO_DICT_F, 'r') as f:
        links_dict = json.load(f)

    rows = []
    max_distance = 2  # Set to 2 for geodesic distances up to 2
    for node in links_dict:
        find_geodesic_neighbors(node, links_dict, max_distance, rows)

    # Convert to DataFrame and save to CSV
    df = pd.DataFrame(rows, columns=["node_1", "node_2", "geodesic_distance"])
    df.to_csv(GEODESICS_F, index=False)
    print(f"CSV file '{GEODESICS_F}' created successfully.")

def find_geodesic_neighbors(start_node, links_dict, max_distance, rows):
    # Set to track unique (node_i, node_j, distance) entries
    visited_pairs = set()

    # Queue for BFS traversal, initialized with (node, distance, orientation)
    queue = [(start_node, 0, None)]  # None for orientation on the first node

    while queue:
        curr_node, distance, prev_orientation = queue.pop(0)

        # Increment the distance as we move to the next level
        next_distance = distance + 1
        if next_distance > max_distance:
            continue

        # Find neighbors with matching bidirectional orientation
        neighbors = [
            (neighbor, links_dict[curr_node]["links"][neighbor]["target_orientation"])
            for neighbor in links_dict[curr_node]["links"]
            if distance == 0 or links_dict[curr_node]["links"][neighbor]["source_orientation"] == prev_orientation
        ]

        # Process each valid neighbor
        for neighbor, orientation in neighbors:
            # Add pair only if it’s unique at this geodesic distance
            pair = (start_node, neighbor, next_distance)
            if pair not in visited_pairs:
                rows.append([start_node, neighbor, next_distance])
                visited_pairs.add(pair)
                # Continue exploring from this neighbor
                queue.append((neighbor, next_distance, orientation))

if __name__ == '__main__':
    main()
