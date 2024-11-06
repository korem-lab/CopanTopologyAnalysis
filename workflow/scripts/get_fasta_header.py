import sys

# fasta_f = sys.argv[1]
# header_f = sys.argv[2]
fasta_f = "workflow/out/reference_metagenomes/sample_1_reference_metagenome.fasta"
header_f = "workflow/out/reference_metagenomes/sample_1_reference_metagenome_ids.txt"

def main():
    with open(fasta_f, 'r') as infile:
        with open(header_f, 'w') as outfile:
            for line in infile:
                if line.startswith(">"):
                    header = line[1:].strip()
                    header = header.split(" ", 1)

                    seq_id = str(header[0])
                    description = str(header[1])

                    outfile.write(seq_id + ";" + description + "\n")


if __name__ == '__main__':
    main()
