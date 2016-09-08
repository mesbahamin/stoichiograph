# TODO: add logging

from collections import namedtuple
from itertools import chain, product

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


def elemental_spelling(word, symbols=ELEMENTS):
    """Given a word and a sequence of symbols (tokens),
    return a list of any possible ways to spell that word
    with those symbols.

    Example:
    >>> elemental_spelling('amputation')
    [(('Am', 'Pu', 'Ta', 'Ti', 'O', 'N'), ('Am', 'P', 'U', 'Ta', 'Ti', 'O', 'N')]
    """
    letter_groupings = _groupings(len(word))

    spellings = [_map_word(word, grouping) for grouping in letter_groupings]

    elemental_spellings = [
        tuple(token.capitalize() for token in spelling)
        for spelling in spellings
        # set operation: set of chars in spelling is subset of set of symbols
        if set(s.lower() for s in spelling) <= set(s.lower() for s in symbols)
    ]

    return elemental_spellings


def _groupings(word_length, token_sizes=(1, 2, 3)):
    """Return a tuple of all character groupings for a word
    of a given length.

    A character grouping is a tuple representing the distribution
    of characters in a tokenized word.

    The word 'canary', if mapped to the grouping (1, 3, 2), would
    be broken down into ['c', 'ana', 'ry'].

    token_sizes defines the possible sizes of character groups,
    and by default allows only singles, pairs, and triplets.

    Example:
    >>> _groupings(4, token_sizes=(1, 2))
    ((2, 2), (1, 1, 2), (1, 2, 1), (2, 1, 1), (1, 1, 1, 1))
    """

    cartesian_products = (
        product(token_sizes, repeat=r)
        for r in range(1, word_length + 1)
    )

    # include only groupings that represent the correct number of chars
    groupings = tuple(
        grouping
        for grouping in chain.from_iterable(cartesian_products)
        if sum(grouping) == word_length
    )

    return groupings


def _map_word(word, grouping):
    """Return a tuple of tokens: word mapped to a grouping.

    Example:
    >>> _map_word('because', (1, 2, 1, 1, 2))
    ('b', 'ec', 'a', 'u', 'se')
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
    test_word = 'Mockery'
    print('{}:\n{}'.format(test_word, elemental_spelling(test_word)))
