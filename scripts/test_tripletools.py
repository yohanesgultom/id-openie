import tripletools

conllu_sentence_1 = '''1	Cintaku	_	PROPN	_	_	6	nsubj	_	OTHER
2	di	_	PROPN	_	_	1	nmod	_	OTHER
3	Rumah	_	PROPN	_	_	2	nmod	_	OTHER
4	Susun	_	PROPN	_	_	3	name	_	OTHER
5	adalah	_	VERB	_	_	6	cop	_	_
6	film	_	NOUN	_	_	0	root	_	_
7	komedi	_	NOUN	_	_	6	compound	_	_
8	situasi	_	NOUN	_	_	7	compound	_	_
9	.	_	PUNCT	_	_	6	punct	_	_

'''

conllu_features_1 = {
    1: {'upostag': 'PROPN', 'flatten_s': 'Cintaku di Rumah Susun', 'head': 6, 'form': 'Cintaku', 'flatten_o_id': [1, 2, 3, 4], 'after_upostag': [], 'flatten_p': 'Cintaku', 'children': [2], 'head_distance': 5, 'before_upostag': ['PROPN'], 'head_upostag': 'NOUN', 'flatten_p_id': [1], 'sentence_id': 0, 'flatten_o': 'Cintaku di Rumah Susun', 'entity': 'OTHER', 'flatten_s_id': [1, 2, 3, 4], 'id': 1, 'deprel': 'nsubj'},
    2: {'upostag': 'PROPN', 'flatten_s': 'di Rumah Susun', 'head': 1, 'form': 'di', 'flatten_o_id': [2, 3, 4], 'after_upostag': [], 'flatten_p': 'di', 'children': [3], 'head_distance': 1, 'before_upostag': ['PROPN'], 'head_upostag': 'PROPN', 'flatten_p_id': [2], 'sentence_id': 0, 'flatten_o': 'di Rumah Susun', 'entity': 'OTHER', 'flatten_s_id': [2, 3, 4], 'id': 2, 'deprel': 'nmod'},
    3: {'upostag': 'PROPN', 'flatten_s': 'Rumah Susun', 'head': 2, 'form': 'Rumah', 'flatten_o_id': [3, 4], 'after_upostag': [], 'flatten_p': 'Rumah', 'children': [4], 'head_distance': 1, 'before_upostag': ['PROPN'], 'head_upostag': 'PROPN', 'flatten_p_id': [3], 'sentence_id': 0, 'flatten_o': 'Rumah Susun', 'entity': 'OTHER', 'flatten_s_id': [3, 4], 'id': 3, 'deprel': 'nmod'},
    4: {'upostag': 'PROPN', 'flatten_s': 'Susun', 'head': 3, 'form': 'Susun', 'flatten_o_id': [4], 'after_upostag': [], 'flatten_p': 'Susun', 'children': [], 'head_distance': 1, 'before_upostag': ['VERB'], 'head_upostag': 'PROPN', 'flatten_p_id': [4], 'sentence_id': 0, 'flatten_o': 'Susun', 'entity': 'OTHER', 'flatten_s_id': [4], 'id': 4, 'deprel': 'name'},
    5: {'upostag': 'VERB', 'flatten_s': 'adalah', 'head': 6, 'form': 'adalah', 'flatten_o_id': [5], 'after_upostag': [], 'flatten_p': 'adalah', 'children': [], 'head_distance': 1, 'before_upostag': ['NOUN'], 'head_upostag': 'NOUN', 'flatten_p_id': [5], 'sentence_id': 0, 'flatten_o': 'adalah', 'entity': '', 'flatten_s_id': [5], 'id': 5, 'deprel': 'cop'},
    6: {'upostag': 'NOUN', 'flatten_s': 'film komedi situasi', 'head': 0, 'form': 'film', 'flatten_o_id': [6, 7, 8], 'after_upostag': [], 'flatten_p': 'film', 'children': [1, 5, 7, 9], 'head_distance': 0, 'before_upostag': ['NOUN'], 'head_upostag': '', 'flatten_p_id': [6], 'sentence_id': 0, 'flatten_o': 'film komedi situasi', 'entity': '', 'flatten_s_id': [6, 7, 8], 'id': 6, 'deprel': 'root'},
    7: {'upostag': 'NOUN', 'flatten_s': 'komedi situasi', 'head': 6, 'form': 'komedi', 'flatten_o_id': [7, 8], 'after_upostag': [], 'flatten_p': 'komedi', 'children': [8], 'head_distance': 1, 'before_upostag': ['NOUN'], 'head_upostag': 'NOUN', 'flatten_p_id': [7], 'sentence_id': 0, 'flatten_o': 'komedi situasi', 'entity': '', 'flatten_s_id': [7, 8], 'id': 7, 'deprel': 'compound'},
    8: {'upostag': 'NOUN', 'flatten_s': 'situasi', 'head': 7, 'form': 'situasi', 'flatten_o_id': [8], 'after_upostag': [], 'flatten_p': 'situasi', 'children': [], 'head_distance': 1, 'before_upostag': [''], 'head_upostag': 'NOUN', 'flatten_p_id': [8], 'sentence_id': 0, 'flatten_o': 'situasi', 'entity': '', 'flatten_s_id': [8], 'id': 8, 'deprel': 'compound'},
    9: {'upostag': 'PUNCT', 'flatten_s': '.', 'head': 6, 'form': '.', 'flatten_o_id': [9], 'after_upostag': [], 'flatten_p': '.', 'children': [], 'head_distance': 3, 'before_upostag': [''], 'head_upostag': 'NOUN', 'flatten_p_id': [9], 'sentence_id': 0, 'flatten_o': '.', 'entity': '', 'flatten_s_id': [9], 'id': 9, 'deprel': 'punct'}
}

