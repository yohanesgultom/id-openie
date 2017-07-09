# Indonesian Open Domain Information Extractor

> This is a work in progress and still focusing on proven of concept instead of precision and recall

Indonesian open domain information extractor using Stanford NLP pipeline, heuristics triples candidate generator, heuristics token expander and Random Forest triple selector.

Input example:

```
"Sembungan adalah sebuah desa yang terletak di kecamatan Kejajar, kabupaten Wonosobo, Jawa Tengah, Indonesia."
```

Expected output:

```
"Sembungan" "adalah"  "desa"
"Sembungan" "terletak di" "kecamatan Kejajar"
```

**Build**

To build from source:

* Install build dependencies:
  * [Oracle JRE/JDK 8](http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html)
  * [Gradle](https://gradle.org/)
  * [Python 2.7](https://www.python.org/)
  * [Pip](https://pip.pypa.io)
  * [Tkinter](https://wiki.python.org/moin/TkInter) (or `python-tk` in Ubuntu) to display comparison charts
* Download and clone this repo
* Install Python dependencies: `pip install -r scripts/requirements.txt`
* Run build command from repo directory: `gradle clean build`
* Get distribution `.tar` or `.zip` from `build/distribution`
* Extract distribution to your choice of installation directory

**Usage**

Command format:

```
usage: extract_triples.py [-h] [-m MODEL_FILE] [-s SCALER_FILE]
                          [-o OUTPUT_FILE] [-f {json,tsv}]
                          input_file

Extract triples from Indonesian text

positional arguments:
  input_file            Input file containing 1 (one) Indonesian sentence per
                        line

optional arguments:
  -h, --help            show this help message and exit
  -m MODEL_FILE, --model_file MODEL_FILE
                        Triples classifier model file
  -s SCALER_FILE, --scaler_file SCALER_FILE
                        Triples classifier scaler file
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
                        Output file containing triples
  -f {json,tsv}, --output_format {json,tsv}
                        Output file format
```

Example:

```
python extract_triples.py -o plain.triples.json plain.txt
python extract_triples.py -o plain.triples.json -f json plain.txt
python extract_triples.py -o plain.triples.tsv -f tsv plain.txt
```

**Datasets**

List of Indonesian NLP datasets collected from various sources:

* POS tagging (source: https://github.com/UniversalDependencies/UD_Indonesian)

  * `data/tagger-id.universal.train`
  * `data/tagger-id.universal.test`

* NER (source: Faculty of Computer Science, UI & https://github.com/yusufsyaifudin/indonesia-ner)

  * `data/ner-id-1.train`
  * `data/ner-id-1.test`
  * `data/ner-id-2.train`
  * `data/ner-id-2.test`

* Dependency parsing (source: https://github.com/UniversalDependencies/UD_Indonesian)

  * `data/parser-id.conllu.train`
  * `data/parser-id.conllu.dev`
  * `data/parser-id.conllu.test`

* Triples selection (manually annotated):

  * `data/triple-selector.dataset.csv` (human readable)
  * `data/triple-selector.train.csv` (vectorized)

**Models**

* Stanford NLP POS tagger: `src/main/resources/tagger-id.universal.model`

* Stanford NLP NER `src/main/resources/ner-id.model.ser.gz`

* Stanford NLP dependency parser: `src/main/resources/parser-id.conllu.model.gz`

* Triple selector model (Scikit-Learn Standard Scaler and Random Forest):
  * `scripts/triples-classifier-scaler.pkl`
  * `scripts/triples-classifier-model.pkl`

**References**

1. Banko, M., Cafarella, M.J., Soderland, S., Broadhead, M. and Etzioni, O., 2007, January. Open Information Extraction from the Web. In IJCAI (Vol. 7, pp. 2670-2676).
1. Angeli, G., Premkumar, M.J. and Manning, C.D., 2015, July. Leveraging linguistic structure for open domain information extraction. In Proceedings of the 53rd Annual Meeting of the Association for Computational Linguistics (ACL 2015).
1. Suhartono, D., 2014. Lemmatization Technique in Bahasa: Indonesian. Journal of Software, 9(5), p.1203.

**Citation**

BibTex format:
```
@mastersthesis{gultom2017thesis,
	author={Yohanes {Gultom}},
	title={Automatic Open Domain Information Extraction from Indonesian Text},
	school={Universitas Indonesia},
	year={2017},
}
```
