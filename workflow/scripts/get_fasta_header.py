import sys

# fasta_f = "dummy.fasta"
# header_f = sys.argv[2]
fasta_f = "workflow/out/reference_metagenomes/sample_1_reference_metagenome.fasta"
header_f = "workflow/out/reference_metagenomes/sample_1_reference_metagenome_ids.txt"

def main():
    with open(fasta_f, 'r') as infile:
        with open(header_f, 'w') as outfile:
            outfile.write("seqid;genome;info\n")
            for line in infile:
                if line.startswith(">"):
                    header = line[1:].strip()
                    header = header.split(" ", 1)

                    seq_id = str(header[0])
                    description = header[1].split(",", 1)

                    if len(description) > 1:
                        genome = description[0]
                        info = description[1]

                        outfile.write(seq_id + ";" + genome + ";" + info + "\n")
                    
                    else:
                        outfile.write(seq_id + ";" + description[0] + ";NA" + "\n")


if __name__ == '__main__':
    main()