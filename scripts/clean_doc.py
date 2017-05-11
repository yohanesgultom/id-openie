import argparse
import sys
import re


def clean_doc(reader, writer):
    sentences = []
    for line in reader:
        line = line.strip()
        if not line:
            continue
        if len(line.split()) < 2:
            continue
        if re.match(r'^BAB\s*(I|II|III|IV|V|VI|VII|VIII).*', line):
            continue
        if re.match(r'^[A-Z]\.\s*.*', line):
            continue
        # remove numbering
        line = re.sub(r'\s*\(\d\)\s*', '', line, flags=re.IGNORECASE)
        # merge lines
        clauses = [s.strip() for s in line.split('.') if s]
        if len(clauses) <= 1:
            sentences.append(clauses[0])
            if line[-1] == '.':
                writer.write(' '.join(sentences).strip() + '.\n')
                sentences = []
        else:
            while clauses:
                clause = clauses.pop(0).strip()
                if clause:
                    if clauses:
                        sentences += [clause + '.']
                        if len(clause.split()) >= 3:
                            writer.write(' '.join(sentences).strip() + '\n')
                            sentences = []
                    else:  # last line
                        if line[-1] == '.':
                            writer.write(clause + '.\n')
                        else:
                            sentences += [clause]

    # just in case last line does not end with dot
    if sentences:
        writer.write(' '.join(sentences).strip() + '.\n')
        sentences = []


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Clean up text document.')
    parser.add_argument('input_file', help='Input text file')
    parser.add_argument('-o', '--output_file', help='Output text file', default='cleaned.txt')
    parser.add_argument('-d', '--debug', help='Debug by printing to stdout instead of file', action='store_true')
    args = parser.parse_args()
    reader = open(args.input_file, 'rb')
    writer = sys.stdout if args.debug else open(args.output_file, 'wb')
    clean_doc(reader, writer)
    reader.close()
    writer.close()
