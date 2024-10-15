from gensim.models import Word2Vec
from gensim.models import KeyedVectors
from node2vec.edges import HadamardEmbedder
import sys
import gc

# in/out files
WALKS_F = sys.argv[1]
MODEL_F = sys.argv[2]
EMBEDDING_F = sys.argv[3]
EDGE_EMBEDDING_F = sys.argv[4]

# embedding params
DIMENSIONS = int(sys.argv[5])
# idk what these really do yet .... just using default params for now
WINDOW = int(sys.argv[6])
MIN_COUNT = int(sys.argv[7])
SG = int(sys.argv[8])

def main():

    with open(WALKS_F, 'r') as file:
        walks = [line.strip().split(',') for line in file.readlines()]

    # vectorization all at once -- not memory friendly
    node_model = Word2Vec(sentences=walks, vector_size=DIMENSIONS, window=WINDOW, min_count=MIN_COUNT, sg=SG)

    # # memory friendly!
    # node_model = Word2Vec(vector_size=DIMENSIONS, window=WINDOW, min_count=MIN_COUNT, sg=SG)

    # # Build vocabulary first (saves memory)
    # node_model.build_vocab(walks)

    # # Train model incrementally
    # node_model.train(walks, total_examples=node_model.corpus_count, epochs=node_model.epochs)

    node_model.save(MODEL_F)
    node_model.wv.save(EMBEDDING_F)

    # Free memory before creating edge embeddings
    # del node_model
    # gc.collect()

    # edges_embs = HadamardEmbedder(keyed_vectors=node_model.wv)

    # # Get all edges in a separate KeyedVectors instance - use with caution could be huge for big networks
    # # edges_kv = edges_embs.as_keyed_vectors()

    # # Save embeddings for later use
    # # edges_kv.save(EDGE_EMBEDDING_F)

    # # Iterate over edges and save them incrementally
    # with open(EDGE_EMBEDDING_F, 'w') as edge_file:
    #     for edge in edges_embs:
    #         edge_file.write(f"{edge}\n")

    # embeddings = KeyedVectors.load(EMBEDDING_F, mmap='r')
    # avector = embeddings['A']  # Get numpy vector of a word
    # model = Word2Vec.load(MODEL_F)
    # most_sim = model.wv.most_similar("A")


if __name__ == '__main__':
    main()
