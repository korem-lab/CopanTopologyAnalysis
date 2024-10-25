from gensim.models import Word2Vec
from gensim.models import KeyedVectors
import json
import sys


MODEL_F = sys.argv[1]
EMBEDDING_F = sys.argv[2]

CLUSTER_DICT_F = sys.argv[3]  


def main():
    model = Word2Vec.load(MODEL_F)

    embedding_kv = KeyedVectors.load(EMBEDDING_F, mmap='r')

    cluster_dict = {}

    for node in embedding_kv.key_to_index.keys():
        nodes = []
        for similar_node, _ in model.wv.most_similar(node, topn=30):
            nodes.append(similar_node)
        cluster_dict[node] = nodes
    
    # Save node clusters to a JSON file for easy viewing
    with open(CLUSTER_DICT_F, 'w') as f:
        json.dump(cluster_dict, f, indent=4)
    

if __name__ == '__main__':
    main()
