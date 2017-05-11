import sys
from clean_doc import clean_doc

case_1 = '''Penggunaan sumber daya alam harus selaras, serasi, dan seimbang dengan
fungsi lingkungan hidup. Sebagai konsekuensinya, kebijakan, rencana, dan/atau
program pembangunan harus dijiwai oleh kewajiban melakukan pelestarian
lingkungan hidup.
'''

expected_1 = '''Penggunaan sumber daya alam harus selaras, serasi, dan seimbang dengan fungsi lingkungan hidup.
Sebagai konsekuensinya, kebijakan, rencana, dan/atau program pembangunan harus dijiwai oleh kewajiban melakukan pelestarian lingkungan hidup.
'''


def test_clean_doc_1(capsys):
    reader = case_1.split('\n')
    writer = sys.stdout
    clean_doc(reader, writer)
    out, err = capsys.readouterr()
    assert out == expected_1
