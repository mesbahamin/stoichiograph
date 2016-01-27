from collections import namedtuple
import csv


def main():
    symbols = get_csv_data('elements.csv', 1)
    test_word = "Osiris"

    tokens = tokenize_sequence(test_word)

    print(tokens.singles)
    print(tokens.pairs)
    print(find_matches(tokens.singles, symbols))
    print(find_matches(tokens.pairs, symbols))

def tokenize_sequence(sequence):
    """Splits a sequence into one list of individual elements, and one of pairs."""

    t = namedtuple('Tokens', (['singles', 'pairs']))

    singles = [sequence[i:i+1] for i in range(0, len(sequence))]
    pairs = [sequence[i:i+2] for i in range(0, len(sequence) - 1)]
    tokens = t(singles, pairs)

    return tokens


def find_matches(sequence, symbols):
    matches = []

    for i in sequence:
        matches += (x for x in symbols if x == i)

    return matches


def get_csv_data(file_name, column):
    symbols = []

    with open(file_name) as infile:
        csv_reader = csv.reader(infile, skipinitialspace=True, delimiter=',')
        next(csv_reader, None)
        for row in csv_reader:
            symbols.append(row[column])

    return symbols


if __name__ == '__main__':
    main()
