# TODO:
# test that all letters in word are present in some element
# generate group_maps only for the exact number of chars in word
#  

from collections import namedtuple
from itertools import chain, product
import csv
import sys


def get_csv_data(file_name, column):
    """Return in a list all data from a given column of a .csv file"""
    data = []

    with open(file_name) as infile:
        csv_reader = csv.reader(infile, skipinitialspace=True, delimiter=',')
        next(csv_reader, None)
        for row in csv_reader:
            data.append(row[column])

    return data


def tokenize_sequence(sequence):
    """Return a list each of all single and double character tokens."""
    t = namedtuple('Tokens', (['single', 'pair']))

    single = [sequence[i:i+1] for i in range(0, len(sequence))]
    pair = [sequence[i:i+2] for i in range(0, len(sequence) - 1)]
    tokens = t(single, pair)

    return tokens


def find_matches(sequence, symbols):
    """Return a list of all element symbols matching
    an item in the given sequence.
    """
    matches = []
    indices = []
    lower_symbols = [i.lower() for i in symbols]
    lower_sequence = [i.lower() for i in sequence]

    for i in lower_sequence:
        matches += (x for x in lower_symbols if x == i)
        indices += (lower_symbols.index(x) for x in lower_symbols if x == i)

    return matches


def groupings(word, group_sizes = [1,2]):
    """Return a list of all permutations of possible character grouping
    arrangements of a word. group_sizes defines the possible sizes of 
    character groups, and by default allows only singles and pairs.
    """
    group_maps = []
    length = len(word)
    cartesian_product = (product(group_sizes, repeat=r)
                         for r in range(1, length + 1))
    products = chain.from_iterable(cartesian_product)

    # include only products that represent the correct number of chars
    for p in products:
        if sum(p) == length:
            p = [tuple(x for x in p)]
            for x in p:
                if x not in group_maps:
                    group_maps.append(x)

    return group_maps 


def main():
    symbols = get_csv_data('elements.csv', 1)

    test_word = "Because"

    tokens = tokenize_sequence(test_word)
    single_matches = find_matches(tokens.single, symbols)
    pair_matches = find_matches(tokens.pair, symbols)

    print(single_matches, pair_matches)


if __name__ == '__main__':
    main()
