# TODO:
# - eliminate unnecessary functions
# - simplify
# - use consistent terminology
import csv
from collections import namedtuple
from itertools import chain, product
from pprint import pprint

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


def get_csv_data(file_name, column, header=True):
    """Return in a list all data from a given column of a .csv file"""

    data = []

    with open(file_name) as infile:
        csv_reader = csv.reader(infile, skipinitialspace=True, delimiter=',')
        if header:
            next(csv_reader, None)  # skip header row
        for row in csv_reader:
            data.append(row[column])

    return data


def tokenize_sequence(sequence):
    """Return a list each of all single and double character tokens."""

    Tokens = namedtuple('Tokens', (['singles', 'doubles']))

    singles = tuple(sequence[i] for i in range(0, len(sequence)))
    doubles = tuple(sequence[i:i+2] for i in range(0, len(sequence) - 1))

    return Tokens(singles, doubles)


def find_matches(sequence, symbols):
    """Return a dictionary of symbols and indices for all
    symbols that match an item in the given sequence.
    """

    return {
        symbol: index
        for character in sequence
        for index, symbol in enumerate(symbols)
        if symbol.lower() == character.lower()
    }


def groupings(word, token_sizes=(1, 2)):
    """Return a tuple of all permutations of possible character
    grouping arrangements of a word.

    token_sizes defines the possible sizes of character groups,
    and by default allows only singles and pairs.
    """

    cartesian_products = (
        product(token_sizes, repeat=r)
        for r in range(1, len(word) + 1)
    )

    # include only groupings that represent the correct number of chars
    groupings = tuple(
        grouping
        for grouping in chain.from_iterable(cartesian_products)
        if sum(grouping) == len(word)
    )

    return groupings


def map_word(word, grouping):
    """Given a word and a grouping, map the characters of the word
    to match the distribution defined in the grouping.

    example:
    >>> map_word('because', (1, 2, 1, 1, 2))
    ['b', 'ec', 'a', 'u', 'se']
    """

    word_chars = (c for c in word)

    mapped = []
    for char_group_size in grouping:
        char_group = ""
        for _ in range(char_group_size):
            char_group += next(word_chars)
        mapped.append(char_group)

    return tuple(mapped)


if __name__ == '__main__':
    symbols = get_csv_data('elements.csv', 1)

    test_word = 'Osiris'

    tokens = tokenize_sequence(test_word)

    single_matches = find_matches(tokens.singles, symbols)
    pair_matches = find_matches(tokens.doubles, symbols)

    letter_groupings = groupings(test_word)

    spellings = [map_word(test_word, g) for g in letter_groupings]

    elemental_spellings = [
        [l.capitalize() for l in spelling]
        for spelling in spellings
        if set(c.lower() for c in spelling) <= set(s.lower() for s in symbols)
    ]

    pprint(tokens)
    pprint(single_matches)
    pprint(pair_matches)
    pprint(list(zip(letter_groupings, spellings)))
    pprint(elemental_spellings)
