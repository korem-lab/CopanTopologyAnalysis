import sys

gfa_f = sys.argv[1]
fasta_f = sys.argv[2]

def main():
    with open(gfa_f, 'r') as gfa, open(fasta_f, 'w') as fasta:
        for line in gfa:
            if line.startswith('S'):  # 'S' lines contain sequences in GFA
                fields = line.strip().split('\t')
                seq_id = str(fields[1]) + "|" + str(fields[3])
                sequence = fields[2] 

                # Write to FASTA format
                fasta.write(f">{seq_id}\n")
                fasta.write(f"{sequence}\n")

if __name__ == '__main__':
    main()