conllu_sentence_2 = '''1	Sembungan	_	PROPN	_	_	4	nsubj	_	LOCATION
2	adalah	_	VERB	_	_	4	cop	_	_
3	sebuah	_	DET	_	_	4	det	_	_
4	desa	_	NOUN	_	_	0	root	_	_
5	yang	_	PRON	_	_	6	nsubjpass	_	_
6	terletak	_	VERB	_	_	4	acl	_	_
7	di	_	ADP	_	_	8	case	_	_
8	kecamatan	_	NOUN	_	_	6	nmod	_	LOCATION
9	Kejajar	_	PROPN	_	_	8	name	_	LOCATION
10	,	_	PUNCT	_	_	8	punct	_	_
11	kabupaten	_	NOUN	_	_	8	appos	_	LOCATION
12	Wonosobo	_	PROPN	_	_	11	name	_	LOCATION

'''

conllu_features_2 = {
    1: {'upostag': 'PROPN', 'flatten_s': 'Sembungan', 'head': 4, 'form': 'Sembungan', 'flatten_o_id': [1], 'after_upostag': [], 'flatten_p': 'Sembungan', 'children': [], 'head_distance': 3, 'before_upostag': ['VERB'], 'head_upostag': 'NOUN', 'flatten_p_id': [1], 'sentence_id': 0, 'flatten_o': 'Sembungan', 'entity': 'LOCATION', 'flatten_s_id': [1], 'id': 1, 'deprel': 'nsubj'},
    2: {'upostag': 'VERB', 'flatten_s': 'adalah', 'head': 4, 'form': 'adalah', 'flatten_o_id': [2], 'after_upostag': [], 'flatten_p': 'adalah', 'children': [], 'head_distance': 2, 'before_upostag': ['DET'], 'head_upostag': 'NOUN', 'flatten_p_id': [2], 'sentence_id': 0, 'flatten_o': 'adalah', 'entity': '', 'flatten_s_id': [2], 'id': 2, 'deprel': 'cop'},
    3: {'upostag': 'DET', 'flatten_s': 'sebuah', 'head': 4, 'form': 'sebuah', 'flatten_o_id': [3], 'after_upostag': [], 'flatten_p': 'sebuah', 'children': [], 'head_distance': 1, 'before_upostag': ['NOUN'], 'head_upostag': 'NOUN', 'flatten_p_id': [3], 'sentence_id': 0, 'flatten_o': 'sebuah', 'entity': '', 'flatten_s_id': [3], 'id': 3, 'deprel': 'det'},
    4: {'upostag': 'NOUN', 'flatten_s': 'desa', 'head': 0, 'form': 'desa', 'flatten_o_id': [4], 'after_upostag': [], 'flatten_p': 'desa', 'children': [1, 2, 3, 6], 'head_distance': 0, 'before_upostag': ['PRON'], 'head_upostag': '', 'flatten_p_id': [4], 'sentence_id': 0, 'flatten_o': 'desa', 'entity': '', 'flatten_s_id': [4], 'id': 4, 'deprel': 'root'},
    5: {'upostag': 'PRON', 'flatten_s': 'yang', 'head': 6, 'form': 'yang', 'flatten_o_id': [5], 'after_upostag': [], 'flatten_p': 'yang', 'children': [], 'head_distance': 1, 'before_upostag': ['VERB'], 'head_upostag': 'VERB', 'flatten_p_id': [5], 'sentence_id': 0, 'flatten_o': 'yang', 'entity': '', 'flatten_s_id': [5], 'id': 5, 'deprel': 'nsubjpass'},
    6: {'upostag': 'VERB', 'flatten_s': 'yang terletak kecamatan Kejajar , kabupaten Wonosobo', 'head': 4, 'form': 'terletak', 'flatten_o_id': [5, 6, 8, 9, 10, 11, 12], 'after_upostag': [], 'flatten_p': 'terletak', 'children': [5, 8], 'head_distance': 2, 'before_upostag': ['ADP'], 'head_upostag': 'NOUN', 'flatten_p_id': [6], 'sentence_id': 0, 'flatten_o': 'yang terletak kecamatan Kejajar , kabupaten Wonosobo', 'entity': '', 'flatten_s_id': [5, 6, 8, 9, 10, 11, 12], 'id': 6, 'deprel': 'acl'},
    7: {'upostag': 'ADP', 'flatten_s': 'di', 'head': 8, 'form': 'di', 'flatten_o_id': [7], 'after_upostag': [], 'flatten_p': 'di', 'children': [], 'head_distance': 1, 'before_upostag': ['NOUN'], 'head_upostag': 'NOUN', 'flatten_p_id': [7], 'sentence_id': 0, 'flatten_o': 'di', 'entity': '', 'flatten_s_id': [7], 'id': 7, 'deprel': 'case'},
    8: {'upostag': 'NOUN', 'flatten_s': 'kecamatan Kejajar , kabupaten Wonosobo', 'head': 6, 'form': 'kecamatan', 'flatten_o_id': [8, 9, 10, 11, 12], 'after_upostag': [], 'flatten_p': 'kecamatan', 'children': [7, 9, 10, 11], 'head_distance': 2, 'before_upostag': ['PROPN'], 'head_upostag': 'VERB', 'flatten_p_id': [8], 'sentence_id': 0, 'flatten_o': 'kecamatan Kejajar , kabupaten Wonosobo', 'entity': 'LOCATION', 'flatten_s_id': [8, 9, 10, 11, 12], 'id': 8, 'deprel': 'nmod'},
    9: {'upostag': 'PROPN', 'flatten_s': 'Kejajar', 'head': 8, 'form': 'Kejajar', 'flatten_o_id': [9], 'after_upostag': [], 'flatten_p': 'Kejajar', 'children': [], 'head_distance': 1, 'before_upostag': ['PUNCT'], 'head_upostag': 'NOUN', 'flatten_p_id': [9], 'sentence_id': 0, 'flatten_o': 'Kejajar', 'entity': 'LOCATION', 'flatten_s_id': [9], 'id': 9, 'deprel': 'name'},
    10: {'upostag': 'PUNCT', 'flatten_s': ',', 'head': 8, 'form': ',', 'flatten_o_id': [10], 'after_upostag': [], 'flatten_p': ',', 'children': [], 'head_distance': 2, 'before_upostag': ['NOUN'], 'head_upostag': 'NOUN', 'flatten_p_id': [10], 'sentence_id': 0, 'flatten_o': ',', 'entity': '', 'flatten_s_id': [10], 'id': 10, 'deprel': 'punct'},
    11: {'upostag': 'NOUN', 'flatten_s': 'kabupaten Wonosobo', 'head': 8, 'form': 'kabupaten', 'flatten_o_id': [11, 12], 'after_upostag': [], 'flatten_p': 'kabupaten', 'children': [12], 'head_distance': 3, 'before_upostag': [''], 'head_upostag': 'NOUN', 'flatten_p_id': [11], 'sentence_id': 0, 'flatten_o': 'kabupaten Wonosobo', 'entity': 'LOCATION', 'flatten_s_id': [11, 12], 'id': 11, 'deprel': 'appos'},
    12: {'upostag': 'PROPN', 'flatten_s': 'Wonosobo', 'head': 11, 'form': 'Wonosobo', 'flatten_o_id': [12], 'after_upostag': [], 'flatten_p': 'Wonosobo', 'children': [], 'head_distance': 1, 'before_upostag': [''], 'head_upostag': 'NOUN', 'flatten_p_id': [12], 'sentence_id': 0, 'flatten_o': 'Wonosobo', 'entity': 'LOCATION', 'flatten_s_id': [12], 'id': 12, 'deprel': 'name'}
}

