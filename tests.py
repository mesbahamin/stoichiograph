import elemental_speller as es
import pytest

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


def test_verify_data():
    assert es.ELEMENTS == ELEMENTS


def test_groupings():
    assert es._groupings(4, token_sizes=()) == ()

    expected = ((2, 2), (1, 1, 2), (1, 2, 1), (2, 1, 1), (1, 1, 1, 1))
    assert es._groupings(4, token_sizes=(1, 2)) == expected

    expected = (
        (1, 3), (2, 2), (3, 1), (1, 1, 2), (1, 2, 1), (2, 1, 1), (1, 1, 1, 1)
    )
    assert es._groupings(4, token_sizes=(1, 2, 3)) == expected


def test_map_word():
    assert es._map_word('because', (1, 2, 1, 1, 2)) == ('b', 'ec', 'a', 'u', 'se')
    assert es._map_word('osiris', (1, 3, 2)) == ('o', 'sir', 'is')


def test_elemental_spelling():
    assert es.elemental_spelling('amputation') == [
        ('Am', 'Pu', 'Ta', 'Ti', 'O', 'N'),
        ('Am', 'P', 'U', 'Ta', 'Ti', 'O', 'N')
    ]
