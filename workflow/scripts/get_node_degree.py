import json
import csv
import sys

LINKS_F = sys.argv[1]
CSV_F = sys.argv[2]

def main():
    with open(LINKS_F, 'r') as f:
        links_dict = json.load(f)

    # for csv
    degree_classes_csv = []
    for node in links_dict:
        degree = len(links_dict[node]["links"])  # Calculate the degree directly
        degree_classes_csv.append((node, degree)) 

    with open(CSV_F, mode='w', newline='') as f:
        # Write to CSV file
        csv_writer = csv.writer(f)

        # Write the header
        csv_writer.writerow(['node', 'degree'])

        # Write all data rows in one go
        csv_writer.writerows(degree_classes_csv)


if __name__ == '__main__':
    main()