conllu_sentence_3 = '''1	Pasukan	_	PROPN	_	_	12	nsubjpass	_	_
2	Mongol	_	PROPN	_	_	1	name	_	ORGANIZATION
3	yang	_	PRON	_	_	5	nsubj	_	_
4	tidak	_	ADV	_	_	5	advmod	_	_
5	tahu	_	VERB	_	_	1	acl	_	_
6	apa	_	NOUN	_	_	5	dobj	_	_
7	yang	_	PRON	_	_	10	dobj	_	_
8	harus	_	ADV	_	_	10	advmod	_	_
9	mereka	_	PRON	_	_	10	nsubj	_	_
10	perbuat	_	VERB	_	_	6	acl	_	_
11	itu	_	DET	_	_	1	det	_	_
12	disiasati	_	VERB	_	_	0	root	_	_

'''

conllu_features_3 = {
    1: {'upostag': 'PROPN', 'flatten_s': 'Pasukan Mongol itu', 'head': 12, 'form': 'Pasukan', 'flatten_o_id': [1, 2, 11], 'after_upostag': [], 'flatten_p': 'Pasukan', 'children': [2, 5, 11], 'head_distance': 11, 'before_upostag': ['PROPN'], 'head_upostag': 'VERB', 'flatten_p_id': [1], 'sentence_id': 0, 'flatten_o': 'Pasukan Mongol itu', 'entity': '', 'flatten_s_id': [1, 2, 11], 'id': 1, 'deprel': 'nsubjpass'},
    2: {'upostag': 'PROPN', 'flatten_s': 'Mongol', 'head': 1, 'form': 'Mongol', 'flatten_o_id': [2], 'after_upostag': [], 'flatten_p': 'Mongol', 'children': [], 'head_distance': 1, 'before_upostag': ['PRON'], 'head_upostag': 'PROPN', 'flatten_p_id': [2], 'sentence_id': 0, 'flatten_o': 'Mongol', 'entity': 'ORGANIZATION', 'flatten_s_id': [2], 'id': 2, 'deprel': 'name'},
    3: {'upostag': 'PRON', 'flatten_s': 'yang', 'head': 5, 'form': 'yang', 'flatten_o_id': [3], 'after_upostag': [], 'flatten_p': 'yang', 'children': [], 'head_distance': 2, 'before_upostag': ['ADV'], 'head_upostag': 'VERB', 'flatten_p_id': [3], 'sentence_id': 0, 'flatten_o': 'yang', 'entity': '', 'flatten_s_id': [3], 'id': 3, 'deprel': 'nsubj'},
    4: {'upostag': 'ADV', 'flatten_s': 'tidak', 'head': 5, 'form': 'tidak', 'flatten_o_id': [4], 'after_upostag': [], 'flatten_p': 'tidak', 'children': [], 'head_distance': 1, 'before_upostag': ['VERB'], 'head_upostag': 'VERB', 'flatten_p_id': [4], 'sentence_id': 0, 'flatten_o': 'tidak', 'entity': '', 'flatten_s_id': [4], 'id': 4, 'deprel': 'advmod'},
    5: {'upostag': 'VERB', 'flatten_s': 'yang tidak tahu apa', 'head': 1, 'form': 'tahu', 'flatten_o_id': [3, 4, 5, 6], 'after_upostag': [], 'flatten_p': 'tidak tahu', 'children': [3, 4, 6], 'head_distance': 4, 'before_upostag': ['NOUN'], 'head_upostag': 'PROPN', 'flatten_p_id': [4, 5], 'sentence_id': 0, 'flatten_o': 'yang tidak tahu apa', 'entity': '', 'flatten_s_id': [3, 4, 5, 6], 'id': 5, 'deprel': 'acl'},
    6: {'upostag': 'NOUN', 'flatten_s': 'apa', 'head': 5, 'form': 'apa', 'flatten_o_id': [6], 'after_upostag': [], 'flatten_p': 'apa', 'children': [10], 'head_distance': 1, 'before_upostag': ['PRON'], 'head_upostag': 'VERB', 'flatten_p_id': [6], 'sentence_id': 0, 'flatten_o': 'apa', 'entity': '', 'flatten_s_id': [6], 'id': 6, 'deprel': 'dobj'},
    7: {'upostag': 'PRON', 'flatten_s': 'yang', 'head': 10, 'form': 'yang', 'flatten_o_id': [7], 'after_upostag': [], 'flatten_p': 'yang', 'children': [], 'head_distance': 3, 'before_upostag': ['ADV'], 'head_upostag': 'VERB', 'flatten_p_id': [7], 'sentence_id': 0, 'flatten_o': 'yang', 'entity': '', 'flatten_s_id': [7], 'id': 7, 'deprel': 'dobj'},
    8: {'upostag': 'ADV', 'flatten_s': 'harus', 'head': 10, 'form': 'harus', 'flatten_o_id': [8], 'after_upostag': [], 'flatten_p': 'harus', 'children': [], 'head_distance': 2, 'before_upostag': ['PRON'], 'head_upostag': 'VERB', 'flatten_p_id': [8], 'sentence_id': 0, 'flatten_o': 'harus', 'entity': '', 'flatten_s_id': [8], 'id': 8, 'deprel': 'advmod'},
    9: {'upostag': 'PRON', 'flatten_s': 'mereka', 'head': 10, 'form': 'mereka', 'flatten_o_id': [9], 'after_upostag': [], 'flatten_p': 'mereka', 'children': [], 'head_distance': 1, 'before_upostag': ['VERB'], 'head_upostag': 'VERB', 'flatten_p_id': [9], 'sentence_id': 0, 'flatten_o': 'mereka', 'entity': '', 'flatten_s_id': [9], 'id': 9, 'deprel': 'nsubj'},
    10: {'upostag': 'VERB', 'flatten_s': 'yang harus mereka perbuat', 'head': 6, 'form': 'perbuat', 'flatten_o_id': [7, 8, 9, 10], 'after_upostag': [], 'flatten_p': 'perbuat', 'children': [7, 8, 9], 'head_distance': 4, 'before_upostag': ['DET'], 'head_upostag': 'NOUN', 'flatten_p_id': [10], 'sentence_id': 0, 'flatten_o': 'yang harus mereka perbuat', 'entity': '', 'flatten_s_id': [7, 8, 9, 10], 'id': 10, 'deprel': 'acl'},
    11: {'upostag': 'DET', 'flatten_s': 'itu', 'head': 1, 'form': 'itu', 'flatten_o_id': [11], 'after_upostag': [], 'flatten_p': 'itu', 'children': [], 'head_distance': 10, 'before_upostag': [''], 'head_upostag': 'PROPN', 'flatten_p_id': [11], 'sentence_id': 0, 'flatten_o': 'itu', 'entity': '', 'flatten_s_id': [11], 'id': 11, 'deprel': 'det'},
    12: {'upostag': 'VERB', 'flatten_s': 'disiasati', 'head': 0, 'form': 'disiasati', 'flatten_o_id': [12], 'after_upostag': [], 'flatten_p': 'disiasati', 'children': [1], 'head_distance': 0, 'before_upostag': [''], 'head_upostag': '', 'flatten_p_id': [12], 'sentence_id': 0, 'flatten_o': 'disiasati', 'entity': '', 'flatten_s_id': [12], 'id': 12, 'deprel': 'root'}
}


