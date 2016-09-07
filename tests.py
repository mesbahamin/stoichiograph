import speller
import unittest

# TODO: change to py.test syntax

ELEMENTS = (
    'Ac', 'Ag', 'Al', 'Am', 'Ar', 'As', 'At', 'Au', 'B', 'Ba', 'Be', 'Bh',
    'Bi', 'Bk', 'Br', 'C', 'Ca', 'Cd', 'Ce', 'Cf', 'Cl', 'Cm', 'Co', 'Cr',
    'Cs', 'Cu', 'Db', 'Ds', 'Dy', 'Er', 'Es', 'Eu', 'F', 'Fe', 'Fm', 'Fr',
    'Ga', 'Gd', 'Ge', 'H', 'He', 'Hf', 'Hg', 'Ho', 'Hs', 'I', 'In', 'Ir',
    'K', 'Kr', 'La', 'Li', 'Lr', 'Lu', 'Md', 'Mg', 'Mn', 'Mo', 'Mt', 'N',
    'Na', 'Nb', 'Nd', 'Ne', 'Ni', 'No', 'Np', 'O', 'Os', 'P', 'Pa', 'Pb',
    'Pd', 'Pm', 'Po', 'Pr', 'Pt', 'Pu', 'Ra', 'Rb', 'Re', 'Rf', 'Rg', 'Rh',
    'Rn', 'Ru', 'S', 'Sb', 'Sc', 'Se', 'Sg', 'Si', 'Sm', 'Sn', 'Sr', 'Ta',
    'Tb', 'Tc', 'Te', 'Th', 'Ti', 'Tl', 'Tm', 'U', 'Uub', 'Uuh', 'Uuo',
    'Uup', 'Uuq', 'Uus', 'Uut', 'V', 'W', 'Xe', 'Y', 'Yb', 'Zn', 'Zr'
)

class MatchingTest(unittest.TestCase):
    test_singles = ['B', 'e', 'c', 'a', 'u', 's', 'e']
    test_pairs = ['Be', 'ec', 'ca', 'au', 'se']

    def test_match_singles(self):
        matches = speller.find_matches(self.test_singles, ELEMENTS)
        self.assertEqual(
            matches,
            {'S': 86, 'B': 8, 'U': 103, 'C': 15}
        )

    def test_match_pairs(self):
        matches = speller.find_matches(self.test_pairs, ELEMENTS)
        self.assertEqual(
            matches,
            {'Au': 7, 'Be': 10, 'Ca': 16, 'Se': 89}
        )


class TokensTest(unittest.TestCase):
    test_word = "Osiris"

    def test_single_chars(self):
        tokens = speller.tokenize_sequence(self.test_word)
        self.assertEqual(tokens.singles, ("O", "s", "i", "r", "i", "s"))

    def test_pair_chars(self):
        tokens = speller.tokenize_sequence(self.test_word)
        self.assertEqual(tokens.doubles, ("Os", "si", "ir", "ri", "is"))


class GroupingTest(unittest.TestCase):
    word = "that"

    def test_singles_and_pairs(self):
        expected_maps = ((2, 2), (1, 1, 2), (1, 2, 1), (2, 1, 1), (1, 1, 1, 1))
        group_maps = speller.groupings(self.word)
        self.assertEqual(group_maps, expected_maps)


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
