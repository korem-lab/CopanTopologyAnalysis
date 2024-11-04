rule getGraphLinks:
    input:
        join(config["graphDir"], "{graph_id}.gfa")
    output:
        # final_output=join(config["linksDir"], "{graph_id}_links2.json"),
        # These outputs are temporary files created during the process
        temp_input_file=join(config["tempDir"], "{graph_id}.gfa"),
        temp_output_file=join(config["tempDir"], "{graph_id}_links_temp.json")
    shell:
        "cp {input} {output.temp_input_file}"
        "python3 workflow/scripts/get_graph_links.py {output.temp_input_file} {output.temp_output_file}"
        # mv {output.temp_output_file} {output.final_output}
        # """
