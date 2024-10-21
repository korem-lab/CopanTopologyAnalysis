from gensim.models import Word2Vec
from gensim.models import KeyedVectors
from sklearn.manifold import TSNE
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import json
import sys

MODEL_F = sys.argv[1]
EMBEDDING_F = sys.argv[2]
WALKS_DICT_F = sys.argv[3]
EMBEDDING_PLOT = sys.argv[4]
PLOT_TITLE = sys.argv[5]
CLUSTER_DICT_F = sys.argv[6]

PERPLEXITY = int(sys.argv[7])
N_ITER = int(sys.argv[8])
N_COMPONENTS = int(sys.argv[9])
RAND_STATE = int(sys.argv[10])

def main():
    model = Word2Vec.load(MODEL_F)

    embedding_kv = KeyedVectors.load(EMBEDDING_F, mmap='r')

    embedding_clusters = []
    node_clusters = []
    cluster_dict = {}

    # for node in walks_dict.keys():
    for node in embedding_kv.key_to_index.keys():
        embeddings = []
        nodes = []
        for similar_node, _ in model.wv.most_similar(node, topn=30):
            nodes.append(similar_node)
            embeddings.append(embedding_kv[similar_node])
        embedding_clusters.append(embeddings)
        node_clusters.append(nodes)
        cluster_dict[node] = nodes
    
    # Save node clusters to a JSON file for easy viewing
    with open(CLUSTER_DICT_F, 'w') as f:
        json.dump(cluster_dict, f, indent=4)
    
    # t-SNE visualization
    embeddings = np.array(embedding_clusters)
    n, m, k = embeddings.shape
    tsne_model_en_2d = TSNE(perplexity=PERPLEXITY, n_components=N_COMPONENTS, init='pca', n_iter=N_ITER, random_state=RAND_STATE)
    embeddings_en_2d = np.array(tsne_model_en_2d.fit_transform(embeddings.reshape(n * m, k))).reshape(n, m, 2)

    tsne_plot_similar_words(PLOT_TITLE, nodes, embeddings_en_2d, node_clusters, 0.7,
                        EMBEDDING_PLOT)

def tsne_plot_similar_words(title, labels, embeddings2d, word_clusters, a, filename):
    plt.figure(figsize=(16, 9))
    colors = cm.rainbow(np.linspace(0, 1, len(labels)))
    for label, embeddings2d, words, color in zip(labels, embeddings2d, word_clusters, colors):
        x = embeddings2d[:, 0]
        y = embeddings2d[:, 1]
        plt.scatter(x, y, c=color, alpha=a, label=label)

        # label each node point
        # for i, word in enumerate(words):
        #     plt.annotate(word, alpha=0.5, xy=(x[i], y[i]), xytext=(5, 2),
        #                  textcoords='offset points', ha='right', va='bottom', size=8)

    plt.legend(loc=4)
    plt.title(title)
    plt.grid(True)
    if filename:
        plt.savefig(filename, format='png', dpi=150, bbox_inches='tight')

if __name__ == '__main__':
    main()
