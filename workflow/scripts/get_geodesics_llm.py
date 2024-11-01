import json
import pandas as pd
from collections import deque, defaultdict

NODE_INFO_DICT_F = "workflow/out/link_dicts/dummy_graph_links.json"
GEODESICS_F = "workflow/out/geodesics/dummy_geodesics_llm_trueGeodesic.csv"

def main():
    with open(NODE_INFO_DICT_F, 'r') as f:
        links_dict = json.load(f)

    # Dictionary to store the geodesic distances
    geodesic_distances = []

    # Calculate geodesic distances from each node to every other node
    for start_node in links_dict:
        distances = bfs_with_bidirectionality(start_node, links_dict)
        for end_node, distance in distances.items():
            if distance > 0:  # Ignore self-loops (distance 0)
                geodesic_distances.append([start_node, end_node, distance])

    # Convert to DataFrame and save to CSV
    df = pd.DataFrame(geodesic_distances, columns=["node_1", "node_2", "geodesic_distance"])
    df.to_csv(GEODESICS_F, index=False)
    print(f"CSV file '{GEODESICS_F}' created successfully.")

def bfs_with_bidirectionality(start_node, links_dict):
    # Initialize distances dictionary with infinity
    distances = defaultdict(lambda: float('inf'))
    distances[start_node] = 0  # Distance to itself is 0

    # Queue for BFS: stores (current node, current distance, previous orientation)
    queue = deque([(start_node, 0, None)])
    
    # Track visited nodes to avoid re-processing
    visited = {start_node}

    while queue:
        curr_node, curr_distance, prev_orientation = queue.popleft()

        # Next distance level
        next_distance = curr_distance + 1

        # Explore each neighbor with correct orientation
        for neighbor, link_info in links_dict[curr_node]["links"].items():
            target_orientation = link_info["target_orientation"]
            source_orientation = link_info["source_orientation"]

            # Check bidirectional constraint for non-root nodes
            if prev_orientation is None or source_orientation == prev_orientation:
                if neighbor not in visited or next_distance < distances[neighbor]:
                    distances[neighbor] = next_distance
                    visited.add(neighbor)
                    # Add the neighbor to the queue, passing its orientation for the next level
                    queue.append((neighbor, next_distance, target_orientation))

    return distances

if __name__ == '__main__':
    main()
