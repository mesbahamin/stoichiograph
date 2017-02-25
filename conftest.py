from collections import defaultdict
import pytest
from speller import Graph, Node


@pytest.fixture()
def test_graph():
    """Return a `speller.Graph` object of the word 'because'."""
    test_graph = Graph()

    test_graph._parents_of = defaultdict(
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

    test_graph._children_of = defaultdict(
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

    return test_graph
