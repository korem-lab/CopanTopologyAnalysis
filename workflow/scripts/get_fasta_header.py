
fasta_f = "workflow/out/copangraphs/sample_1_0_02.fasta"
header_f = "workflow/out/copangraphs/sample_1_0_02_ids.txt"

# # this for format of reference metagenomes fasta
# def main():
#     with open(fasta_f, 'r') as infile:
#         with open(header_f, 'w') as outfile:
#             outfile.write("seqid;genome;info\n")
#             for line in infile:
#                 if line.startswith(">"):
#                     header = line[1:].strip()
#                     header = header.split(" ", 1)

#                     seq_id = str(header[0])
#                     description = header[1].split(",", 1)

#                     if len(description) > 1:
#                         genome = description[0]
#                         info = description[1]

#                         outfile.write(seq_id + ";" + genome + ";" + info + "\n")
                    
#                     else:
#                         outfile.write(seq_id + ";" + description[0] + ";NA" + "\n")

# this for format of sample 1 copan fasta
def main():
    with open(fasta_f, 'r') as infile:
        with open(header_f, 'w') as outfile:
            outfile.write("qseqid\n")
            for line in infile:
                if line.startswith(">"):
                    header = line[1:].strip()
                    
                    outfile.write(header + "\n")


if __name__ == '__main__':
    main()
