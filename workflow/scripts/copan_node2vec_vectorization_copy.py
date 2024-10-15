from gensim.models import Word2Vec, KeyedVectors
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
WINDOW = int(sys.argv[6])
MIN_COUNT = int(sys.argv[7])
SG = int(sys.argv[8])


def main():
    with open(WALKS_F, 'r') as file:
        walks = [line.strip().split(',') for line in file.readlines()]

    # Train Word2Vec model incrementally
    node_model = Word2Vec(vector_size=DIMENSIONS, window=WINDOW, min_count=MIN_COUNT, sg=SG)
    node_model.build_vocab(walks)
    node_model.train(walks, total_examples=node_model.corpus_count, epochs=node_model.epochs)

    # Save node embeddings and clear memory
    node_model.save(MODEL_F)
    node_model.wv.save(EMBEDDING_F)
    del node_model
    gc.collect()

    # Generate and save edge embeddings
    node_wv = KeyedVectors.load(EMBEDDING_F, mmap='r')
    edges_embs = HadamardEmbedder(keyed_vectors=node_wv)
    edges = extract_edges(walks)

    # Save edge embeddings in chunks to avoid high memory usage
    save_edge_embeddings_in_chunks(edges_embs, edges, EDGE_EMBEDDING_F)

    # edges_kv = edges_embs.as_keyed_vectors()
    # edges_kv.save(EDGE_EMBEDDING_F)


    # with open(EDGE_EMBEDDING_F, 'w') as edge_file:
    #     for edge in edges_embs:
    #         edge_file.write(f"{edge}\n")

def extract_edges(walks):
    edges = set()  # Use a set to avoid duplicates
    for walk in walks:
        for i in range(len(walk) - 1):
            edges.add((walk[i], walk[i + 1]))  # Add consecutive nodes as an edge
    return list(edges)  # Convert the set of edges to a list


def save_edge_embeddings_in_chunks(edges_embs, edge_list, output_file):
    with open(output_file, 'w') as edge_file:
        for edge in edge_list:
            edge_embedding = edges_embs[edge]
            edge_file.write(f"{edge[0]},{edge[1]},{' '.join(map(str, edge_embedding))}\n")


if __name__ == '__main__':
    main()
