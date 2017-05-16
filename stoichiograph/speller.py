from collections import defaultdict, namedtuple
from io import StringIO
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
    """Return a list of any possible ways to spell a word with a given
    set of symbols.

    Example:
    >>> spell('amputation')
    [('Am', 'Pu', 'Ta', 'Ti', 'O', 'N'), ('Am', 'P', 'U', 'Ta', 'Ti', 'O', 'N')]
    """
    log.info('Word: {}'.format(word))

    g = Graph()
    build_spelling_graph(word, g)

    elemental_spellings = sorted(
        [
            tuple(node.value.capitalize() for node in path)
            # There will only ever be at most 2 firsts and 2 lasts.
            for first in g.firsts()
            for last in g.lasts()
            for path in find_all_paths(g._children_of, first, last)
        ],
        reverse=True
    )

    log.info('Spellings: {}'.format(elemental_spellings))

    return elemental_spellings


class Graph():
    """A directed acyclic graph that stores all possible elemental
    spellings of a word.
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
        """Add a parent-child relatonship to the graph. None is ok as a
        key, but not a value.
        """
        log.debug('add_edge({}, {})'.format(parent, child))
        if parent is not None:
            self._parents_of[child].add(parent)
        if child is not None:
            self._children_of[parent].add(child)

    def nodes(self, connected_only=True):
        """Return a list of all nodes."""
        if connected_only:
            return set(
                node for node in
                set(self._children_of.keys()) | set(self._parents_of.keys())
                if node is not None
            )
        else:
            return set(
                node for node in
                set(self._children_of.keys())
                | set(self._parents_of.keys())
                | set(v for s in self._children_of.values() for v in s)
                | set(v for s in self._parents_of.values() for v in s)
                if node is not None
            )

    def edges(self):
        """Return a list of all parent-child relationships."""
        return [
            (parent, child)
            for parent in self._children_of
            for child in self._children_of[parent]
        ]

    # TODO(amin): Eliminate dead-end nodes from exported graph.
    def export(self, connected_only=True):
        """Print a string to stdout that can be piped to Graphviz to
        generate a graph diagram.
        """
        export = StringIO()
        export.write('digraph G {\n')
        export.write('    graph [rankdir=LR];\n')
        export.write('    node [width=0.75 shape=circle];\n')

        edges = [
            (p, c)
            for p, c in self.edges()
            if p is not None and c is not None
        ]
        for parent, child in sorted(edges):
            export.write('    "{}" -> "{}";\n'.format(parent, child))

        for node in sorted(self.nodes(connected_only=connected_only)):
            export.write('    "{}" [label="{}"];\n'.format(node, node.value.capitalize()))
        export.write('}')
        return export.getvalue()


# A single node of the graph. A glyph and its position in the word.
Node = namedtuple('Node', ['value', 'position'])


def build_spelling_graph(word, graph, symbols=ELEMENTS):
    """Given a word and a graph, find all single and double-character
    glyphs in the word. Add them to the graph only if they are present
    within the given set of allowed symbols.
    """

    def pop_root(remaining, position=0, previous_root=None):
        """Pop the single and double-character roots off the front of a
        given string, then recurse into what remains.

        For the word 'because', the roots and remainders for each call
        look something like:

            'b' 'ecause'
                'e' 'cause'
                    'c' 'ause'
                        'a' 'use'
                            'u' 'se'
                                's' 'e'
                                    'e' ''
                                'se' ''
                            'us' 'e'
                        'au' 'se'
                    'ca' 'use'
                'ec' 'ause'
            'be' 'cause'

        For each root present in the set of allowed symbols, add an edge
        to the graph:

            previous root --> current root.

        Keep track of processed values for `remaining` and do not
        evaluate a given value more than once.

        Keep track of the position of each root so that repeated roots
        are distinct nodes.
        """
        if remaining == '':
            graph.add_edge(previous_root, None)
            return

        single_root = Node(remaining[0], position)
        if single_root.value.capitalize() in symbols:
            graph.add_edge(previous_root, single_root)

            if remaining not in processed:
                pop_root(remaining[1:], position + 1, previous_root=single_root)

        if len(remaining) >= 2:
            double_root = Node(remaining[0:2], position)
            if double_root.value.capitalize() in symbols:
                graph.add_edge(previous_root, double_root)

                if remaining not in processed:
                    pop_root(remaining[2:], position + 2, previous_root=double_root)
        processed.add(remaining)

    processed = set()
    pop_root(word)


def find_all_paths(parents_to_children, start, end, path=[]):
    """Return a list of all paths through a graph from start to end.
    `parents_to_children` is a dict with parent nodes as keys and sets
    of child nodes as values.

    Based on https://www.python.org/doc/essays/graphs/
    """
    path = path + [start]
    if start == end:
        return [path]
    if start not in parents_to_children.keys():
        return []
    paths = []
    for node in parents_to_children[start]:
        if node not in path:
            newpaths = find_all_paths(parents_to_children, node, end, path)
            for newpath in newpaths:
                paths.append(tuple(newpath))
    return paths


if __name__ == '__main__':
    test_word = 'Mockery'
    print('{}:\n{}'.format(test_word, spell(test_word)))
