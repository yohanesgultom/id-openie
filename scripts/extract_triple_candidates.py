"""
Extract triple candidates heuristically
Author: yohanes.gultom@gmail.com
"""

import itertools
import csv
import sys
import argparse
import json
from tripletools import (
    conllu,
    vectorize,
    parse_connlu_file,
    extract_triples_by_combinations,
    flatten_conllu_sentence
)


def extract_candidates(conllu_file, output_file, format, verbose=False):
    print('Extracting triples')
    count = {'sentences': 0, 'candidates': 0}
    out = sys.stdout
    if not verbose:
        out = open(output_file, 'wb')
    mapped = {}
    mark_head = format in ['annotate', 'publish']
    for index, s, s_header in parse_connlu_file(conllu_file, mark_head=mark_head):
        sentence_text = flatten_conllu_sentence(s)
        for first, second, third, subj, pred, obj in extract_triples_by_combinations(s, s_header):
            if format == 'train':
                # vector only format for machine learning model input
                out.write(','.join((str(v) for v in vectorize(first, second, third))) + ',0\n')
            elif format == 'annotate':
                # human readable format for easier annotation
                out.write('{}\t{}\t{}\t{}\t{}\t{}\n'.format(
                    first['sentence_id'],
                    sentence_text,
                    subj,
                    pred,
                    obj,
                    0
                ))
            elif format == 'publish':
                # merge both human readable and vector format to simplify publishing
                out.write('{}\t{}\t{}\t{}\t{}\t'.format(
                    first['sentence_id'],
                    sentence_text,
                    subj,
                    pred,
                    obj
                ))
                out.write('\t'.join((str(v) for v in vectorize(first, second, third))) + ',0\n')
            count['candidates'] += 1
        count['sentences'] += 1
    print('{} sentence(s) processed and {} triples candidates extracted.'.format(count['sentences'], count['candidates']))
    out.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('conllu_file', help='Universal Dependencies treebank in CONLL-U format file')
    parser.add_argument('-o', '--output_file', help='Output file', default='triple_candidates.tsv')
    parser.add_argument('-v', '--verbose', help='Output verbosity', action='store_true')
    parser.add_argument('-f', '--format', help='Output format', choices=['annotate', 'train', 'publish'], default='annotate')
    args = parser.parse_args()
    extract_candidates(args.conllu_file, args.output_file, args.format, args.verbose)
