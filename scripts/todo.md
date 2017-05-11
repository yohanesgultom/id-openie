# Todo

* Latar belakang optimisasi metrik (recall atau precision). Pertimbangkan pakai varian f1
* Tujuan candidate generation harus high recall
* Masukkan error analysis
* Perjelas definisi triple
* Perjelas scope (mana yang masuk dan di luar scope)

# Misc

* Infer knowledge from entity
* Co-reference resolution

# Selecting Triples

* Select triples with different POS structure eg:
    * X-ADP-Y (perbandingan-pada-hewan, adenoma-pada-kelenjar hipofisis)
    * X-PRON-Y (ajaran-yang-bervariasi)
    * X-ADJ-Y (Versi remix Hurt-populer di-kalangan penggemar musik urban)
    * X-Y-ADJ (Duryodana-merasa-cemburu)

* Split inheritable token eg:
    * satu atau dua buah (torpedo) -> (1) satu buah (torpedo), (2) dua buah (torpedo)
    * (chi) universal dan surgawi -> (1) chi universal, (2) chi surgawi
    * seorang pelatih dan pemain sepak bola -> (1) seorang pelatih sepak bola, (2) seorang pemain sepak bola

* Special patterns eg:
    * Melingge adalah gampong di kecamatan Pulo Aceh, kabupaten Aceh Besar, Indonesia -> (1) Melingge-adalah-gampong, (2) Melingge-terletak di-Pulo  Aceh, (3) Pulo Aceh-terletak di-kabupaten Aceh Besar

* Append 'ketika' (SCONJ) to predicate eg:
    * kehancuran tiga Gojoseon mulai ketika Yan menyerang Gojoseon -> kehancuran tiga Gojoseon-mulai ketika-Yan menyerang Gojoseon

* Rearrange clause eg:
    * Bulan November , pasukan Cakraningrat merebut Kartasura kembali -> (1) pasukan Cakraningrat-merebut-Kartasura, (2) pasukan Cakraningrat-merebut pada-bulan November

* Extracting implicit triples from such sentence