conllu_sentence_4 = '''1	Perkembangan	_	NOUN	_	_	3	nsubjpass	_	_
2	ini	_	DET	_	_	1	det	_	_
3	diikuti	_	VERB	_	_	0	root	_	_
4	oleh	_	ADP	_	_	5	case	_	_
5	helm	_	NOUN	_	_	3	nmod	_	OTHER
6	Brodie	_	PROPN	_	_	5	name	_	OTHER
7	yang	_	PRON	_	_	8	nsubjpass	_	_
8	dipakai	_	VERB	_	_	5	acl	_	_
9	tentara	_	NOUN	_	_	8	nmod	_	_
10	Imperium	_	PROPN	_	_	9	name	_	LOCATION
11	Britania	_	PROPN	_	_	10	name	_	LOCATION
12	dan	_	CONJ	_	_	11	cc	_	_
13	AS	_	PROPN	_	_	11	conj	_	LOCATION

'''

conllu_features_4 = {
    1: {'upostag': 'NOUN', 'flatten_s': 'Perkembangan ini', 'head': 3, 'form': 'Perkembangan', 'flatten_o_id': [1, 2], 'after_upostag': [], 'flatten_p': 'Perkembangan', 'children': [2], 'head_distance': 2, 'before_upostag': ['DET'], 'head_upostag': 'VERB', 'flatten_p_id': [1], 'sentence_id': 0, 'flatten_o': 'Perkembangan ini', 'nearest_adp_id': None, 'entity': '', 'flatten_s_id': [1, 2], 'id': 1, 'deprel': 'nsubjpass'},
    2: {'upostag': 'DET', 'flatten_s': 'ini', 'head': 1, 'form': 'ini', 'flatten_o_id': [2], 'after_upostag': [], 'flatten_p': 'ini', 'children': [], 'head_distance': 1, 'before_upostag': ['VERB'], 'head_upostag': 'NOUN', 'flatten_p_id': [2], 'sentence_id': 0, 'flatten_o': 'ini', 'nearest_adp_id': None, 'entity': '', 'flatten_s_id': [2], 'id': 2, 'deprel': 'det'},
    3: {'upostag': 'VERB', 'flatten_s': 'Perkembangan ini diikuti helm Brodie', 'head': 0, 'form': 'diikuti', 'flatten_o_id': [1, 2, 3, 5, 6], 'after_upostag': [], 'flatten_p': 'diikuti', 'children': [1, 5], 'head_distance': 0, 'before_upostag': ['ADP'], 'head_upostag': '', 'flatten_p_id': [3], 'sentence_id': 0, 'flatten_o': 'Perkembangan ini diikuti helm Brodie', 'nearest_adp_id': None, 'entity': '', 'flatten_s_id': [1, 2, 3, 5, 6], 'id': 3, 'deprel': 'root'},
    4: {'upostag': 'ADP', 'flatten_s': 'oleh', 'head': 5, 'form': 'oleh', 'flatten_o_id': [4], 'after_upostag': [], 'flatten_p': 'oleh', 'children': [], 'head_distance': 1, 'before_upostag': ['NOUN'], 'head_upostag': 'NOUN', 'flatten_p_id': [4], 'sentence_id': 0, 'flatten_o': 'oleh', 'nearest_adp_id': None, 'entity': '', 'flatten_s_id': [4], 'id': 4, 'deprel': 'case'},
    5: {'upostag': 'NOUN', 'flatten_s': 'helm Brodie', 'head': 3, 'form': 'helm', 'flatten_o_id': [5, 6], 'after_upostag': [], 'flatten_p': 'helm', 'children': [4, 6, 8], 'head_distance': 2, 'before_upostag': ['PROPN'], 'head_upostag': 'VERB', 'flatten_p_id': [5], 'sentence_id': 0, 'flatten_o': 'helm Brodie', 'nearest_adp_id': 4, 'entity': 'OTHER', 'flatten_s_id': [5, 6], 'id': 5, 'deprel': 'nmod'},
    6: {'upostag': 'PROPN', 'flatten_s': 'Brodie', 'head': 5, 'form': 'Brodie', 'flatten_o_id': [6], 'after_upostag': [], 'flatten_p': 'Brodie', 'children': [], 'head_distance': 1, 'before_upostag': ['PRON'], 'head_upostag': 'NOUN', 'flatten_p_id': [6], 'sentence_id': 0, 'flatten_o': 'Brodie', 'nearest_adp_id': 4, 'entity': 'OTHER', 'flatten_s_id': [6], 'id': 6, 'deprel': 'name'},
    7: {'upostag': 'PRON', 'flatten_s': 'yang', 'head': 8, 'form': 'yang', 'flatten_o_id': [7], 'after_upostag': [], 'flatten_p': 'yang', 'children': [], 'head_distance': 1, 'before_upostag': ['VERB'], 'head_upostag': 'VERB', 'flatten_p_id': [7], 'sentence_id': 0, 'flatten_o': 'yang', 'nearest_adp_id': None, 'entity': '', 'flatten_s_id': [7], 'id': 7, 'deprel': 'nsubjpass'},
    8: {'upostag': 'VERB', 'flatten_s': 'yang dipakai tentara Imperium Britania', 'head': 5, 'form': 'dipakai', 'flatten_o_id': [7, 8, 9, 10, 11], 'after_upostag': [], 'flatten_p': 'dipakai', 'children': [7, 9], 'head_distance': 3, 'before_upostag': ['NOUN'], 'head_upostag': 'NOUN', 'flatten_p_id': [8], 'sentence_id': 0, 'flatten_o': 'yang dipakai tentara Imperium Britania', 'nearest_adp_id': None, 'entity': '', 'flatten_s_id': [7, 8, 9, 10, 11], 'id': 8, 'deprel': 'acl'},
    9: {'upostag': 'NOUN', 'flatten_s': 'tentara Imperium Britania', 'head': 8, 'form': 'tentara', 'flatten_o_id': [9, 10, 11], 'after_upostag': [], 'flatten_p': 'tentara', 'children': [10], 'head_distance': 1, 'before_upostag': ['PROPN'], 'head_upostag': 'VERB', 'flatten_p_id': [9], 'sentence_id': 0, 'flatten_o': 'tentara Imperium Britania', 'nearest_adp_id': None, 'entity': '', 'flatten_s_id': [9, 10, 11], 'id': 9, 'deprel': 'nmod'},
    10: {'upostag': 'PROPN', 'flatten_s': 'Imperium Britania', 'head': 9, 'form': 'Imperium', 'flatten_o_id': [10, 11], 'after_upostag': [], 'flatten_p': 'Imperium', 'children': [11], 'head_distance': 1, 'before_upostag': ['PROPN'], 'head_upostag': 'NOUN', 'flatten_p_id': [10], 'sentence_id': 0, 'flatten_o': 'Imperium Britania', 'nearest_adp_id': None, 'entity': 'LOCATION', 'flatten_s_id': [10, 11], 'id': 10, 'deprel': 'name'},
    11: {'upostag': 'PROPN', 'flatten_s': 'Britania', 'head': 10, 'form': 'Britania', 'flatten_o_id': [11], 'after_upostag': [], 'flatten_p': 'Britania', 'children': [12, 13], 'head_distance': 1, 'before_upostag': ['CONJ'], 'head_upostag': 'PROPN', 'flatten_p_id': [11], 'sentence_id': 0, 'flatten_o': 'Britania', 'nearest_adp_id': None, 'entity': 'LOCATION', 'flatten_s_id': [11], 'id': 11, 'deprel': 'name'},
    12: {'upostag': 'CONJ', 'flatten_s': 'dan', 'head': 11, 'form': 'dan', 'flatten_o_id': [12], 'after_upostag': [], 'flatten_p': 'dan', 'children': [], 'head_distance': 1, 'before_upostag': [''], 'head_upostag': 'PROPN', 'flatten_p_id': [12], 'sentence_id': 0, 'flatten_o': 'dan', 'nearest_adp_id': None, 'entity': '', 'flatten_s_id': [12], 'id': 12, 'deprel': 'cc'},
    13: {'upostag': 'PROPN', 'flatten_s': 'AS', 'head': 11, 'form': 'AS', 'flatten_o_id': [13], 'after_upostag': [], 'flatten_p': 'AS', 'children': [], 'head_distance': 2, 'before_upostag': [''], 'head_upostag': 'PROPN', 'flatten_p_id': [13], 'sentence_id': 0, 'flatten_o': 'AS', 'nearest_adp_id': None, 'entity': 'LOCATION', 'flatten_s_id': [13], 'id': 13, 'deprel': 'conj'}
}


