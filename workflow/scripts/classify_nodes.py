import json
import csv

LINKS_F = "workflow/out/link_dicts/copan_0_links.json"
DEGREE_CLASS_F = "workflow/out/node_classification/copan_0_node_degree_classification.json"
CSV_F = "workflow/out/node_classification/copan_0_node_degree_classification.csv"

def main():
    with open(LINKS_F, 'r') as f:
        links_dict = json.load(f)

    # # for a dict
    # degree_classes_dict = {}
    # for node in links_dict.keys():
    #     degree = len(links_dict[node]["links"])
        
    #     if degree not in degree_classes_dict.keys():
    #         degree_classes_dict[degree] = [node]
        
    #     else:
    #         degree_classes_dict[degree].append(node)

    # with open(DEGREE_CLASS_F, 'w') as f:
    #     json.dump(degree_classes_dict, f, indent=4)

    # for csv
    degree_classes_csv = []
    for node in links_dict:
        degree = len(links_dict[node]["links"])  # Calculate the degree directly
        degree_classes_csv.append((node, degree)) 

    with open(CSV_F, mode='w', newline='') as f:
        # Write to CSV file
        csv_writer = csv.writer(f)

        # Write the header
        csv_writer.writerow(['node', 'degree'])

        # Write all data rows in one go
        csv_writer.writerows(degree_classes_csv)


if __name__ == '__main__':
    main()
