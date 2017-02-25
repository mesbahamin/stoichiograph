from collections import defaultdict
import speller
from speller import Node

ELEMENTS = {
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
}


def test_verify_data():
    """Assert that the set of elements in `speller.py` matches this
    canonical set.
    """
    assert speller.ELEMENTS == ELEMENTS


def test_elemental_spelling():
    """Assert that we get the expected results when spelling various
    inputs.
    """
    assert speller.spell('amputation') == [
        ('Am', 'Pu', 'Ta', 'Ti', 'O', 'N'),
        ('Am', 'P', 'U', 'Ta', 'Ti', 'O', 'N')
    ]
    assert speller.spell('') == []
    assert speller.spell('o') == [('O',)]


def test_find_all_paths():
    """Make simple graph with some branches, and assert that we find all
    the paths from the first node to the last.
    """
    parents_to_children = {
        'a': {'b'},
        'b': {'c'},
        'c': {'d'},
        'd': {'e', 'y', 'z'},
        'e': {'f', 'x'},
        'f': {'g', 'x'},
        'g': {'h'},
        'h': {'i'},
        'x': {'y'},
        'y': {'z'},
    }

    assert set(speller.find_all_paths(parents_to_children, 'a', 'z')) == set([
        ('a', 'b', 'c', 'd', 'z'),
        ('a', 'b', 'c', 'd', 'y', 'z'),
        ('a', 'b', 'c', 'd', 'e', 'x', 'y', 'z'),
        ('a', 'b', 'c', 'd', 'e', 'f', 'x', 'y', 'z'),
    ])


def test_build_spelling_graph():
    """Make a `speller.Graph` object, then build it with a word and
    assert that it contains the proper node relationships.
    """
    g = speller.Graph()
    speller.build_spelling_graph('because', g)

    assert g._parents_of == defaultdict(
        set,
        {
            Node(value='c', position=2): {Node(value='be', position=0)},
            Node(value='au', position=3): {Node(value='c', position=2)},
            Node(value='s', position=5): {
                Node(value='au', position=3),
                Node(value='u', position=4)
            },
            Node(value='se', position=5): {
                Node(value='au', position=3),
                Node(value='u', position=4)
            },
            None: {Node(value='se', position=5)},
            Node(value='ca', position=2): {Node(value='be', position=0)},
            Node(value='u', position=4): {Node(value='ca', position=2)}
        }
    )

    assert g._children_of == defaultdict(
        set,
        {
            None: {Node(value='be', position=0), Node(value='b', position=0)},
            Node(value='be', position=0): {
                Node(value='ca', position=2),
                Node(value='c', position=2)
            },
            Node(value='c', position=2): {Node(value='au', position=3)},
            Node(value='au', position=3): {
                Node(value='se', position=5),
                Node(value='s', position=5)
            },
            Node(value='ca', position=2): {Node(value='u', position=4)},
            Node(value='u', position=4): {
                Node(value='se', position=5),
                Node(value='s', position=5)
            }
        }
    )


class TestGraph:
    """Tests for the methods of the `speller.Graph` class."""

    def test_firsts(self, test_graph):
        """Assert that the graph properly identifies its first nodes."""
        assert test_graph.firsts() == {Node('be', 0), Node('b', 0)}

    def test_lasts(self, test_graph):
        """Assert that the graph properly identifies its last nodes."""
        assert test_graph.lasts() == {Node('se', 5)}

    def test_add_edge(self, test_graph):
        """Add an edge to the graph."""
        parent = Node('te', 0)
        child = Node('st', 2)
        test_graph.add_edge(parent, child)
        assert test_graph._children_of[parent] == {child}
        assert test_graph._parents_of[child] == {parent}

    def test_add_edge_with_no_parent(self, test_graph):
        """Add an edge with no parent to the graph. Assert that 'None'
        isn't added to `_parents_of[child]`.
        """
        parent = None
        child = Node('a', 0)
        test_graph.add_edge(parent, child)
        assert child in test_graph._children_of[parent]
        assert None not in test_graph._parents_of[child]

    def test_add_edge_with_no_child(self, test_graph):
        """Add an edge with no child to the graph. Assert that `None`
        isn't added to `_children_of[parent]`.
        """
        parent = Node('z', 25)
        child = None
        test_graph.add_edge(parent, child)
        assert None not in test_graph._children_of[parent]
        assert parent in test_graph._parents_of[child]

    def test_nodes(self, test_graph):
        """Assert that the graph properly lists its nodes."""
        assert set(test_graph.nodes(connected_only=True)) == set([
            Node(value='be', position=0),
            Node(value='c', position=2),
            Node(value='ca', position=2),
            Node(value='au', position=3),
            Node(value='u', position=4),
            Node(value='s', position=5),
            Node(value='se', position=5),
        ])
        assert set(test_graph.nodes(connected_only=False)) == set([
            Node(value='b', position=0),
            Node(value='be', position=0),
            Node(value='c', position=2),
            Node(value='ca', position=2),
            Node(value='au', position=3),
            Node(value='u', position=4),
            Node(value='s', position=5),
            Node(value='se', position=5),
        ])

    def test_edges(self, test_graph):
        """Assert that the graph properly lists its edges."""
        assert set(test_graph.edges()) == set([
            (None, Node(value='b', position=0)),
            (None, Node(value='be', position=0)),
            (Node(value='be', position=0), Node(value='c', position=2)),
            (Node(value='be', position=0), Node(value='ca', position=2)),
            (Node(value='c', position=2), Node(value='au', position=3)),
            (Node(value='au', position=3), Node(value='s', position=5)),
            (Node(value='au', position=3), Node(value='se', position=5)),
            (Node(value='ca', position=2), Node(value='u', position=4)),
            (Node(value='u', position=4), Node(value='s', position=5)),
            (Node(value='u', position=4), Node(value='se', position=5))
        ])

    def test_export(self, test_graph):
        """Assert that the graph exports the proper dot code."""
        assert test_graph.export() == (
"""digraph G {
	graph [rankdir=LR];
	node [width=0.75 shape=circle];
	"Node(value='au', position=3)" -> "Node(value='s', position=5)";
	"Node(value='au', position=3)" -> "Node(value='se', position=5)";
	"Node(value='be', position=0)" -> "Node(value='c', position=2)";
	"Node(value='be', position=0)" -> "Node(value='ca', position=2)";
	"Node(value='c', position=2)" -> "Node(value='au', position=3)";
	"Node(value='ca', position=2)" -> "Node(value='u', position=4)";
	"Node(value='u', position=4)" -> "Node(value='s', position=5)";
	"Node(value='u', position=4)" -> "Node(value='se', position=5)";
	"Node(value='au', position=3)" [label="Au"];
	"Node(value='be', position=0)" [label="Be"];
	"Node(value='c', position=2)" [label="C"];
	"Node(value='ca', position=2)" [label="Ca"];
	"Node(value='s', position=5)" [label="S"];
	"Node(value='se', position=5)" [label="Se"];
	"Node(value='u', position=4)" [label="U"];
}"""
        )
