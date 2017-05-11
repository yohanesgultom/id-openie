import sys
from extract_triples import extract
from sklearn.externals import joblib

conllu_file = 'plain.txt.conllu'
model_file = 'triples-classifier-model.pkl'
classifier = joblib.load(model_file)
count = extract(conllu_file, classifier, sys.stdout, format='json')
print('{} triple(s) extracted'.format(count))
