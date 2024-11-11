"""
Check that all nodes in copangraph are accounted for in every file in the node2vec pipeline.
"""
import json
from gensim.models import Word2Vec
from gensim.models import KeyedVectors

GRAPH_F = "config/copangraphs/sample_1_0_02.gfa"

LINKS_F = "workflow/out/link_dicts/sample_1_0_02_links.json"
LINKS_CHECK_F = "workflow/out/validation/nodes_not_in_links.txt"

WALKS_ORIENTED_F = "workflow/out/walk_dicts_oriented/sample_1_0_02_30Lw10Nw1.0p1.0q50k_walks_oriented.json"
WALKS_VECTORIZED_F = "workflow/out/walk_lists_vectorized/sample_1_0_02_30Lw10Nw1.0p1.0q50k_walks_vectorized.txt"
WALKS_ORIENTED_CHECK_F = "workflow/out/validation/nodes_not_in_walkDict_sample_1_0_02.txt"
WALKS_VECTORIZED_CHECK_F = "workflow/out/validation/nodes_not_in_walkList_sample_1_0_02.txt"

EMBEDDINGS_F = "workflow/out/vectorization_model/embeddings/sample_1_0_02_30Lw10Nw1.0p1.0q50k_walks.embeddings"
MODEL_F = "workflow/out/vectorization_model/models/sample_1_0_02_30Lw10Nw1.0p1.0q50k_walks.model"
EMBEDDINGS_CHECK_F = "workflow/out/validation/nodes_not_in_embeddings_sample_1_0_02"
MODEL_CHECK_F = "workflow/out/validation/nodes_not_in_model_sample_1_0_02"

CLUSTER_F = "workflow/out/cluster_dicts/sample_1_0_02_30Lw10Nw1.0p1.0q50k_30perp1000iter_clusters.json"
CLUSTER_CHECK_F = "workflow/out/validation/nodes_not_in_clusterDict_sample_1_0_02.txt"


def main():
    nodes = get_nodes(GRAPH_F)
    print("Number of nodes:" + str(len(set(nodes))))

    link_nodes = check_links(nodes, LINKS_F, LINKS_CHECK_F)
    print("Number of nodes in links dict:" + str(len(set(link_nodes))))

    walk_nodes = check_walks(nodes, WALKS_ORIENTED_F, WALKS_VECTORIZED_F, WALKS_ORIENTED_CHECK_F, WALKS_VECTORIZED_CHECK_F)
    walk_dict_nodes = walk_nodes[0]
    walk_list_nodes = walk_nodes[1]
    print("Number of nodes in walks dict:" + str(len(set(walk_dict_nodes))))
    print("Number of nodes in walks list:" + str(len(set(walk_list_nodes))))

    embedding_nodes = check_embeddings(nodes, walk_dict_nodes, walk_list_nodes, EMBEDDINGS_F, MODEL_F, EMBEDDINGS_CHECK_F, MODEL_CHECK_F)
    model_nodes = embedding_nodes[0]
    emb_nodes = embedding_nodes[1]
    print("Number of nodes in model:" + str(len(set(model_nodes))))
    print("Number of nodes in walks list:" + str(len(set(emb_nodes))))

    cluster_nodes = check_node_clusters(nodes, CLUSTER_F, CLUSTER_CHECK_F)
    print("Number of nodes in clusters dict:" + str(len(set(cluster_nodes))))


def get_nodes(graph_file):
    nodes = []
    with open(graph_file, 'r') as f:
        for line in f:
            line = line.strip()
            fields = line.strip().split('\t')
            if line.startswith("S"):
                node = fields[1]  # Get the node id (the second field)
                nodes.append(node)  # Add it to the list

    return nodes


def write_check_file(nodes, check_f):
    with open(check_f, 'w') as f:
            for node in nodes:
                f.write(str(node) + "\n")


def check_two_lists(nodes, check_list, check_f):
    nodes_not_in_list = [node for node in nodes if node not in check_list]
    
    if len(nodes_not_in_list) > 0:
        write_check_file(nodes_not_in_list, check_f)


def check_links(nodes, links_f, nodes_not_in_links_f):
    with open(links_f, 'r') as f:
        links_dict = json.load(f)
    
    links_nodes = list(links_dict.keys())

    check_two_lists(nodes, links_nodes, nodes_not_in_links_f)

    return links_nodes


def check_walks(nodes, walks_oriented_f, walks_vectorized_f, nodes_not_in_dict_f, nodes_not_in_list_f):
    with open(walks_oriented_f, 'r') as f:
        walks_dict = json.load(f)
    
    unoriented_nodes = []
    with open(walks_vectorized_f, 'r') as f:
        for line in f:
            line_nodes = line.strip().split(',')
            unoriented_nodes.extend(line_nodes)

    oriented_nodes = list(walks_dict.keys())
    unoriented_nodes = list(set(unoriented_nodes))

    check_two_lists(nodes, oriented_nodes, nodes_not_in_dict_f)
    check_two_lists(nodes, unoriented_nodes, nodes_not_in_list_f)
    
    return oriented_nodes, unoriented_nodes


def check_embeddings(nodes, walk_dict_nodes, walk_list_nodes, embeddings_f, model_f, emb_check_f, model_check_f):
    model = Word2Vec.load(model_f)
    model_nodes = list(model.wv.key_to_index.keys())

    embedding_kv = KeyedVectors.load(embeddings_f, mmap='r')
    embedding_nodes = list(embedding_kv.key_to_index.keys())
    
    check_two_lists(nodes, model_nodes, model_check_f + "_graphNodes.txt")
    check_two_lists(nodes, embedding_nodes, emb_check_f + "_graphNodes.txt")

    check_two_lists(walk_dict_nodes, model_nodes, model_check_f + "_walkDictNodes.txt")
    check_two_lists(walk_dict_nodes, embedding_nodes, emb_check_f + "_walkDictNodes.txt")

    check_two_lists(walk_list_nodes, model_nodes, model_check_f + "_walkListNodes.txt")
    check_two_lists(walk_list_nodes, embedding_nodes, emb_check_f + "_walkListNodes.txt")

    return model_nodes, embedding_nodes

def check_node_clusters(nodes, cluster_dict_f, cluster_check_f):
    with open(cluster_dict_f, 'r') as f:
        cluster_dict = json.load(f)

    cluster_nodes = list(cluster_dict.keys())
    
    check_two_lists(nodes, cluster_nodes, cluster_check_f)

    return cluster_nodes


if __name__ == '__main__':
    main()
