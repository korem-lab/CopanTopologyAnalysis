rule walkAndEmbed:
    input:
        join(config["linksDir"], "{graph_id}_links.json")
    output:
        join(config["embeddingsDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_walks.embeddings")
    params: 
        walk_length="{walk_length}",
        n_walks="{n_walks}",
        p="{p}",
        q="{q}",
        seed=config["seed"], 
        dimensions="{k}",
        window=config["window"], 
        min_count=config["min_count"], 
        sg=config["sg"]
    shell:
        """
        python3 workflow/scripts/walk_and_embed.py {input} {output} \
        {params.walk_length} {params.n_walks} {params.p} {params.q} {params.seed} \
        {params.dimensions} {params.window} {params.min_count} {params.sg}
        """

rule getPairwiseDistances:
    input: join(config["embeddingsDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_walks.embeddings")
    output: join(config["distancesDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q{k}k_pairwiseDistances.csv")
    shell:
        """
        python3 workflow/scripts/pairwise_distance.py {input} {output}
        """