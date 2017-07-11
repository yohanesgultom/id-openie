"""
Triple tools
Author: yohanes.gultom@gmail.com
"""

import itertools
import csv
import argparse

BEST_FEATURES = [0, 1, 2, 3, 5, 6, 10, 11, 12, 14, 17, 18, 19, 20, 21, 22, 23]  # F1 0.586
# BEST_FEATURES = [0, 1, 2, 3, 5, 6, 10, 11, 12, 17, 18, 19, 20, 21, 22, 23]   # F1 0.579
# BEST_FEATURES = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]  # F1 0.547


# constants
conllu = ['ID', 'FORM', 'LEMMA', 'UPOSTAG', 'XPOSTAG', 'FEATS', 'HEAD', 'DEPREL', 'DEPS', 'MISC']
postag = ['', 'ADJ', 'ADP', 'ADV', 'AUX', 'CCONJ', 'DET', 'INTJ', 'NOUN', 'NUM', 'PART', 'PRON', 'PROPN', 'PUNCT', 'SCONJ', 'SYM', 'VERB', 'X', 'CONJ']
deprel = ['', 'acl', 'advcl', 'advmod', 'amod', 'appos', 'aux', 'case', 'cc', 'ccomp', 'clf', 'compound', 'conj', 'cop', 'csubj', 'dep', 'det', 'discourse', 'dislocated', 'expl', 'fixed', 'flat', 'goeswith', 'iobj', 'list', 'mark', 'nmod', 'nsubj', 'nummod', 'obj', 'obl', 'orphan', 'parataxis', 'punct', 'reparandum', 'root', 'vocative', 'xcomp', 'nsubjpass', 'name', 'dobj', 'neg', 'mwe', 'csubjpass']
entity = ['', 'PERSON', 'LOCATION', 'ORGANIZATION', 'TIME', 'QUANTITY', 'OTHER', 'DATE']

# extraction RULES
subject_object_candidates_pos = ['PROPN', 'NOUN', 'PRON', 'VERB']
predicate_candidates_pos = ['VERB', 'AUX']
non_subject_object_candidates_form = ['yang', 'adalah']
non_predicate_candidates_form = ['yang']
num_siblings = 1  # bigram


def extract_triples_by_root_children(conllu_s, header):
    """
    Extract features (triples) for clustering from sentence (conllu_s)
    by combining sentence root/header with 2 of its children
    """
    # find all direct branches of header
    direct_branches = []
    for id, row in conllu_s.iteritems():
        # children (direct branches of header)
        if (
            row['head'] == header['id'] and
            row['upostag'] in subject_object_candidates_pos and
            row['form'] not in non_subject_object_candidates_form
        ):
            direct_branches.append(id)

    # yield triples combinations
    if len(direct_branches) > 1:
        for combi in itertools.combinations(direct_branches, 2):
            first = None
            third = None
            if combi[0] < header['id'] and header['id'] < combi[1]:
                first = conllu_s[combi[0]]
                third = conllu_s[combi[1]]
            elif combi[1] < header['id'] and header['id'] < combi[0]:
                first = conllu_s[combi[1]]
                third = conllu_s[combi[0]]

            if first and third:
                second = conllu_s[header['id']]
                yield (first, second, third)


def extract_triples_by_combinations(conllu_s, header):
    """
    Extract features (triples) for clustering from sentence (conllu_s)
    by enumerating all possible triple combination of word
    """
    num_tokens = len(conllu_s)
    # sentence start from 1
    for i in range(1, num_tokens - 2):
        first = conllu_s[i]
        # RULES for Subject
        if (
            first['upostag'] in subject_object_candidates_pos and
            first['form'] not in non_subject_object_candidates_form and
            (first['deprel'] not in ['compound', 'name'] or first['head_distance'] > 2)
        ):
            for j in range(i + 1, num_tokens - 1):
                second = conllu_s[j]
                # RULES for Predicate
                if (
                    second['upostag'] in predicate_candidates_pos
                ):
                    for k in range(j + 1, num_tokens):
                        third = conllu_s[k]
                        # RULES for Object
                        if (
                            third['upostag'] in subject_object_candidates_pos and
                            third['form'] not in non_subject_object_candidates_form and
                            (third['deprel'] not in ['compound', 'name'] or third['head_distance'] > 2) and
                            (third['upostag'] not in predicate_candidates_pos or first['upostag'] not in predicate_candidates_pos)
                        ):
                            s = first['flatten_s']
                            p = second['flatten_p']
                            if third['nearest_adp_id']:
                                p += ' ' + conllu_s[third['nearest_adp_id']]['form']
                            o = third['flatten_o']
                            yield (first, second, third, s, p, o)


