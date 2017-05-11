'''
Merged data and label file where:
merged = data[:-1] + label[-1:]
@author yohanes.gultom@gmail.com
'''
import csv
import argparse
from itertools import izip

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', help='Source TSV file')
    parser.add_argument('label_file', help='Target TSV file')
    parser.add_argument('-ld', '--data_delimiter', help='Data file delimiter', default='\t')
    parser.add_argument('-ll', '--label_delimiter', help='Label file delimiter', default='\t')
    parser.add_argument('-lo', '--output_delimiter', help='Output file delimiter', default='\t')
    parser.add_argument('-o', '--output_file', help='Output file', default='merged.tsv')
    args = parser.parse_args()

    with open(args.data_file, 'rb') as data_file, open(args.label_file, 'rb') as label_file, open(args.output_file, 'wb') as output_file:
        data_reader = csv.reader(data_file, delimiter=args.data_delimiter, quoting=csv.QUOTE_NONE)
        label_reader = csv.reader(label_file, delimiter=args.label_delimiter, quoting=csv.QUOTE_NONE)
        writer = csv.writer(output_file, delimiter=args.output_delimiter, quoting=csv.QUOTE_NONE, quotechar='')
        for data, label in izip(data_reader, label_reader):
            merged = data[:-1] + label[-1:]
            writer.writerow(merged)
