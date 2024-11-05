rule getGraphLinks:
    input:
        join(config["storageDir"], config["graphDir"], "{graph_id}.gfa")
    output:
        temp_out=temp(join(config["tempDir"], config["linksDir"], "{graph_id}_links.json"))
        
    shell:
        """
        mkdir -p {config[tempDir]}/{config[graphDir]}

        cp {input} {config[tempDir]}/{config[graphDir]}/

        mkdir -p {config[tempDir]}/{config[linksDir]}

        python3 workflow/scripts/get_graph_links.py {config[tempDir]}/{config[graphDir]}/{wildcards.graph_id}.gfa {output}

        cp {output} {config[storageDir]}/{config[linksDir]}/
        """

# rule randomSampleWalks:
#     input:
#         join(config["storageDir"], config["linksDir"], "{graph_id}_links.json")
#     output:
#         walks_oriented=join(config["tempDir"], config["walkDictsDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q_walks_oriented.json"),
#         walks_vectorized=join(config["tempDir"], config["walkListsDir"], "{graph_id}_{walk_length}Lw{n_walks}Nw{p}p{q}q_walks_vectorized.txt")
#     params: 
#         walk_length="{walk_length}",
#         n_walks="{n_walks}",
#         p="{p}",
#         q="{q}",
#         seed=config["seed"]
#     shell:
#         """
#         mkdir -p {config[tempDir]}/{config[graphDir]}

#         cp {input} {config[tempDir]}/{config[graphDir]}/

#         mkdir -p {config[tempDir]}/{config[linksDir]}

#         python3 workflow/scripts/generate_walks.py {input} \
#         {params.walk_length} {params.n_walks} {params.p} {params.q} {params.seed} \
#         {output.walks_oriented} {output.walks_vectorized}
#         """

