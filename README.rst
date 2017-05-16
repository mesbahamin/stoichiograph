Stoichiograph - The Elemental Speller
=====================================

Spell words with elemental symbols from the periodic table ("He", "Cu", etc). I
made this when I was bored in Chemistry class. I wrote about the process of
making it `here`_.

.. figure:: https://cloud.githubusercontent.com/assets/5744114/21043177/7c3efe8c-bdaa-11e6-9c1a-22db4de6bb2f.png
    :alt: A list of four words and their elemental spellings

    Some words and their elemental spellings

.. _here: https://www.amin.space/blog/2017/5/elemental_speller/


Installation
------------

.. code-block::

    $ pip install stoichiograph


Usage
-----

.. code-block::

    usage: stoichiograph [-h] [-b BATCH_FILE] [-c] [--debug] [--list-elements]
                         [--export-graph] [-o OUTPUT_FILE] [-s] [-t] [-v] [-V]
                         [words [words ...]]

    Spell words with elemental symbols from the periodic table.

    positional arguments:
      words                 word(s) for which to find elemental spellings

    optional arguments:
      -h, --help            show this help message and exit
      -b BATCH_FILE, --batch-file BATCH_FILE
                            text file containing one word per line
      -c, --clobber         overwrite output file if it exists
      --debug               print debug log
      --list-elements       print list of elemental symbols and exit
      --export-graph        export graph of first word as dot code
      -o OUTPUT_FILE, --output-file OUTPUT_FILE
                            path of output json file
      -s, --sort            sort words by length
      -t, --tuples          display spellings as tuples
      -v, --verbose         print a detailed log
      -V, --version         print version info and exit


Graph Export
------------

Stoichiograph builds a graph to find a word's elemental spellings. Use the
`--export-graph` option to output dot code that `graphviz`_ can use to generate
an image of the graph.

.. code-block:: bash

    $ stoichiograph --export-graph flashbacks | dot -Tpng -o word_graph.png

.. figure:: https://cloud.githubusercontent.com/assets/5744114/26102406/abf1a33a-39e9-11e7-8bdb-fef168e8e0cf.png
    :alt: The file output by the above command

    A visualization of the directed acyclic graph of elemental spellings for
    'flashbacks'.


.. _Graphviz: http://www.graphviz.org/Home.php
