"""
Triples clustering using k-modes
Author: yohanes.gultom@gmail.com
"""

import numpy as np
import itertools
import csv
import argparse
from pprint import pprint
from kmodes import kmodes
from tripletools import (
    conllu,
    vectorize,
    parse_connlu_file,
    extract_triples_by_combinations,
    extract_triples_by_children_combination
)

# config
n_clusters = 3
init_cluster = 'Cao'
output_file = 'clustered.tsv'


if __name__ == '__main__':
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('conllu_file', help='Universal Dependencies treebank in CONLL-U format')
    parser.add_argument('-c', '--cluster_size', type=int, help='Desired cluster size', default=n_clusters)
    parser.add_argument('-i', '--cluster_init', choices=['Cao', 'Huang'], help='Cluster initialization method', default=init_cluster)
    parser.add_argument('-o', '--output_file', help='Output file', default=output_file)
    args = parser.parse_args()

    # extract features
    x = []
    triples = []
    print('Extracting features')
    for index, s, s_header in parse_connlu_file(args.conllu_file):
        for obj in extract_triples_by_combinations(s, s_header):
            triples.append(obj)
            x.append(vectorize(obj[0], obj[1], obj[2]))

    # convert data to numpy matrix
    x = np.array(x)
    print(x.shape)
    pprint(x)

    # k-modes clustering
    print('# of clusters: {}'.format(args.cluster_size))
    print('Initialization: {}'.format(args.cluster_init))
    kmodes = kmodes.KModes(n_clusters=args.cluster_size, init=args.cluster_init, verbose=1)
    predictions = kmodes.fit_predict(x)
    print(predictions)

    print('clustered')
    concat = np.concatenate((predictions.reshape(1, len(predictions)).T, x), axis=1)
    x_predicted = sorted(concat.tolist())
    pprint(x_predicted)
    print('centroids')
    pprint(kmodes.cluster_centroids_)


    # # map triples
    # clusters = {}
    # for i in range(len(predictions)):
    #     cluster_index = predictions[i]
    #     triple = triples[i]
    #     # so funny
    #     triple[0]['vector'] = x[i]
    #     if cluster_index not in clusters:
    #         clusters[cluster_index] = []
    #     clusters[cluster_index].append(triple)
    #
    # # print by cluster
    # with open(args.output_file, 'wb') as out:
    #     for key in sorted(clusters.iterkeys()):
    #         print('Cluster {}\t{}'.format(key, len(clusters[key])))
    #         for t in clusters[key]:
    #             out.write('{}\t{}\t{}\t{}\t{}\t{}_{}_{}\t{}_{}_{}\t{}_{}_{}\t{}\t{}\n'.format(
    #                 # triple cluster id
    #                 key,
    #                 # sentence id
    #                 t[0]['sentence_id'],
    #                 # triple text
    #                 t[0]['flatten'], t[1]['form'], t[2]['flatten'],
    #                 # triple deprel-postag
    #                 t[0]['upostag'], t[0]['deprel'], t[0]['head_upostag'],
    #                 t[1]['upostag'], t[1]['deprel'], t[1]['head_upostag'],
    #                 t[2]['upostag'], t[2]['deprel'], t[2]['head_upostag'],
    #                 # vector
    #                 t[0]['vector'],
    #                 (vectorize(t[0]) + vectorize(t[1]) + vectorize(t[2]))
    #             ))
    #
    # print('Completed.')
