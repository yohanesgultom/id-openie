'''
Convert Named-Entity tagged file (Open NLP format) to Stanford NLP format (token-based)
@Author yohanes.gultom@gmail

Tagged file example (2 sentences):
"Internal DPD Sulsel mudah-mudahan dalam waktu dekat ada keputusan.  Sudah ada keputusan kita serahkan ke DPP dan Rabu ini kita akan rapat harian soal itu," kata <PERSON>Sudding</PERSON> kepada Tribunnews.com, <TIME>Senin (30/1/2012)</TIME>.
Menurut <PERSON>Sudding</PERSON>, DPP Hanura pada prinsipnya memberikan kesempatan dan ruang sama bagi pengurus DPD dan DPC Hanura Sulsel untuk menyampaikan aspirasinya.
"Dan diberikan kesempatan melakukan verfikasi akar msalah yang terjadi di DPD Hanura Sulsel," kata dia.
'''

import sys
import re

SINGLE_PATTERN = re.compile(r'^([^<>]*)<(\w+)>([^<]*)</(\w+)>([^<>]*)$', re.I)
START_PATTERN = re.compile(r'^([^<>]*)<(\w+)>([^<]*)$', re.I)
END_PATTERN = re.compile(r'^([^<>]*)</(\w+)>([^<]*)$', re.I)
EOS_PATTERN = re.compile(r'^([^<>]*)\.$', re.I)
NON_ENTITY_TYPE = 'O'

infile = sys.argv[1]
outfile = sys.argv[2]
cur_type = NON_ENTITY_TYPE
with open(infile, 'rb') as f, open(outfile, 'w') as out:
    for line in f:
        for token in line.strip().split(' '):
            token = token.strip()
            if not token:
                continue

            match = re.match(SINGLE_PATTERN, token)
            if match:
                if match.group(1):
                    out.write(match.group(1) + '\t' + NON_ENTITY_TYPE + '\n')
                out.write(match.group(3) + '\t' + match.group(2) + '\n')
                if match.group(2) != match.group(4):
                    raise ValueError('Invalid tag pair: {} and {}'.format(match.group(2), match.group(4)))
                if match.group(5):
                    out.write(match.group(5) + '\t' + NON_ENTITY_TYPE + '\n')
                continue

            match = re.match(START_PATTERN, token)
            if match:
                if match.group(1):
                    out.write(match.group(1) + '\t' + NON_ENTITY_TYPE + '\n')
                cur_type = match.group(2)
                out.write(match.group(3) + '\t' + cur_type + '\n')
                continue

            match = re.match(END_PATTERN, token)
            if match:
                out.write(match.group(1) + '\t' + cur_type + '\n')
                if match.group(2) != cur_type:
                    raise ValueError('Invalid tag pair: {} and {}'.format(cur_type, match.group(2)))
                cur_type = NON_ENTITY_TYPE
                if match.group(3):
                    out.write(match.group(3) + '\t' + NON_ENTITY_TYPE + '\n')
                continue

            match = re.match(EOS_PATTERN, token)
            if match:
                out.write(match.group(1) + '\t' + cur_type + '\n')
                out.write('.' + '\t' + cur_type + '\n')
                out.write('\n')
                continue

            out.write(token + '\t' + cur_type + '\n')
