import pytest
import elemental_speller as es

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


def test_verify_data():
    assert es.ELEMENTS == ELEMENTS


def test_groupings():
    assert es.generate_groupings(4, batch_sizes=()) == ()

    assert es.generate_groupings(4, batch_sizes=(1, 2)) == (
        (2, 2), (1, 1, 2), (1, 2, 1), (2, 1, 1), (1, 1, 1, 1)
    )

    assert es.generate_groupings(4, batch_sizes=(1, 2, 3)) == (
        (1, 3), (2, 2), (3, 1), (1, 1, 2), (1, 2, 1), (2, 1, 1), (1, 1, 1, 1)
    )


def test_map_word():
    assert es.map_word('because', (1, 2, 1, 1, 2)) == ('b', 'ec', 'a', 'u', 'se')
    assert es.map_word('osiris', (1, 3, 2)) == ('o', 'sir', 'is')

    with pytest.raises(ValueError):
        es.map_word('toolong', (2, 1))
        es.map_word('short', (2, 2, 2))


def test_elemental_spelling():
    assert es.spell('amputation') == [
        ('Am', 'Pu', 'Ta', 'Ti', 'O', 'N'),
        ('Am', 'P', 'U', 'Ta', 'Ti', 'O', 'N')
    ]
