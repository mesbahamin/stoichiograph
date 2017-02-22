from collections import defaultdict, namedtuple


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
        """Add a parent-child to child relatonship to the graph.
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
            print('\t{} -> {}'.format(parent.value, child.value))
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


def build_graph(word, graph):
    """Given a word and a graph, recursively find all single and
    double-character tokens in the word and add them to the graph.
    """

    def segments(word, position=0, previous_root=None):
        if word == '':
            graph.add_edge(previous_root, None)
            return

        single_root = Node(word[0], position)
        graph.add_edge(previous_root, single_root)

        if word not in processed:
            single_stem = word[1:]
            segments(single_stem, position + 1, previous_root=single_root)

        if len(word) >= 2:
            double_root = Node(word[0:2], position)
            graph.add_edge(previous_root, double_root)

            if word not in processed:
                double_stem = word[2:]
                segments(double_stem, position + 2, previous_root=double_root)
        processed.add(word)

    processed = set()
    segments(word)


if __name__ == '__main__':
    from pprint import pprint
    w = 'inconspicuous'
    g = Graph()
    build_graph(w, g)

    spellings = list()
    for first in g._children_of[None]:
        for last in g._parents_of[None]:
            for path in find_all_paths(g._children_of, first, last):
                spellings.append(tuple(node.value for node in path))

    pprint(spellings)
