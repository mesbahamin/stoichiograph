import speller
import unittest


class MatchingTest(unittest.TestCase):
    test_singles = ['B', 'e', 'c', 'a', 'u', 's', 'e']
    test_pairs = ['Be', 'ec', 'ca', 'au', 'se']
    symbols = speller.get_csv_data('elements.csv', 1)

    def test_match_singles(self):
        matches = speller.find_matches(self.test_singles, self.symbols)
        self.assertEqual(matches, ['b', 'c', 'u', 's'])

    def test_match_pairs(self):
        matches = speller.find_matches(self.test_pairs, self.symbols)
        self.assertEqual(matches, ['be', 'ca', 'au', 'se'])


class TokensTest(unittest.TestCase):
    test_word = "Osiris"

    def test_single_chars(self):
        tokens = speller.tokenize_sequence(self.test_word)
        self.assertEqual(tokens.single, ["O", "s", "i", "r", "i", "s"])

    def test_pair_chars(self):
        tokens = speller.tokenize_sequence(self.test_word)
        self.assertEqual(tokens.pair, ["Os", "si", "ir", "ri", "is"])


class FileTest(unittest.TestCase):
    file_name = "elements.csv"
    proper_data = ['H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne',
                   'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar', 'K', 'Ca',
                   'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn',
                   'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr', 'Rb', 'Sr', 'Y', 'Zr',
                   'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn',
                   'Sb', 'Te', 'I', 'Xe', 'Cs', 'Ba', 'La', 'Ce', 'Pr', 'Nd',
                   'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb',
                   'Lu', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg',
                   'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn', 'Fr', 'Ra', 'Ac', 'Th',
                   'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm',
                   'Md', 'No', 'Lr', 'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds',
                   'Rg', 'Uub', 'Uut', 'Uuq', 'Uup', 'Uuh', 'Uus', 'Uuo']

    def test_file_contains_proper_data(self):
        data = speller.get_csv_data(self.file_name, 1)
        self.assertEqual(data, self.proper_data)


if __name__ == '__main__':
    unittest.main(warnings='ignore')
