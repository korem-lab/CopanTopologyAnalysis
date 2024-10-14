rule getGraphLinks:
    input:
        join(config["graphDir"],"{graph_id}.gfa")
    output:
        join(config["linksDir"],"{graph_id}_links.json")
    shell:
        """
        python3 scripts/copan_get_graph_links.py {input} {output}
        """

rule randomSampleWalks:
    input:
        join(config["linksDir"],"{graph_id}_links.json")
    output:
        walks_oriented=join(config["walkDictsDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q_walks_oriented.json"),
        walks_vectorized=join(config["walkListsDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q_walks_vectorized.txt")
    params: 
        walk_length=config["walk_length"],
        n_walks=config["n_walks"],
        p=config["p"],
        q=config["q"],
        seed=config["seed"]
    shell:
        """
        python3 workflow/scripts/copan_node2vec_walks_vectorized_copy.py {input} \
        {params.walk_length} {params.n_walks} {params.p} {params.q} {params.seed} \
        {output.walks_oriented} {output.walks_vectorized}
        """

rule vectorizeWalks:
    input: 
        join(config["walkListsDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q_walks_vectorized.txt")
    output:
        model=join(config["modelDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q_walks.model"),
        embeddings=join(config["embeddingsDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q_walks.embeddings"),
        edge_embeddings=join(config["edgeEmbeddingsDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q_walks.edge_embeddings")
    params:
        dimensions=config["dimensions"], 
        window=config["window"], 
        min_count=config["min_count"], 
        sg=config["sg"]
    shell:
        """
        python3 workflow/scripts/copan_node2vec_vectorization_copy.py \
        {input} {output.model} {output.embeddings} {output.edge_embeddings} \
        {params.dimensions} {params.window} {params.min_count} {params.sg}
        """



        



