import csv

def main():
    symbols = get_symbols('elements.csv')
    print(symbols)


def get_symbols(file_name):
    symbols = []

    with open(file_name) as infile:
        csv_reader = csv.reader(infile, skipinitialspace=True, delimiter=',')
        next(csv_reader, None)
        for row in csv_reader:
            symbols.append(row[1])

    return symbols

if __name__ == '__main__':
    main()
