from os.path import join

configfile: "config/config.yaml"

# Define variables for multiple values
GRAPH_IDS = config["graph_id"]
WALK_LENGTHS = config["walk_lengths"]
N_WALKS = config["n_walks"]
P_VALUES = config["p"]
Q_VALUES = config["q"]
PERPLEXITIES = config["perplexities"]
N_ITERS = config["n_iters"]
DIMENSIONS = config["dimensions"]

rule all:
    input:
       expand(join(config["graphDir"], "{graph_id}.gfa"), graph_id=GRAPH_IDS),
       expand(join(config["linksDir"], "{graph_id}_links2.json"), graph_id=GRAPH_IDS),

       # # walks
       # expand(join(config["walkListsDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q_walks_vectorized.txt"),
       #        graph_id=GRAPH_IDS,
       #        walk_length=WALK_LENGTHS,
       #        n_walks=N_WALKS,
       #        p=P_VALUES,
       #        q=Q_VALUES),
       # expand(join(config["walkDictsDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q_walks_oriented.json"),
       #        graph_id=GRAPH_IDS,
       #        walk_length=WALK_LENGTHS,
       #        n_walks=N_WALKS,
       #        p=P_VALUES,
       #        q=Q_VALUES),

       # # model embeddings
       # expand(join(config["modelDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_walks.model"),
       #        graph_id=GRAPH_IDS,
       #        walk_length=WALK_LENGTHS,
       #        n_walks=N_WALKS,
       #        p=P_VALUES,
       #        q=Q_VALUES, 
       #        k=DIMENSIONS),
       # expand(join(config["embeddingsDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_walks.embeddings"),
       #        graph_id=GRAPH_IDS,
       #        walk_length=WALK_LENGTHS,
       #        n_walks=N_WALKS,
       #        p=P_VALUES,
       #        q=Q_VALUES, 
       #        k=DIMENSIONS),
       # expand(join(config["edgeEmbeddingsDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_walks.edge_embeddings"),
       #        graph_id=GRAPH_IDS,
       #        walk_length=WALK_LENGTHS,
       #        n_walks=N_WALKS,
       #        p=P_VALUES,
       #        q=Q_VALUES, 
       #        k=DIMENSIONS),

       # #  plotting embedding with t-SNE
       #  expand(join(config["plotsDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_{perplexity}perp{n_iter}iter_embeddingPlot.png"),
       #         graph_id=GRAPH_IDS,
       #         walk_length=WALK_LENGTHS,
       #         n_walks=N_WALKS,
       #         p=P_VALUES,
       #         q=Q_VALUES,
       #         perplexity=PERPLEXITIES,
       #         n_iter=N_ITERS, 
       #         k=DIMENSIONS),
       # expand(join(config["clustersDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_clusters.json"),
       #        graph_id=GRAPH_IDS,
       #        walk_length=WALK_LENGTHS,
       #        n_walks=N_WALKS,
       #        p=P_VALUES,
       #        q=Q_VALUES,
       #        k=DIMENSIONS), 

       # # pairwise distances
       # expand(join(config["distancesDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_pairwiseDistances.csv"),
       #        graph_id=GRAPH_IDS,
       #        walk_length=WALK_LENGTHS,
       #        n_walks=N_WALKS,
       #        p=P_VALUES,
       #        q=Q_VALUES,
       #        k=DIMENSIONS), 

       # # degree info for each node
       # expand(join(config["degreeDir"], "{graph_id}_node_degrees.json"),
       #        graph_id=GRAPH_IDS), 
       # expand(join(config["degreeDir"], "{graph_id}_node_degrees.csv"),
       #        graph_id=GRAPH_IDS), 

       # # joining pairwise distances plus degree for each node
       # expand(join(config["distDegDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_distancesWithDegree.csv"),
       #        graph_id=GRAPH_IDS,
       #        walk_length=WALK_LENGTHS,
       #        n_walks=N_WALKS,
       #        p=P_VALUES,
       #        q=Q_VALUES,
       #        k=DIMENSIONS)

include:
    "workflow/rules/copan_node2vec_pmglocal.smk"
