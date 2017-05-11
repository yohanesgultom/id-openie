import csv
import argparse
import json
from pandas import read_csv, merge

parser = argparse.ArgumentParser()
parser.add_argument('sentences_file', help='Sentences file')
parser.add_argument('labels_file', help='Labels file')
parser.add_argument('-o', '--output', help='Output file', default='out.json')
args = parser.parse_args()

joined = {}
count = [0, 0]
sentences = read_csv(args.sentences_file, delimiter='\t', names=['id', 'text'])
with open(args.labels_file, 'rb') as labels:
    labels = csv.reader(labels, delimiter='\t')
    for row in labels:
        if row[0].strip() == '1':
            sent_id = int(row[1].strip())
            triple = [row[2].strip(), row[3].strip(), row[4].strip()]
            if sent_id not in joined:
                joined[sent_id] = {
                    'id': sent_id,
                    'text': sentences.loc[sent_id]['text'].strip(),
                    'triples': []
                }
            joined[sent_id]['triples'].append(triple)
            count[1] += 1
        else:
            count[0] += 1

with open(args.output, 'w') as outfile:
    json.dump(joined, outfile)

print('Negative, Positive: {}'.format(count))
print('Positive labels: {}'.format(count[1] / float(sum(count))))
print('Output saved to {}'.format(args.output))
