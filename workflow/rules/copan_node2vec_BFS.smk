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
        join(config["walkListsDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q_walks_vectorized_BFS.txt")
    params: 
        walk_length="{walk_length}",
        n_walks="{n_walks}",
        p="{p}",
        q="{q}",
        seed=config["seed"]
    shell:
        """
        python3 workflow/scripts/generate_walks_BFS_pared.py {input} \
        {params.walk_length} {params.n_walks} {params.p} {params.q} {params.seed} \
        {output}
        """

rule embed:
    input: 
        join(config["walkListsDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q_walks_vectorized_BFS.txt")
    output:
        join(config["embeddingsDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_walks_BFS.embeddings")
    params:
        dimensions="{k}",
        window=config["window"], 
        min_count=config["min_count"], 
        sg=config["sg"]
    shell:
        """
        python3 workflow/scripts/vectorize_embed_nodes_pared.py \
        {input} {output} \
        {params.dimensions} {params.window} {params.min_count} {params.sg}
        """

rule visualizeTSNE_binClustering:
    input:
        embeddings=join(config["embeddingsDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_walks_BFS.embeddings"),
        tax_csv=join(config["taxonomyDir"], "{graph_id}_nodes_by_{tax_level}.csv")
    output: 
        join(config["plotsDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_{perplexity}perp{n_iter}iter_embeddingPlot_{tax_level}_BFS.png")
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
        alpha=config["alpha"], 
        tax_level="{tax_level}"
    shell:
        """
        python3 workflow/scripts/visualize_embeddings_binClustering.py \
        {input.embeddings} {input.tax_csv} {output} \
        {params.graph_id} {params.walk_length} {params.n_walks} {params.p} {params.q} \
        {params.perplexity} {params.n_iter} {params.n_components} {params.rand_state} {params.dimensions} {params.alpha} {params.tax_level}
        """

rule PCA:
    input:
        embeddings=join(config["embeddingsDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_walks_BFS.embeddings"),
        tax_csv=join(config["taxonomyDir"], "{graph_id}_nodes_by_{tax_level}.csv")
    output: 
        join(config["plotsDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_PCA_{tax_level}_BFS.png")
    params:
        dimensions="{k}",
        walk_length="{walk_length}",
        n_walks="{n_walks}",
        p="{p}",
        q="{q}",
        n_components=config["n_components"], 
        graph_id=GRAPH_IDS, 
        alpha=config["alpha"], 
        tax_level="{tax_level}"
    shell:
        """
        python3 workflow/scripts/pca_viz.py \
        {input.embeddings} {input.tax_csv} {output} \
        {params.graph_id} {params.walk_length} {params.n_walks} {params.p} {params.q} \
        {params.n_components} {params.dimensions} {params.alpha} {params.tax_level}
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
    input: join(config["embeddingsDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_walks_BFS.embeddings")
    output: join(config["distancesDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_pairwiseDistances_BFS.csv")
    shell:
        """
        python3 workflow/scripts/pairwise_distance.py {input} {output}
        """

rule joinDistanceDegree:
    input: 
        distances=join(config["distancesDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_pairwiseDistances_BFS.csv"),
        degrees=join(config["degreeDir"], "{graph_id}_node_degrees.csv")
    output: 
        join(config["distDegDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_distancesWithDegree_BFS.csv")
    shell:
        """
        python3 workflow/scripts/join_distance_degree.py {input.distances} {input.degrees} {output}
        """  

rule joinDistanceTax:
    input: 
        distances=join(config["distancesDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_pairwiseDistances_BFS.csv"),
        tax_csv=join(config["taxonomyDir"], "{graph_id}_nodes_by_{tax_level}.csv")
    output: 
        join(config["taxonomyDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_{tax_level}_distancesWithTax_BFS.csv")
    params:
        tax_level="{tax_level}"
    shell:
        """
        python3 workflow/scripts/join_distance_species.py {input.distances} {input.tax_csv} {output} {params.tax_level}
        """      

rule getDistDegStats:
    input: join(config["distDegDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_distancesWithDegree_BFS.csv")
    output: join(config["distDegDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_stats_BFS.csv")
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

rule getAverageDist:
    input: 
        join(config["taxonomyDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_{tax_level}_distancesWithTax_BFS.csv")
    output:
        join(config["taxonomyDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_{tax_level}_averageDistance_BFS.csv")
    shell:
        """
        python3 workflow/scripts/average_pairwise_distances.py {input} {output}
        """

rule silhouetteScore:
    input: 
        distances=join(config["distancesDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_pairwiseDistances_BFS.csv"),
        species_df=join(config["taxonomyDir"], "{graph_id}_nodes_by_{tax_level}_multilabel.csv")
    output:
        join(config["distancesDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_silhouetteScore_BFS.txt")
    shell:
        """
        python3 workflow/scripts/multilabel_silhouette_score.py {input.distances} {input.species_df} {output}
        """
