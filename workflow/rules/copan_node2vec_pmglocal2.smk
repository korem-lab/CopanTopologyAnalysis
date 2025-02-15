rule getGraphLinks:
    input:
        join(config["graphDir"], "{graph_id}.gfa")
    output:
        temp_input=temp(join(config["tempDir"], "{graph_id}.gfa")),
        temp_output=temp(join(config["tempDir"], "{graph_id}_links_temp.json")), 

        final_output=join(config["linksDir"], "{graph_id}_links.json")
    shell:
        """
        mkdir -p {config[tempDir]}

        cp {input} {output.temp_input}

        python3 workflow/scripts/get_graph_links.py {output.temp_input} {output.temp_output}

        touch {output.temp_input} {output.temp_output}

        cp {output.temp_output} {output.final_output}

        touch {output.final_output}
        """

rule randomSampleWalks:
    input:
        join(config["linksDir"], "{graph_id}_links.json")
    output:
        # Temporary files using consistent wildcards
        temp_input=temp(join(config["tempDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q_links.json")),
        temp_walks_oriented=temp(join(config["tempDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q_walks_oriented.json")),
        temp_walks_vectorized=temp(join(config["tempDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q_walks_vectorized.txt")),
        
        # Final output files with the same wildcards
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
        mkdir -p {config[tempDir]}

        cp {input} {output.temp_input}

        python3 workflow/scripts/generate_walks.py {output.temp_input} \
        {params.walk_length} {params.n_walks} {params.p} {params.q} {params.seed} \
        {output.temp_walks_oriented} {output.temp_walks_vectorized}
        
        touch {output.temp_input} {output.temp_walks_oriented} {output.temp_walks_vectorized}

        cp {output.temp_walks_oriented} {output.walks_oriented}
        cp {output.temp_walks_vectorized} {output.walks_vectorized}

        touch {output.walks_oriented} {output.walks_vectorized}
        """

rule embed:
    input: 
        join(config["walkListsDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q_walks_vectorized.txt")
    output:
        temp_input=temp(join(config["tempDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_walks_vectorized.txt")),

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
        mkdir -p {config[tempDir]}

        cp {input} {output.temp_input}

        python3 workflow/scripts/vectorize_embed_nodes.py \
        {output.temp_input} {output.temp_model} {output.temp_embeddings} {output.temp_edge_embeddings} \
        {params.dimensions} {params.window} {params.min_count} {params.sg}

        touch {output.temp_input} {output.temp_model} {output.temp_embeddings} {output.temp_edge_embeddings}

        cp {output.temp_model} {output.model}
        cp {output.temp_embeddings} {output.embeddings}
        cp {output.temp_edge_embeddings} {output.edge_embeddings}

        touch {output.model} {output.embeddings} {output.edge_embeddings}
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
        mkdir -p {config[tempDir]}

        cp {input.model} {output.temp_model}
        cp {input.embeddings} {output.temp_embeddings}

        python3 workflow/scripts/cluster_dict.py {output.temp_model} {output.temp_embeddings} {output.temp_cluster_dict}

        touch {output.temp_model} {output.temp_embeddings} {output.temp_cluster_dict}

        cp {output.temp_cluster_dict} {output.cluster_dict}

        touch {output.cluster_dict}
        """

rule visualizeTSNE:
    input:
        model=join(config["modelDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_walks.model"),
        embeddings=join(config["embeddingsDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_walks.embeddings"),
        links=join(config["linksDir"], "{graph_id}_links.json")
    output: 
        temp_model=temp(join(config["tempDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_{perplexity}perp{n_iter}iter_walks.model")),
        temp_embeddings=temp(join(config["tempDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_{perplexity}perp{n_iter}iter_walks.embeddings")),
        temp_links=temp(join(config["tempDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_{perplexity}perp{n_iter}iter_links.json")), 
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
        mkdir -p {config[tempDir]}

        cp {input.model} {output.temp_model}
        cp {input.embeddings} {output.temp_embeddings}
        cp {input.links} {output.temp_links}

        python3 workflow/scripts/visualize_embeddings.py \
        {output.temp_model} {output.temp_embeddings} {output.temp_links} {output.temp_plot} \
        {params.graph_id} {params.walk_length} {params.n_walks} {params.p} {params.q} \
        {params.perplexity} {params.n_iter} {params.n_components} {params.rand_state} {params.dimensions}

        touch {output.temp_model} {output.temp_embeddings} {output.temp_links} {output.temp_plot}

        cp {output.temp_plot} {output.plot}

        touch {output.plot}
        """

rule getNodeDegrees:
    input: join(config["linksDir"], "{graph_id}_links.json")
    output: 
        temp_input=temp(join(config["tempDir"], "{graph_id}_links.json")),
        temp_csv=temp(join(config["tempDir"], "{graph_id}_node_degrees.csv")),

        csv=join(config["degreeDir"], "{graph_id}_node_degrees.csv")
    shell:
        """
        mkdir -p {config[tempDir]}

        cp {input} {output.temp_input}

        python3 workflow/scripts/get_node_degree.py {output.temp_input} {output.temp_csv}

        touch {output.temp_input} {output.temp_csv}

        cp {output.temp_csv} {output.csv}

        touch {output.csv}
        """

rule getPairwiseDistances:
    input: join(config["embeddingsDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_walks.embeddings")
    output: 
        temp_input=temp(join(config["tempDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_walks.embeddings")),
        temp_output=temp(join(config["tempDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_pairwiseDistances.csv")),

        final_output=join(config["distancesDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_pairwiseDistances.csv")
    shell:
        """
        mkdir -p {config[tempDir]}

        cp {input} {output.temp_input}

        python3 workflow/scripts/pairwise_distance.py {output.temp_input} {output.temp_output}

        touch {output.temp_input} {output.temp_output}

        cp {output.temp_output} {output.final_output}

        touch {output.final_output}
        """

rule joinDistanceDegree:
    input: 
        distances=join(config["distancesDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_pairwiseDistances.csv"),
        degrees=join(config["degreeDir"], "{graph_id}_node_degrees.csv")
    output: 
        temp_dist=temp(join(config["tempDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_pairwiseDistances.csv")),
        temp_deg=temp(join(config["tempDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_node_degrees.csv")),
        temp_output=temp(join(config["tempDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_distancesWithDegree.csv")),
        final_output=join(config["distDegDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_distancesWithDegree.csv")
    shell:
        """
        mkdir -p {config[tempDir]}

        cp {input.distances} {output.temp_dist}
        cp {input.degrees} {output.temp_deg}

        python3 workflow/scripts/join_distance_degree.py {output.temp_dist} {output.temp_deg} {output.temp_output}

        touch {output.temp_deg} {output.temp_dist} {output.temp_output}

        cp {output.temp_output} {output.final_output}

        touch {output.final_output}
        """

rule getDistDegStats:
    input: 
        join(config["distDegDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_distancesWithDegree.csv")
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
        mkdir -p {config[tempDir]}
        
        cp {input} {output.temp_input}

        python3 get_distance_degree_distribution.py {output.temp_input} {output.temp_output} \
        {params.dimensions} {params.walk_length} {params.n_walks} {params.p} {params.q} {params.graph_id}

        touch {output.temp_input} {output.temp_output}

        cp {output.temp_output} {output.final_output}

        touch {output.final_output}
        """