rule getGraphLinks:
    input: join(config["graphDir"], "{graph_id}.gfa")
    output: join(config["linksDir"], "{graph_id}_links.json")
    temp:
        temp_input_file=join(config["tempDir"], "{graph_id}.gfa"),
        temp_output_file=join(config["tempDir"], "{graph_id}_links_temp.json")
    shell:
        """
        # Copy the original input file to the external temp directory
        cp {input} {temp.temp_input_file}

        # Run the Python script using the temp input file and save output as a temp file
        python3 workflow/scripts/get_graph_links.py {temp.temp_input_file} {temp.temp_output_file}

        # Move the temp output file to the final output location
        mv {temp.temp_output_file} {output.final_output}
        """