rule getGraphLinks:
    input:
        join(config["graphDir"], "{graph_id}.gfa")
    output:
        temp_input=temp(join(config["tempDir"], "{graph_id}.gfa")),
        temp_output=temp(join(config["tempDir"], "{graph_id}_links_temp.json")), 

        final_output=join(config["linksDir"], "{graph_id}_links.json")
    shell:
        """
        cp {input} {output.temp_input}

        python3 workflow/scripts/get_graph_links.py {output.temp_input} {output.temp_output}

        cp {output.temp_output} {output.final_output}
        """

rule randomSampleWalks:
    input:
        join(config["linksDir"], "{graph_id}_links.json")
    output:
        temp_input=temp(join(config["tempDir"], "{graph_id}_links.json")),
        temp_walks_oriented=temp(join(config["tempDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q_walks_oriented.json")),
        temp_walks_vectorized=temp(join(config["tempDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q_walks_vectorized.txt")),

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
        cp {input} {temp_input}

        python3 workflow/scripts/generate_walks.py {output.temp_input} \
        {params.walk_length} {params.n_walks} {params.p} {params.q} {params.seed} \
        {output.temp_walks_oriented} {output.temp_walks_vectorized}
        
        cp {output.temp_walks_oriented} {output.walks_oriented}
        cp {output.temp_walks_vectorized} {output.walks_vectorized}
        """

rule embed:
    input: 
        join(config["walkListsDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q_walks_vectorized.txt")
    output:
        temp_input=temp(join(config["tempDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q_walks_vectorized.txt")),
        temp_model=temp(join(config["tempDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_walks.model")),
        temp_embeddings=temp(join(config["tempDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_walks.embeddings")),
        temp_edge_embeddings=temp(join(config["tempDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_walks.edge_embeddings")),

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
        cp {input} {output.temp_input}

        python3 workflow/scripts/vectorize_embed_nodes.py \
        {output.temp_input} {output.temp_model} {output.temp_embeddings} {output.temp_edge_embeddings} \
        {params.dimensions} {params.window} {params.min_count} {params.sg}

        cp {output.temp_model} {output.model}
        cp {output.temp_embeddings} {output.embeddings}
        cp {output.temp_edge_embeddings} {output.edge_embeddings}
        """

rule getClusters:
    input:
        model=join(config["modelDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_walks.model"),
        embeddings=join(config["embeddingsDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_walks.embeddings")
    output: 
        temp_model=temp(join(config["tempDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_walks.model")), 
        temp_embeddings=temp(join(config["tempDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_walks.embeddings")),
        temp_cluster_dict=temp(join(config["tempDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_clusters.json")),

        cluster_dict=join(config["clustersDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_clusters.json")
    shell:
        """
        cp {input.model} {output.temp_model}
        cp {input.embeddings} {output.temp_embeddings}

        python3 workflow/scripts/cluster_dict.py {output.temp_model} {output.temp_embeddings} {output.temp_cluster_dict}

        cp {output.temp_cluster_dict} {output.cluster_dict}
        """

rule visualizeTSNE:
    input:
        model=join(config["modelDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_walks.model"),
        embeddings=join(config["embeddingsDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_walks.embeddings"),
        links=join(config["linksDir"], "{graph_id}_links.json")
    output: 
        temp_model=temp(join(config["tempDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_walks.model")),
        temp_embeddings=temp(join(config["tempDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_walks.embeddings")),
        temp_links=temp(join(config["tempDir"], "{graph_id}_links.json")), 
        temp_plot=temp(join(config["tempDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_{perplexity}perp{n_iter}iter_embeddingPlot.png")),

        plot=join(config["plotsDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_{perplexity}perp{n_iter}iter_embeddingPlot.png")
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
        graph_id=GRAPH_IDS
    shell:
        """
        cp {input.model} {output.temp_model}
        cp {input.embeddings} {output.temp_embeddings}
        cp {input.links} {output.temp_links}

        python3 workflow/scripts/visualize_embeddings.py \
        {output.temp_model} {output.temp_embeddings} {output.temp_links} {output.temp_plot} \
        {params.graph_id} {params.walk_length} {params.n_walks} {params.p} {params.q} \
        {params.perplexity} {params.n_iter} {params.n_components} {params.rand_state} {params.dimensions}

        cp {output.temp_plot} {output.plot}
        """

rule getNodeDegrees:
    input: join(config["linksDir"], "{graph_id}_links.json")
    output: 
        temp_input=temp(join(config["tempDir"], "{graph_id}_links.json")),
        temp_json=temp(join(config["tempDir"], "{graph_id}_node_degrees.json")),
        temp_csv=temp(join(config["tempDir"], "{graph_id}_node_degrees.csv")),

        json=join(config["degreeDir"], "{graph_id}_node_degrees.json"),
        csv=join(config["degreeDir"], "{graph_id}_node_degrees.csv")
    shell:
        """
        cp {input} {output.temp_input}

        python3 get_node_degree.py {output.temp_input} {output.temp_json} {output.temp_csv}

        cp {output.temp_json} {output.json}
        cp {output.temp_csv} {output.csv}
        """

rule getPairwiseDistances:
    input: join(config["embeddingsDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_walks.embeddings")
    output: 
        temp_input=temp(join(config["tempDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_walks.embeddings")),
        temp_output=temp(join(config["tempDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_pairwiseDistances.csv")),

        final_output=join(config["distancesDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_pairwiseDistances.csv")
    shell:
        """
        cp {input} {output.temp_input}

        python3 workflow/scripts/pairwise_distance.py {output.temp_input} {output.temp_output}

        cp {output.temp_output} {output.final_output}
        """

rule joinDistanceDegree:
    input: 
        distances=join(config["distancesDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_pairwiseDistances.csv"),
        degrees=join(config["degreeDir"], "{graph_id}_node_degrees.csv")
    output: 
        temp_dist=temp(join(config["tempDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_pairwiseDistances.csv")),
        temp_deg=temp(join(config["tempDir"], "{graph_id}_node_degrees.csv")),
        temp_output=temp(join(config["tempDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_distancesWithDegree.csv")),
        final_output=join(config["distDegDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_distancesWithDegree.csv")
    shell:
        """
        cp {input.distances} {output.temp_dist}
        cp {input.degrees} {output.temp_deg}

        python3 workflow/scripts/join_distance_degree.py {output.temp_dist} {output.temp_deg} {output.temp_output}

        cp {output.temp_output} {output.final_output}
        """

rule getDistDegStats:
    input: join(config["distDegDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_distancesWithDegree.csv")
    output: 
        temp_input=temp(join(config["tempDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_distancesWithDegree.csv")), 
        temp_output=temp(join(config["tempDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_stats.csv")),

        final_output=join(config["distDegDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_stats.csv")
    params:
        dimensions="{k}",
        walk_length="{walk_length}",
        n_walks="{n_walks}",
        p="{p}",
        q="{q}",
        graph_id=GRAPH_IDS
    shell:
        """
        cp {input} {output.temp_input}

        python3 get_distance_degree_distribution.py {output.temp_input} {output.temp_output} \
        {params.dimensions} {params.walk_length} {params.n_walks} {params.p} {params.q} {params.graph_id}

        cp {output.temp_output} {output.final_output}
        """