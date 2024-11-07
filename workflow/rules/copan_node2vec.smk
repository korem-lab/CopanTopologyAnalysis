rule getGraphLinks:
    input:
        join(config["graphDir"], "{graph_id}.gfa")
    output:
        join(config["linksDir"], "{graph_id}_links.json")
    shell:
        """
        python3 workflow/scripts/get_graph_links.py {input} {output}
        """

rule randomSampleWalks:
    input:
        join(config["linksDir"], "{graph_id}_links.json")
    output:
        walks_oriented=join(config["walkDictsDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q_walks_oriented.json"),
        walks_vectorized=join(config["walkListsDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q_walks_vectorized.txt")
    params: 
        walk_length="{walk_length}",
        n_walks="{n_walks}",
        p="{p}",
        q="{q}",
        seed=config["seed"]
    shell:
        """
        python3 workflow/scripts/generate_walks.py {input} \
        {params.walk_length} {params.n_walks} {params.p} {params.q} {params.seed} \
        {output.walks_oriented} {output.walks_vectorized}
        """

rule embed:
    input: 
        join(config["walkListsDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q_walks_vectorized.txt")
    output:
        model=join(config["modelDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_walks.model"),
        embeddings=join(config["embeddingsDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_walks.embeddings"),
        edge_embeddings=join(config["edgeEmbeddingsDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_walks.edge_embeddings")
    params:
        dimensions="{k}",
        window=config["window"], 
        min_count=config["min_count"], 
        sg=config["sg"]
    shell:
        """
        python3 workflow/scripts/vectorize_embed_nodes.py \
        {input} {output.model} {output.embeddings} {output.edge_embeddings} \
        {params.dimensions} {params.window} {params.min_count} {params.sg}
        """

rule getClusters:
    input:
        model=join(config["modelDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_walks.model"),
        embeddings=join(config["embeddingsDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_walks.embeddings")
    output: 
        join(config["clustersDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_clusters.json")
    shell:
        """
        python3 workflow/scripts/cluster_dict.py {input.model} {input.embeddings} {output}
        """

rule visualizeTSNE:
    input:
        model=join(config["modelDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_walks.model"),
        embeddings=join(config["embeddingsDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_walks.embeddings"),
        links=join(config["linksDir"], "{graph_id}_links.json")
    output: 
        join(config["plotsDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_{perplexity}perp{n_iter}iter_embeddingPlot.png")
    params:
        dimensions="{k}",
        walk_length="{walk_length}",
        n_walks="{n_walks}",
        p="{p}",
        q="{q}",
        perplexity="{perplexity}", 
        n_iter="{n_iter}",
        n_components=config["n_components"], 
        rand_state=config["random_state"],
        graph_id=GRAPH_IDS, 
        alpha=config["alpha"]
    shell:
        """
        python3 workflow/scripts/visualize_embeddings.py \
        {input.model} {input.embeddings} {input.links} {output} \
        {params.graph_id} {params.walk_length} {params.n_walks} {params.p} {params.q} \
        {params.perplexity} {params.n_iter} {params.n_components} {params.rand_state} {params.dimensions} {params.alpha}
        """

rule visualizeTSNE_binClustering:
    input:
        embeddings=join(config["embeddingsDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_walks.embeddings"),
        tax_csv=join(config["taxonomyDir"])
    output: 
        join(config["plotsDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_{perplexity}perp{n_iter}iter_embeddingPlot_species.png")
    params:
        dimensions="{k}",
        walk_length="{walk_length}",
        n_walks="{n_walks}",
        p="{p}",
        q="{q}",
        perplexity="{perplexity}", 
        n_iter="{n_iter}",
        n_components=config["n_components"], 
        rand_state=config["random_state"],
        graph_id=GRAPH_IDS, 
        alpha=config["alpha"]
    shell:
        """
        python3 workflow/scripts/visualize_embeddings_binClustering.py \
        {input.embeddings} {input.tax_csv} {output} \
        {params.graph_id} {params.walk_length} {params.n_walks} {params.p} {params.q} \
        {params.perplexity} {params.n_iter} {params.n_components} {params.rand_state} {params.dimensions} {params.alpha}
        """

rule getNodeDegrees:
    input: join(config["linksDir"], "{graph_id}_links.json")
    output: 
        csv=join(config["degreeDir"], "{graph_id}_node_degrees.csv")
    shell:
        """
        python3 workflow/scripts/get_node_degree.py {input} {output.csv}
        """

rule getPairwiseDistances:
    input: join(config["embeddingsDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_walks.embeddings")
    output: join(config["distancesDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_pairwiseDistances.csv")
    shell:
        """
        python3 workflow/scripts/pairwise_distance.py {input} {output}
        """

rule joinDistanceDegree:
    input: 
        distances=join(config["distancesDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_pairwiseDistances.csv"),
        degrees=join(config["degreeDir"], "{graph_id}_node_degrees.csv")
    output: join(config["distDegDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_distancesWithDegree.csv")
    shell:
        """
        python3 workflow/scripts/join_distance_degree.py {input.distances} {input.degrees} {output}
        """    

rule getDistDegStats:
    input: join(config["distDegDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_distancesWithDegree.csv")
    output: join(config["distDegDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_stats.csv")
    params:
        dimensions="{k}",
        walk_length="{walk_length}",
        n_walks="{n_walks}",
        p="{p}",
        q="{q}",
        graph_id=GRAPH_IDS
    shell:
        """
        python3 get_distance_degree_distribution.py {input} {output} \
        {params.dimensions} {params.walk_length} {params.n_walks} {params.p} {params.q} {params.graph_id}
        """

