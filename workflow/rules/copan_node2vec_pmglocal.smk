rule getGraphLinks:
    input:
        graph_file=join(config["graphDir"], "{graph_id}.gfa")
    output:
        final_output=join(config["linksDir"], "{graph_id}_links2.json"),
        temp_input_file=temp(join(config["tempDir"], "{graph_id}.gfa")),
        temp_output_file=temp(join(config["tempDir"], "{graph_id}_links_temp.json"))
    shell:
        """
        # Copy the original input file to the external temp directory
        cp {input.graph_file} {output.temp_input_file}

        # Run the Python script using the temp input file and save output as a temp file
        python3 workflow/scripts/get_graph_links.py {output.temp_input_file} {output.temp_output_file}

        # Print directory contents before moving the output
        echo "Contents of temp directory before mv:"
        ls -l {config["tempDir"]}

        # Check if the temp output file was created
        if [ -f {output.temp_output_file} ]; then
            echo "Temp output file exists: {output.temp_output_file}"
        else
            echo "Temp output file NOT found: {output.temp_output_file}"
            exit 1
        fi

        # Move the temp output file to the final output location
        mv {output.temp_output_file} {output.final_output}
        """