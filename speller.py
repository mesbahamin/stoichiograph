import csv

def main():
    symbols = get_csv_data('elements.csv', 1)
    test_word = "Osiris"
    print(find_matches(test_word, symbols))

def find_matches(word, symbols):
    matches = []

    for char in word:
        single = char
        matches += (x for x in symbols if x == char)

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