```
1	Tidak	_	PART	_	_	2	neg	_	_
2	ada	_	VERB	_	_	0	root	_	_
3	keterangan	_	NOUN	_	_	2	dobj	_	_
4	kejatuhan	_	NOUN	_	_	3	compound	_	_
5	Yerusalem	_	PROPN	_	_	4	name	_	LOCATION
6	(	_	PUNCT	_	_	7	punct	_	_
7	berbeda	_	VERB	_	_	3	appos	_	_
8	dengan	_	ADP	_	_	9	case	_	_
9	kota	_	NOUN	_	_	7	nmod	_	_
10	-	_	PUNCT	_	_	9	punct	_	_
11	kota	_	NOUN	_	_	9	mwe	_	_
12	lain	_	ADJ	_	_	9	amod	_	_
13	)	_	PUNCT	_	_	7	punct	_	_
14	maupun	_	CONJ	_	_	2	cc	_	_
15	gagalnya	_	NOUN	_	_	17	nsubj	_	_
16	Sanherib	_	NOUN	_	_	15	compound	_	PERSON
17	merebut	_	VERB	_	_	2	conj	_	_
18	Yerusalem	_	NOUN	_	_	17	dobj	_	LOCATION
19	.	_	PUNCT	_	_	2	punct	_	_

1	Kota	_	NOUN	_	_	3	det	_	_
2	ini	_	DET	_	_	1	det	_	_
3	letaknya	_	NOUN	_	_	0	root	_	_
4	di	_	ADP	_	_	5	case	_	_
5	bagian	_	NOUN	_	_	3	nmod	_	_
6	utara	_	NOUN	_	_	5	amod	_	OTHER
7	.	_	PUNCT	_	_	3	punct	_	_

1	Apa	_	NOUN	_	_	0	root	_	_
2	yang	_	PRON	_	_	4	dobj	_	_
3	ia	_	PRON	_	_	4	nsubj	_	_
4	lakukan	_	VERB	_	_	1	acl	_	_
5	,	_	PUNCT	_	_	1	punct	_	_
6	dan	_	CONJ	_	_	1	cc	_	_
7	mengapa	_	NOUN	_	_	1	conj	_	_
8	ia	_	PRON	_	_	9	nsubj	_	_
9	melakukannya	_	VERB	_	_	7	acl	_	_
10	?	_	PUNCT	_	_	1	punct	_	_

1	Lelaki	_	PROPN	_	_	5	nsubj	_	OTHER
2	dan	_	CONJ	_	_	1	cc	_	OTHER
3	Telaga	_	PROPN	_	_	1	conj	_	OTHER
4	adalah	_	VERB	_	_	5	cop	_	_
5	album	_	NOUN	_	_	0	root	_	_
6	solo	_	NOUN	_	_	5	amod	_	_
7	Franky	_	PROPN	_	_	5	name	_	PERSON
8	Sahilatua	_	PROPN	_	_	7	name	_	PERSON
9	yang	_	PRON	_	_	10	nmod	_	_
10	berisi	_	VERB	_	_	5	acl	_	_
11	tiga	_	NUM	_	_	12	nummod	_	_
12	lagu	_	NOUN	_	_	10	dobj	_	_
13	baru	_	ADJ	_	_	12	amod	_	_
14	(	_	PUNCT	_	_	16	punct	_	_
15	"	_	PUNCT	_	_	16	punct	_	OTHER
16	Lelaki	_	PROPN	_	_	12	appos	_	OTHER
17	dan	_	CONJ	_	_	16	cc	_	OTHER
18	Telaga	_	PROPN	_	_	16	conj	_	OTHER
19	"	_	PUNCT	_	_	16	punct	_	OTHER
20	,	_	PUNCT	_	_	16	punct	_	_
21	"	_	PUNCT	_	_	22	punct	_	OTHER
22	Hitam	_	PROPN	_	_	16	conj	_	OTHER
23	Putih	_	PROPN	_	_	22	name	_	OTHER
24	"	_	PUNCT	_	_	22	punct	_	OTHER
25	,	_	PUNCT	_	_	22	punct	_	_
26	dan	_	CONJ	_	_	16	cc	_	_
27	"	_	PUNCT	_	_	28	punct	_	OTHER
28	Nyanyian	_	PROPN	_	_	16	conj	_	OTHER
29	Para	_	PROPN	_	_	30	det	_	OTHER
30	Mantan	_	PROPN	_	_	28	name	_	OTHER
31	"	_	PUNCT	_	_	28	punct	_	OTHER
32	)	_	PUNCT	_	_	16	punct	_	_
33	dan	_	CONJ	_	_	10	cc	_	_
34	sisanya	_	NOUN	_	_	36	nsubj	_	_
35	adalah	_	VERB	_	_	36	cop	_	_
36	lagu	_	NOUN	_	_	10	conj	_	_
37	-	_	PUNCT	_	_	36	punct	_	_
38	lagu	_	NOUN	_	_	36	mwe	_	_
39	yang	_	PRON	_	_	40	nsubjpass	_	_
40	diambil	_	VERB	_	_	36	acl	_	_
41	dari	_	ADP	_	_	42	case	_	_
42	album	_	NOUN	_	_	40	nmod	_	_
43	-	_	PUNCT	_	_	42	punct	_	_
44	album	_	NOUN	_	_	42	mwe	_	_
45	solo	_	NOUN	_	_	42	compound	_	_
46	Franky	_	PROPN	_	_	45	name	_	PERSON
47	sebelumnya	_	ADJ	_	_	42	amod	_	_
48	maupun	_	CONJ	_	_	42	cc	_	_
49	album	_	NOUN	_	_	42	conj	_	_
50	-	_	PUNCT	_	_	49	punct	_	_
51	album	_	NOUN	_	_	49	mwe	_	_
52	Franky	_	PROPN	_	_	49	name	_	OTHER
53	&amp;	_	SYM	_	_	52	punct	_	OTHER
54	Jane	_	PROPN	_	_	53	name	_	OTHER
55	.	_	PUNCT	_	_	5	punct	_	_

```



or extraction with transformation

``
Bang Yong Guk berkomentar "..." -> Bang Yong Guk-memberikan-komentar
``

Some known problem: knowledge with unusual structure "Ada banyak penduduk Indonesia di Singapura", "Selain pintar, Einstein juga humoris"

* Reduce candidates generated from this sentence

