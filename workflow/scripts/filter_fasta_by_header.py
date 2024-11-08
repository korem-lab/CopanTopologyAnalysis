from Bio import SeqIO

ids_file = "workflow/out/blast/qseqs_no_blast_hits.txt"
fasta_file = "workflow/out/copangraphs/sample_1_0_02.fasta"
output_file = "workflow/out/copangraphs/sample_1_0_02_noBlastHitQueries.fasta"

def extract_sequences(fasta_file, ids_file, output_file):
    # Read the sequence IDs from the txt file
    with open(ids_file, 'r') as id_file:
        seq_ids = set(line.strip() for line in id_file)

    # Open the output file to write the selected sequences
    with open(output_file, 'w') as output_fasta:
        # Parse the original FASTA file and write the sequences with matching IDs
        count = 0
        for record in SeqIO.parse(fasta_file, "fasta"):
            if record.id in seq_ids:
                SeqIO.write(record, output_fasta, "fasta")
                count += 1

        print(f"Extracted {count} sequences to {output_file}.")

# Call the function
extract_sequences(fasta_file, ids_file, output_file)
