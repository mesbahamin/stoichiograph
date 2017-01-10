from itertools import chain, product
import logging

# TODO(amin): Profile and optimize
# TODO(amin): Add performance reporting to log
# TODO(amin): Use recursion to save time with long words that can't be spelled.
# TODO(amin): Convert symbol tuple to element name or atomic number tuple

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

ELEMENTS = (
    'H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne', 'Na', 'Mg', 'Al',
    'Si', 'P', 'S', 'Cl', 'Ar', 'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe',
    'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr', 'Rb', 'Sr', 'Y',
    'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb',
    'Te', 'I', 'Xe', 'Cs', 'Ba', 'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd',
    'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir',
    'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn', 'Fr', 'Ra', 'Ac',
    'Th', 'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm', 'Md', 'No',
    'Lr', 'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds', 'Rg', 'Cn', 'Nh', 'Fl',
    'Mc', 'Lv', 'Ts', 'Og'
)


# TODO(amin): Use optional caching/memoization to improve performance
# TODO(amin): Support appostrophies
# TODO(amin): Add option to require no repeated symbols
def elemental_spelling(word, symbols=ELEMENTS):
    """Given a word and a sequence of symbols (tokens),
    return a list of any possible ways to spell that word
    with those symbols.

    Example:
    >>> elemental_spelling('amputation')
    [('Am', 'Pu', 'Ta', 'Ti', 'O', 'N'), ('Am', 'P', 'U', 'Ta', 'Ti', 'O', 'N')]
    """
    log.info('Word: {}'.format(word))
    letter_groupings = _groupings(len(word))

    spellings = [_map_word(word, grouping) for grouping in letter_groupings]

    elemental_spellings = [
        tuple(token.capitalize() for token in spelling)
        for spelling in spellings
        # set operation: set of chars in spelling is subset of set of symbols
        if set(s.lower() for s in spelling) <= set(s.lower() for s in symbols)
    ]

    log.info('Spellings: {}'.format(elemental_spellings))

    return elemental_spellings


def _groupings(word_length, token_sizes=(1, 2)):
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

    log.debug('Groupings: {}'.format(groupings))

    return groupings


# TODO(amin): Handle failure cases (grouping doesn't add up to word length)
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

    log.debug('Grouping: {}. Mapped word: {}'.format(grouping, mapped))

    return tuple(mapped)


if __name__ == '__main__':
    test_word = 'Mockery'
    print('{}:\n{}'.format(test_word, elemental_spelling(test_word)))