```
1	Kapal	_	NOUN	_	_	3	nsubjpass	_	_
2	ini	_	DET	_	_	1	det	_	_
3	didesain	_	VERB	_	_	0	root	_	_
4	sebagai	_	ADP	_	_	5	case	_	_
5	kapal	_	NOUN	_	_	3	nmod	_	_
6	serang	_	NOUN	_	_	5	compund	_	_
7	berkecapatan	_	VERB	_	_	5	acl	_	_
8	tinggi	_	ADJ	_	_	7	amod	_	_
9	,	_	PUNCT	_	_	3	punct	_	_
10	untuk	_	ADP	_	_	11	case	_	_
11	mencapai	_	VERB	_	_	16	xcomp	_	_
12	itu	_	NOUN	_	_	11	dobj	_	_
13	maka	_	SCONJ	_	_	16	mark	_	_
14	badan	_	NOUN	_	_	16	nsubjpass	_	_
15	kapal	_	NOUN	_	_	14	compound	_	_
16	dibuat	_	VERB	_	_	3	parataxis	_	_
17	dari	_	ADP	_	_	18	case	_	_
18	Aluminium	_	PROPN	_	_	16	nmod	_	OTHER
19	sehingga	_	ADP	_	_	16	advmod	_	_
20	bisa	_	ADV	_	_	22	advmod	_	_
21	lebih	_	ADV	_	_	22	advmod	_	_
22	ringan	_	ADJ	_	_	19	amod	_	_
23	selain	_	ADP	_	_	24	case	_	_
24	itu	_	NOUN	_	_	31	nmod	_	_
25	untuk	_	ADP	_	_	26	case	_	_
26	mencapai	_	VERB	_	_	31	xcomp	_	_
27	kecepatan	_	NOUN	_	_	26	dobj	_	_
28	tinggi	_	ADJ	_	_	27	amod	_	_
29	kapal	_	NOUN	_	_	31	nsubjpass	_	_
30	ini	_	DET	_	_	29	det	_	_
31	dilengkapi	_	VERB	_	_	3	parataxis	_	_
32	dengan	_	ADP	_	_	33	case	_	_
33	mesin	_	NOUN	_	_	31	nmod	_	_
34	gas	_	NOUN	_	_	33	compound	_	_
35	turbin	_	NOUN	_	_	34	compound	_	_
36	General	_	PROPN	_	_	33	name	_	OTHER
37	Electric	_	PROPN	_	_	36	name	_	OTHER
38	LM	_	PROPN	_	_	37	name	_	OTHER
39	1500	_	NUM	_	_	38	nummod	_	OTHER
40	selain	_	ADP	_	_	42	case	_	_
41	2	_	NUM	_	_	42	nummod	_	QUANTITY
42	buah	_	NOUN	_	_	33	nmod	_	QUANTITY
43	mesin	_	NOUN	_	_	42	compound	_	_
44	diesel	_	NOUN	_	_	43	compound	_	_
45	untuk	_	ADP	_	_	46	case	_	_
46	kecepatan	_	NOUN	_	_	42	nmod	_	_
47	rendah	_	ADJ	_	_	46	amod	_	_
48	.	_	PUNCT	_	_	3	punct	_	_

1	Kebanyakan	_	DET	_	_	2	det	_	_
2	penduduknya	_	NOUN	_	_	3	nsubj	_	_
3	beragama	_	VERB	_	_	0	root	_	_
4	Katolik	_	PROPN	_	_	3	dobj	_	OTHER
5	Roma	_	PROPN	_	_	4	name	_	OTHER
6	,	_	PUNCT	_	_	3	punct	_	_
7	namun	_	SCONJ	_	_	8	mark	_	_
8	ada	_	VERB	_	_	3	advcl	_	_
9	pula	_	ADV	_	_	11	advmod	_	_
10	sedikit	_	ADV	_	_	11	advmod	_	_
11	orang	_	NOUN	_	_	8	dobj	_	_
12	Islam	_	PROPN	_	_	11	name	_	OTHER
13	di	_	ADP	_	_	14	case	_	_
14	situ	_	NOUN	_	_	11	nmod	_	_
15	.	_	PUNCT	_	_	3	punct	_	_
```

# Flatten/Expand Entity

* Use machine learning

#### Problematic samples:

```
0	(Sembungan)	terletak	di (kecamatan) Kejajar , kabupaten Wonosobo , Jawa Tengah , Indonesia	PROPN_nsubj_NOUN	VERB_acl_NOUN	NOUN_nmod_VERB	1
0	(Sembungan)	terletak	di (kabupaten) Wonosobo , Jawa Tengah , Indonesia	PROPN_nsubj_NOUN	VERB_acl_NOUN	NOUN_appos_NOUN	1
0	(Sembungan)	terletak	di (Jawa) Tengah , Indonesia	PROPN_nsubj_NOUN	VERB_acl_NOUN	PROPN_appos_NOUN	1
7	(Lagu) ini	ditampilkan	dalam (rilisan) EP ( Extended Play ) , Moshi Moshi Harajuku , dan album " Pamyu Pamyu Revolution "	PROPN_nsubjpass_VERB	VERB_root_	NOUN_nmod_NOUN	1
9	(Cikal) bakal Lembaga Pendidikan ini	dirintis	oleh beberapa (ulama) terdahulu di antaranya	NOUN_nsubjpass_VERB	VERB_root_	NOUN_nmod_VERB	1
35	(Konsekuensi) logis	diekspresikan	sebagai (hubungan)	NOUN_nsubjpass_VERB	VERB_root_	NOUN_nmod_NOUN	1
37	(Krisis) finansial Islandia 2008	adalah	sebagai (dampak)	PROPN_nsubj_NOUN	VERB_cop_NOUN	NOUN_nmod_NOUN
```