def test_vectorize():
    s = conllu_features_1
    v = tripletools.vectorize(s[1], s[5], s[6])
    assert v == [12, 27, 8, 6, 1, 4, 0, 16, 13, 8, 8, 35, 0, 0, 4, 1, 0]

    s = conllu_features_2
    v = tripletools.vectorize(s[1], s[2], s[4])
    assert v == [12, 27, 8, 2, 0, 1, 0, 16, 13, 8, 8, 35, 0, 0, 4, 2, 0]


def test_expand_node():
    expanded = sorted(tripletools.expand_node(conllu_features_2[8], conllu_features_2).items())
    assert ' '.join([token[1]['form'] for token in expanded]) == 'kecamatan Kejajar'

    expanded = sorted(tripletools.expand_node(conllu_features_4[9], conllu_features_4).items())
    assert ' '.join([token[1]['form'] for token in expanded]) == 'tentara Imperium Britania'


def test_flatten_node_for_object():
    n = conllu_features_4[9]
    assert tripletools.flatten_node(n, conllu_features_4, expand_as='o') == ('tentara Imperium Britania', [9, 10, 11])


def test_flatten_node_for_predicate():
    n = conllu_features_2[2]
    assert tripletools.flatten_node(n, conllu_features_2, expand_as='p') == ('adalah', [2])

    n = conllu_features_2[6]
    assert tripletools.flatten_node(n, conllu_features_2, expand_as='p') == ('terletak', [6])

    n = conllu_features_3[5]
    assert tripletools.flatten_node(n, conllu_features_3, expand_as='p') == ('tidak tahu', [4, 5])