def extract_triples_by_children_combination(conllu_s, header):
    """
    Extract features (triples) for clustering from sentence (conllu_s)
    by combining sentence predicate nodes with 2 of their children
    """
    for k, v in conllu_s.items():
        # RULES for Subject, Predicate and Object
        if (
            v['upostag'] in predicate_candidates_pos and
            v['form'] not in non_predicate_candidates_form
        ):
            for first, second, third in extract_triples_by_root_children(conllu_s, v):
                yield (first, second, third)


def trace_children_pos(child_pos_list, parent_pos, node, s):
    """
    Find parent that has parent_pos pos tag and has one child of child_pos
    """
    parent_pos_list = [parent_pos] if parent_pos not in ['NOUN', 'PROPN'] else ['NOUN', 'PROPN']
    if node['deprel'] == 'root' or node['upostag'] not in parent_pos_list:
        return None
    else:
        # find child with upostag == child_pos
        for child_id in node['children']:
            if s[child_id]['upostag'] in child_pos_list:
                return s[child_id]

        # if not found try to search on node's parent
        return trace_children_pos(child_pos_list, parent_pos, s[node['head']], s)


def remove_token_if_first(field, values, tokens):
    while (tokens and tokens[0][1][field] in values):
        tokens.pop(0)


def remove_token_if_last(field, values, tokens):
    while (tokens and tokens[-1][1][field] in values):
        tokens.pop(-1)


def remove_token_if_first_or_last(field, values, tokens):
    remove_token_if_first(field, values, tokens)
    remove_token_if_last(field, values, tokens)


def expand_node(node, s):
    """
    Expand node to its children as dict
    """
    expanded = {node['id']: node}
    has_quote = False
    # EXPAND RULES

    for k in node['children']:
        v = s[k]
        if v['deprel'] in ['compound', 'name', 'amod']:
            expanded.update(expand_node(v, s))
        elif v['entity'] and v['entity'] == node['entity'] and abs(v['id'] - node['id']) == 1:
            expanded.update(expand_node(v, s))
        elif has_quote:
            expanded.update(expand_node(v, s))
        elif node['deprel'] == 'root':     # [Sembungan adalah sebuah] (desa) [.]
            continue
        else:
            if v['form'] in ['\'', '"']:  # (" Lelaki dan Telaga ")
                has_quote = True
            if (v['upostag'] in ['CONJ'] or v['form'] in [',', '/']):  # (kecamatan) Kejajar [, kabupaten Wonosobo]
                break
            if v['upostag'] in ['VERB', 'ADP']:  # (helm) Brodie [yang dipakai]
                continue
            if v['children'] and 'ADP' in [s[i]['upostag'] for i in v['children']]:  # (Stahlhelm) Jerman [dengan perbaikan desain], [Beberapa bulan sebelum] (Rose)
                continue
            expanded.update(expand_node(v, s))

    return expanded


def flatten_node(node, s, expand_as='o', mark_head=False):
    """
    Expand node and its branches to clause string
    """
    if expand_as.lower() in ['s', 'o']:
        expanded = expand_node(node, s)
        sorted_nodes = sorted(expanded.items())

        # EXPAND RULES
        remove_token_if_first_or_last('upostag', ['CONJ', 'ADP'], sorted_nodes)
        remove_token_if_first('form', [')'], sorted_nodes)
        remove_token_if_last('form', ['(', 'yang'], sorted_nodes)

        text = ' '.join([v['form'] if not mark_head or k != node['id'] else '({})'.format(v['form']) for k, v in sorted_nodes])
        ids = [k for k, v in sorted_nodes]
    elif expand_as.lower() in ['p']:
        text = node['form'] if not mark_head else '({})'.format(node['form'])
        ids = [node['id']]

        # EXPAND RULES
        negation_node = [s[c_id] for c_id in node['children'] if s[c_id]['form'].lower() == 'tidak']
        if negation_node:
            text = negation_node[0]['form'] + ' ' + text
            ids = [negation_node[0]['id']] + ids

    return text, ids


def flatten_conllu_sentence(conllu_s):
    return ' '.join([token['form'] for token in conllu_s.values()])


