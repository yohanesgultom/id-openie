import os
import csv
import argparse
import subprocess
import numpy as np
import json
from sys import platform
from sklearn.externals import joblib
from sklearn.preprocessing import StandardScaler
from tripletools import (
    vectorize,
    parse_connlu_file,
    extract_triples_by_combinations,
    get_best_features
)
from pprint import pprint

# choose script based on OS (windows or *nix)
DEPPARSE_SCRIPT = 'bin' + os.sep + 'id-openie'
if platform == 'win32':
    DEPPARSE_SCRIPT += '.bat'


def write_json(triples, y, out):
    count = 0
    grouped = {}
    for i in range(y.shape[0]):
        if y[i] == 1:
            triple = triples[i]
            if triple[1] not in grouped:
                grouped[triple[1]] = {}
            if triple[2] not in grouped[triple[1]]:
                grouped[triple[1]][triple[2]] = {}
            if triple[3] not in grouped[triple[1]][triple[2]]:
                grouped[triple[1]][triple[2]][triple[3]] = {}
            count += 1
    out.write(json.dumps(grouped) + '\n')
    return count


def write_tsv(triples, y, out):
    writer = csv.writer(out, delimiter='\t', quoting=csv.QUOTE_NONE, quotechar='')
    count = 0
    for i in range(y.shape[0]):
        if y[i] == 1:
            writer.writerow(triples[i])
            count += 1
    return count


def extract(conllu_file, classifier, out, format='tsv', scaler=None):
    X = []
    triples = []
    for index, s, s_header in parse_connlu_file(conllu_file):
        for first, second, third, subj, pred, obj in extract_triples_by_combinations(s, s_header):
            X.append(vectorize(first, second, third))
            triples.append((first['sentence_id'], subj, pred, obj))
    X = np.array(X, dtype='float32')
    # apply best features selection
    X = X[:, get_best_features()]
    # scale if scaler is available
    if scaler:
        X = scaler.transform(X)
    y = classifier.predict(X)
    # write output
    if format == 'tsv':
        return write_tsv(triples, y, out)
    else:  # format == 'json'
        return write_json(triples, y, out)


if __name__ == '__main__':

    if os.path.isfile(DEPPARSE_SCRIPT):
        parser = argparse.ArgumentParser(description='Extract triples from Indonesian text')
        parser.add_argument('input_file', help='Input file containing 1 (one) Indonesian sentence per line')
        parser.add_argument('-m', '--model_file', help='Triples classifier model file', default='triples-classifier-model.pkl')
        parser.add_argument('-s', '--scaler_file', help='Triples classifier scaler file', default='triples-classifier-scaler.pkl')
        parser.add_argument('-o', '--output_file', help='Output file containing triples')
        parser.add_argument('-f', '--output_format', help='Output file format', choices=['json', 'tsv'], default='json')
        args = parser.parse_args()
        args.output_file = args.output_file if args.output_file else 'triples.' + args.output_format

        # dependency parsing
        print('Parsing dependency tree..')
        depparse_output = os.path.basename(args.input_file) + '.conllu'
        subprocess.call([DEPPARSE_SCRIPT, '-f', args.input_file])

        # extract triples
        classifier = joblib.load(args.model_file)
        scaler = joblib.load(args.scaler_file)
        with open(args.output_file, 'wb') as out:
            count = extract(depparse_output, classifier, out, args.output_format, scaler=scaler)

        print('{} triple(s) extracted'.format(count))
        print('Triples saved in ' + args.output_file)
    else:
        print('File not found: ' + DEPPARSE_SCRIPT)
