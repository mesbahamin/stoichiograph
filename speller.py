from collections import defaultdict, namedtuple
from functools import lru_cache
import logging

# TODO(amin): Convert symbol tuple to element name or atomic number tuple

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

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

    log.debug('Using graph speller')
    g = Graph()
    build_graph(word, g)

    spellings = list()
    for first in g.firsts():
        for last in g.lasts():
            for path in find_all_paths(g._children_of, first, last):
                spellings.append(tuple(node.value for node in path))

    elemental_spellings = sorted([
        tuple(token.capitalize() for token in spelling)
        for spelling in spellings
    ], reverse=True)

    log.info('Spellings: {}'.format(elemental_spellings))

    return elemental_spellings


# A single node of the graph.
Node = namedtuple('Node', ['value', 'position'])


class Graph():
    """A directed acyclic graph that stores all possible
    elemental spellings of a word.
    """
    def __init__(self):
        self._parents_of = defaultdict(set)
        self._children_of = defaultdict(set)

    def firsts(self):
        """Return nodes with no parents."""
        return self._children_of[None]

    def lasts(self):
        """Return nodes with no children."""
        return self._parents_of[None]

    def add_edge(self, parent, child):
        """Add a parent-child relatonship to the graph.
        None is ok as a key, but not a value.
        """
        if parent is not None:
            self._parents_of[child].add(parent)
        if child is not None:
            self._children_of[parent].add(child)

    def edges(self):
        """Return a list of all parent-child relationships."""
        return [
            (parent, child)
            for parent in self._children_of
            for child in self._children_of[parent]
        ]

    def export(self):
        """Print a string to stdout that can be interpreted by
        Graphviz.
        """
        print('digraph G {')
        for (parent, child) in self.edges():
            a = None if parent is None else parent.value
            b = None if child is None else child.value
            print('\t{} -> {}'.format(a, b))
        print('}')


def find_all_paths(graph, start, end, path=[]):
    """Return a list of all paths through the graph from start
    to end.
    Based on https://www.python.org/doc/essays/graphs/
    """
    path = path + [start]
    if start == end:
        return [path]
    if start not in graph.keys():
        return []
    paths = []
    for node in graph[start]:
        if node not in path:
            newpaths = find_all_paths(graph, node, end, path)
            for newpath in newpaths:
                paths.append(tuple(newpath))
    return paths


def build_graph(word, graph, symbols=ELEMENTS):
    """Given a word and a graph, recursively find all single and
    double-character tokens in the word and add them to the graph.
    """

    def segments(word, position=0, previous_root=None):
        if word == '':
            graph.add_edge(previous_root, None)
            return

        single_root = Node(word[0], position)
        if single_root.value.capitalize() in symbols:
            graph.add_edge(previous_root, single_root)

            if word not in processed:
                segments(word[1:], position + 1, previous_root=single_root)

        if len(word) >= 2:
            double_root = Node(word[0:2], position)
            if double_root.value.capitalize() in symbols:
                graph.add_edge(previous_root, double_root)

                if word not in processed:
                    segments(word[2:], position + 2, previous_root=double_root)
        processed.add(word)

    processed = set()
    segments(word)


if __name__ == '__main__':
    test_word = 'Mockery'
    print('{}:\n{}'.format(test_word, spell(test_word)))
