from collections import namedtuple
import csv
import sys


def main():
    symbols = get_csv_data('elements.csv', 1)

    test_word = "Because"

    tokens = tokenize_sequence(test_word)
    single_matches = find_matches(tokens.single, symbols)
    pair_matches = find_matches(tokens.pair, symbols)

    print(single_matches, pair_matches)



def tokenize_sequence(sequence):
    t = namedtuple('Tokens', (['single', 'pair']))

    single = [sequence[i:i+1] for i in range(0, len(sequence))]
    pair = [sequence[i:i+2] for i in range(0, len(sequence) - 1)]
    tokens = t(single, pair)

    return tokens


def find_matches(sequence, symbols):
    matches = []
    lower_symbols = [i.lower() for i in symbols]
    lower_sequence = [i.lower() for i in sequence]

    for i in lower_sequence:
        matches += (x for x in lower_symbols if x == i)
    # TODO: Make this return an array of indices
    return matches


def get_csv_data(file_name, column):
    data = []

    with open(file_name) as infile:
        csv_reader = csv.reader(infile, skipinitialspace=True, delimiter=',')
        next(csv_reader, None)
        for row in csv_reader:
            data.append(row[column])

    return data


if __name__ == '__main__':
    main()
