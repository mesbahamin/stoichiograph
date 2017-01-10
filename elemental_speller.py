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
def spell(word, symbols=ELEMENTS):
    """Return a list of any possible ways to spell a word
    with a given set of symbols.

    Example:
    >>> spell('amputation')
    [('Am', 'Pu', 'Ta', 'Ti', 'O', 'N'), ('Am', 'P', 'U', 'Ta', 'Ti', 'O', 'N')]
    """
    log.info('Word: {}'.format(word))
    groupings = generate_groupings(len(word))

    spellings = [map_word(word, grouping) for grouping in groupings]

    elemental_spellings = [
        tuple(token.capitalize() for token in spelling)
        for spelling in spellings
        # set operation: set of chars in spelling is subset of set of symbols
        if set(s.lower() for s in spelling) <= set(s.lower() for s in symbols)
    ]

    log.info('Spellings: {}'.format(elemental_spellings))

    return elemental_spellings


def generate_groupings(word_length, group_sizes=(1, 2)):
    """Return all groupings for a word of a given length.

    A grouping is a tuple representing the distribution of
    characters in a word. By default, characters can be in
    groups of 1 or 2.

    Example:
    >>> generate_groupings(4)
    ((2, 2), (1, 1, 2), (1, 2, 1), (2, 1, 1), (1, 1, 1, 1))
    """
    cartesian_products = (
        product(group_sizes, repeat=r)
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
def map_word(word, grouping):
    """Return a word mapped to a grouping.

    Example:
    >>> map_word('because', (1, 2, 1, 1, 2))
    ('b', 'ec', 'a', 'u', 'se')
    """
    chars = (c for c in word)

    mapped = []
    for group_size in grouping:
        group = ""
        for _ in range(group_size):
            group += next(chars)
        mapped.append(group)

    log.debug('Grouping: {}. Mapped word: {}'.format(grouping, mapped))

    return tuple(mapped)


if __name__ == '__main__':
    test_word = 'Mockery'
    print('{}:\n{}'.format(test_word, spell(test_word)))
