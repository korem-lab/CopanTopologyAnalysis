from Bio import SeqIO
import csv

fasta_file = "workflow/out/copangraphs/sample_1_0_02.fasta"
output_csv = "workflow/out/blast/sample_1_0_02_seqLengths.csv"

# Open the output CSV file for writing
with open(output_csv, "w", newline="") as csvfile:
    csvwriter = csv.writer(csvfile)
    # Write header
    csvwriter.writerow(["qseqid", "length"])

    # Read each sequence from the FASTA file and write its length
    for record in SeqIO.parse(fasta_file, "fasta"):
        csvwriter.writerow([record.id, len(record.seq)])