# def test_parse_connlu_file(tmpdir):
#     p = tmpdir.join('temp4.conllu')
#     p.write(conllu_sentence_4)
#     actual = [{'index': index, 's': s, 's_header': s_header} for index, s, s_header in tripletools.parse_connlu_file(str(p))]
#     assert actual == [{'index': 0, 's': conllu_features_4, 's_header': conllu_features_4[3]}]

#     p = tmpdir.join('temp1.conllu')
#     p.write(conllu_sentence_1)
#     actual = [{'index': index, 's': s, 's_header': s_header} for index, s, s_header in tripletools.parse_connlu_file(str(p))]
#     assert actual == [{'index': 0, 's': conllu_features_1, 's_header': conllu_features_1[6]}]
#
#     p = tmpdir.join('temp2.conllu')
#     p.write(conllu_sentence_2)
#     actual = [{'index': index, 's': s, 's_header': s_header} for index, s, s_header in tripletools.parse_connlu_file(str(p))]
#     assert actual == [{'index': 0, 's': conllu_features_2, 's_header': conllu_features_2[4]}]
#
#     p = tmpdir.join('temp3.conllu')
#     p.write(conllu_sentence_3)
#     actual = [{'index': index, 's': s, 's_header': s_header} for index, s, s_header in tripletools.parse_connlu_file(str(p))]
#     assert actual == [{'index': 0, 's': conllu_features_3, 's_header': conllu_features_3[12]}]


def test_flatten_conllu_sentence():
    assert tripletools.flatten_conllu_sentence(conllu_features_1) == 'Cintaku di Rumah Susun adalah film komedi situasi .'
    assert tripletools.flatten_conllu_sentence(conllu_features_2) == 'Sembungan adalah sebuah desa yang terletak di kecamatan Kejajar , kabupaten Wonosobo'
    assert tripletools.flatten_conllu_sentence(conllu_features_3) == 'Pasukan Mongol yang tidak tahu apa yang harus mereka perbuat itu disiasati'
