# Indonesian Knowledge Extractor

> This is a work in progress and still focusing on proven of concept instead of accuracy

Indonesian knowledge extractor using Stanford NLP Open IE [1].

Using Indonesian lemmatizer annotator which is an modified port from https://github.com/davidchristiandy/lemmatizer [2].

**Build**

To build from source:

* Install [Oracle JRE/JDK 8](http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html), [Gradle](https://gradle.org/) and [Python 2.7]()
* Download and clone this repo
* Run build command from repo directory

```
gradle clean build
```

**Installation**

To run the distribution without building:

* Install [Oracle JRE/JDK 8](http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html) and [Python 2.7]()
* Get the distribution in `build/distributions` (`.zip` or `.tar`) and extract it
* Install Python dependencies eg. `pip install -r requirements.txt` (Java dependencies are already included inside `lib`)

**Usage**

Command format:

```
python extract_triples.py [-h] [-o OUTPUT_FILE] input_file
 
positional arguments:
 
    input_file: Input file containing 1 (one) Indonesian sentence per line
 
optional arguments:
 
    -o, --output_file: Output file containing triples
```

Example:

```
python extract_triples.py plain.txt -o triples.tsv 
```

**References**

1. Angeli, G., Premkumar, M.J. and Manning, C.D., 2015, July. Leveraging linguistic structure for open domain information extraction. In Proceedings of the 53rd Annual Meeting of the Association for Computational Linguistics (ACL 2015).
2. Suhartono, D., 2014. Lemmatization Technique in Bahasa: Indonesian. Journal of Software, 9(5), p.1203.