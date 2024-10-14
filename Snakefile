from os.path import join

configfile: "config/config.yaml"

GRAPH_ID = ["dummy_graph"]

rule all:
    input:
        # Entry point for copan node2vec pipeline: GFA file of copangraph
        expand(join(config["graphDir"],"{graph_id}.gfa"), graph_id=GRAPH_ID),
        # Dict of all bidirectional links from input graph
        expand(join(config["linksDir"],"{graph_id}_links.json"), graph_id=GRAPH_ID),
        # Dicts with oriented walks and lists with vectorized walks
        expand(
                    join(config["walkListsDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q_walks_vectorized.txt"),
                    graph_id=GRAPH_ID,
                    walk_length=config["walk_length"],
                    n_walks=config["n_walks"],
                    p=config["p"],
                    q=config["q"]
                ),
        expand(
                    join(config["walkDictsDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q_walks_oriented.json"),
                    graph_id=GRAPH_ID,
                    walk_length=config["walk_length"],
                    n_walks=config["n_walks"],
                    p=config["p"],
                    q=config["q"]
                ),
        expand(
                    join(config["modelDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q_walks.model"),
                    graph_id=GRAPH_ID,
                    walk_length=config["walk_length"],
                    n_walks=config["n_walks"],
                    p=config["p"],
                    q=config["q"]
                ),
        expand(
                    join(config["embeddingsDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q_walks.embeddings"),
                    graph_id=GRAPH_ID,
                    walk_length=config["walk_length"],
                    n_walks=config["n_walks"],
                    p=config["p"],
                    q=config["q"]
                ),
        expand(
                    join(config["edgeEmbeddingsDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q_walks.edge_embeddings"),
                    graph_id=GRAPH_ID,
                    walk_length=config["walk_length"],
                    n_walks=config["n_walks"],
                    p=config["p"],
                    q=config["q"]
                )
        
include:
    "workflow/rules/copan_node2vec.smk"