def set_extra_properties(s, children, mark_head=False):
    """
    Retrieve head's pos tag
    Flatten subject/object candidates
    """
    for k, v in s.iteritems():
        # get head pos tag
        s[k]['head_upostag'] = s[v['head']]['upostag'] if v['head'] > 0 else ''
        # get siblings pos tags
        before = v['id'] - num_siblings
        s[k]['before_upostag'] = [s[i]['upostag'] if i > 0 else '' for i in range(before, v['id'])]
        after = v['id'] + num_siblings + 1
        s[k]['before_upostag'] = [s[i]['upostag'] if i < len(s) else '' for i in range(after - num_siblings, after)]
        # get children id
        if k in children:
            sorted_children = sorted(children[k])
            s[k]['children'] = sorted_children

    # loop once more to flatten as children is required
    for k, v in s.iteritems():
        if v['upostag'] in subject_object_candidates_pos:
            s[k]['flatten_s'], s[k]['flatten_s_id'] = flatten_node(s[k], s, expand_as='s', mark_head=mark_head)
            s[k]['flatten_o'], s[k]['flatten_o_id'] = flatten_node(s[k], s, expand_as='o', mark_head=mark_head)
            # trace ADP node to parents to be inherited
            if v['head'] > 0:
                nearest_adp_node = trace_children_pos(['ADP'], v['upostag'], v, s)
                if nearest_adp_node:
                    s[k]['nearest_adp_id'] = nearest_adp_node['id']
        if v['upostag'] == 'VERB':
            s[k]['flatten_p'], s[k]['flatten_p_id'] = flatten_node(s[k], s, expand_as='p', mark_head=mark_head)


def get_neigbour_upostag(position, token):
    key = position + '_upostag'
    if position not in ['before', 'after'] or not token[key]:
        return postag.index('')
    return postag.index(token[key][0])


def get_next_upostag(token):
    return get_neigbour_upostag('after', token)


def get_prev_upostag(token):
    return get_neigbour_upostag('before', token)


def vectorize(first, second, third):
    """
    Convert a triple's member to feature vector
    """
    distance_first_second = abs(first['id'] - second['id'])
    distance_second_third = abs(second['id'] - third['id'])
    first_is_child_of_second = 1 if first['id'] in second['children'] else 0
    third_is_child_of_second = 1 if third['id'] in second['children'] else 0

    vector = []
    vector.append(postag.index(first['upostag']))
    vector.append(deprel.index(first['deprel']))
    vector.append(postag.index(first['head_upostag']))
    vector.append(entity.index(first['entity']))
    vector.append(len(first['children']))
    vector.append(distance_first_second)
    vector.append(first_is_child_of_second)
    vector.append(get_prev_upostag(first))
    vector.append(get_next_upostag(first))
    vector.append(1 if first['nearest_adp_id'] else 0)

    vector.append(postag.index(second['upostag']))
    vector.append(deprel.index(second['deprel']))
    vector.append(postag.index(second['head_upostag']))
    vector.append(entity.index(second['entity']))
    vector.append(len(second['children']))
    vector.append(get_prev_upostag(second))
    vector.append(get_next_upostag(second))

    vector.append(postag.index(third['upostag']))
    vector.append(deprel.index(third['deprel']))
    vector.append(postag.index(third['head_upostag']))
    vector.append(entity.index(third['entity']))
    vector.append(len(third['children']))
    vector.append(distance_second_third)
    vector.append(third_is_child_of_second)
    vector.append(get_prev_upostag(third))
    vector.append(get_next_upostag(third))
    vector.append(1 if third['nearest_adp_id'] else 0)

    return vector


def parse_connlu_file(conllu_file, mark_head=False):
    with open(conllu_file, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t', quoting=csv.QUOTE_NONE)
        s = {}
        children = {}
        s_header = None
        index = 0
        for row in reader:
            if len(row) > 0:
                id = int(row[conllu.index('ID')])
                head_id = int(row[conllu.index('HEAD')])
                deprel = row[conllu.index('DEPREL')].split(':')[0]  # ignore sub relation
                obj = {
                    'id': id,
                    'sentence_id': index,
                    'form': row[conllu.index('FORM')],
                    'upostag': row[conllu.index('UPOSTAG')],
                    'head': head_id,
                    'head_distance': abs(head_id - id) if head_id > 0 else 0,
                    'deprel': deprel if deprel != '_' else 'root',
                    'head_upostag': '',
                    'before_upostag': [],
                    'after_upostag': [],
                    'flatten_s': row[conllu.index('FORM')],
                    'flatten_p': row[conllu.index('FORM')],
                    'flatten_o': row[conllu.index('FORM')],
                    'flatten_s_id': [id],
                    'flatten_p_id': [id],
                    'flatten_o_id': [id],
                    'entity': row[conllu.index('MISC')] if row[conllu.index('MISC')] != '_' else '',
                    'children': [],
                    'nearest_adp_id': None
                }
                s[id] = obj
                # map children
                if obj['head'] != 0:
                    if obj['head'] not in children:
                        children[obj['head']] = []
                    if id not in children[obj['head']]:
                        children[obj['head']].append(id)
                # find root header
                s_header = obj if obj['head'] == 0 else s_header
            else:
                set_extra_properties(s, children, mark_head)
                yield index, s, s_header
                s = {}
                index += 1
                children = {}
        if s:
            # if last element not a blank
            set_extra_properties(s, children, mark_head)
            yield index, s, s_header


def get_best_features():
    return BEST_FEATURES
