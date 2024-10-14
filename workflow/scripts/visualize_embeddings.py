# import sys
# import matplotlib.pyplot as plt

# from sklearn.manifold import TSNE
# from sklearn.model_selection import train_test_split
# from sklearn.linear_model import LogisticRegressionCV
# from sklearn.metrics import accuracy_score

# import os
# import networkx as nx
# import numpy as np
# import pandas as pd

# from stellargraph.data import BiasedRandomWalk
# from stellargraph import StellarGraph
# from stellargraph import datasets
# from IPython.display import display, HTML

from gensim.models import Word2Vec
import random
import os

# import numpy as np
# import pandas as pd
# from matplotlib import pyplot as plt
import tensorflow as tf
from tensorflow import keras

MODEL_F = "workflow/out/vectorization_model/models/dummy_graph_1Lw10Nw1p1q_walks.model"

def main():
    model = Word2Vec.load(MODEL_F)
    most_sim = model.wv.most_similar("A")
    print(most_sim)

    embedding_clusters = []
    node_clusters = []
    for word in keys:
        embeddings = []
        words = []
        for similar_word, _ in model.most_similar(word, topn=30):
            words.append(similar_word)
            embeddings.append(model[similar_word])
        embedding_clusters.append(embeddings)
        word_clusters.append(words)

    # dataset = datasets.Cora()
    # display(HTML(dataset.description))
    # G, node_subjects = dataset.load(largest_connected_component_only=True)

    # # Retrieve node embeddings and corresponding subjects
    # node_ids = model.wv.index2word  # list of node IDs
    # node_embeddings = (
    #    model.wv.vectors
    # )  
    # # numpy.ndarray of size number of nodes times embeddings dimensionality
    # node_targets = node_subjects[[int(node_id) for node_id in node_ids]]

    # # Apply t-SNE transformation on node embeddings
    # tsne = TSNE(n_components=2)
    # node_embeddings_2d = tsne.fit_transform(node_embeddings)

    # # draw the points
    # alpha = 0.7
    # label_map = {l: i for i, l in enumerate(np.unique(node_targets))}
    # node_colours = [label_map[target] for target in node_targets]

    # plt.figure(figsize=(10, 8))
    # plt.scatter(
    #     node_embeddings_2d[:, 0],
    #     node_embeddings_2d[:, 1],
    #     c=node_colours,
    #     cmap="jet",
    #     alpha=alpha,
    # )

    # model = keras.models.load_model(MODEL_F)


if __name__ == '__main__':
    main()
