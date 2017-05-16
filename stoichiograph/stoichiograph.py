#!/usr/bin/python3

import argparse
import collections
import json
import logging
import pathlib

from stoichiograph import speller

__title__ = 'stoichiograph'
__author__ = 'Amin Mesbah'
__version__ = '0.0.1'
__description__ = 'Spell words with elemental symbols from the periodic table.'


def get_args():
    parser = argparse.ArgumentParser(
        prog=__title__,
        description=__description__
    )
    parser.add_argument(
        'words',
        help='word(s) for which to find elemental spellings',
        type=str,
        nargs='*'
    )
    parser.add_argument(
        '-b', '--batch-file',
        help='text file containing one word per line'
    )
    parser.add_argument(
        '-c', '--clobber', action='store_true',
        help='overwrite output file if it exists'
    )
    parser.add_argument(
        '--debug', action='store_true',
        help='print debug log'
    )
    parser.add_argument(
        '--list-elements', action='store_true',
        help='print list of elemental symbols and exit'
    )
    parser.add_argument(
        '--export-graph', action='store_true',
        help='export graph of first word as dot code'
    )
    parser.add_argument(
        '-o', '--output-file',
        help='path of output json file'
    )
    parser.add_argument(
        '-s', '--sort', action='store_true',
        help='sort words by length'
    )
    parser.add_argument(
        '-t', '--tuples', action='store_true',
        help='display spellings as tuples'
    )
    parser.add_argument(
        '-v', '--verbose', action='store_true',
        help='print a detailed log'
    )
    parser.add_argument(
        '-V', '--version', action='store_true',
        help='print version info and exit'
    )

    return parser.parse_args()


def main():
    args = get_args()

    if args.version:
        print('{} {}'.format(__title__, __version__))
        raise SystemExit

    if args.list_elements:
        print('{} Elements:'.format(len(speller.ELEMENTS)))
        print(sorted(list(speller.ELEMENTS)))
        raise SystemExit

    if args.debug:
        CONSOLE_LOG_LEVEL = logging.DEBUG
    elif args.verbose:
        CONSOLE_LOG_LEVEL = logging.INFO
    else:
        CONSOLE_LOG_LEVEL = logging.WARNING

    logging.basicConfig(level=CONSOLE_LOG_LEVEL)
    logging.debug('{} {}'.format(__title__, __version__))

    SORT_WORDS = args.sort
    TUPLES = args.tuples

    if args.output_file:
        OUTPUT_FILE = pathlib.Path(args.output_file)
        CLOBBER = args.clobber

        if not CLOBBER and OUTPUT_FILE.exists():
            logging.warning(
                "{} exists. To overwrite, use '--clobber'.".format(OUTPUT_FILE)
            )
            raise SystemExit

    if args.batch_file:
        words_file = pathlib.Path(args.batch_file)
        with words_file.open('r') as f:
            dictionary = f.readlines()

        # TODO(amin): Handle punctuation, apostraphies, etc.
        words = [word.rstrip('\n') for word in dictionary if "'" not in word]
    else:
        words = args.words

    if SORT_WORDS:
        words.sort(key=len, reverse=True)

    if args.export_graph and words:
        g = speller.Graph()
        speller.build_spelling_graph(words[0], g)
        print(g.export())
        raise SystemExit

    spellable = collections.OrderedDict()

    for word in words:
        if TUPLES:
            spellings = speller.spell(word)
        else:
            spellings = [''.join(s) for s in speller.spell(word)]

        if spellings:
            spellable[word] = spellings
            for spelling in spellings:
                print(spelling)

    if args.output_file:
        with OUTPUT_FILE.open('w') as f:
            json.dump(spellable, f, indent=4, sort_keys=False)

    logging.debug('Done!')


if __name__ == '__main__':
    main()
