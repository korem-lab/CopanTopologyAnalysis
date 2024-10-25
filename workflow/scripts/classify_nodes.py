import json

LINKS_F = "workflow/out/link_dicts/copan_0_links.json"
DEGREE_CLASS_F = "workflow/out/node_classification/copan_0_node_degree_classification.json"

def main():
    with open(LINKS_F, 'r') as f:
        links_dict = json.load(f)
    
    degree_classes_dict = {}

    for node in links_dict.keys():
        degree = len(links_dict[node]["links"].keys())
        
        if degree not in degree_classes_dict.keys():
            degree_classes_dict[degree] = [node]
        
        else:
            degree_classes_dict[degree].append(node)
    
    with open(DEGREE_CLASS_F, 'w') as f:
        json.dump(degree_classes_dict, f, indent=4)


if __name__ == '__main__':
    main()
