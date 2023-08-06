"""
dphon
 
Usage:
    dphon <text1> <text2> [--n=<n>] [--output=<file>] [--variants-only]
    dphon -h | --help
    dphon --version
 
Options:
    -h --help           Show this screen.
    --version           Show program version.
    --variants-only     Limit to matches with graphic variation.
    --n=<n>             Limit to matches with length >= n [default: 3].
 
Examples:
    dphon 老子丙.txt 老子乙.txt --output=matches.txt
    dphon 周南.txt 鹿鳴之什.txt --variants-only
 
Help:
    For more information on using this tool, please visit the Github repository:
    https://github.com/direct-phonology/direct
"""

from sys import stderr, stdin, stdout
from docopt import docopt

from . import __version__
from .lib import Comparator


def run():
    """CLI entrypoint."""
    arguments = docopt(__doc__, version=__version__)
    # read in the two files
    with open(arguments['<text1>'], encoding='utf-8') as file:
        text1 = file.read()
    with open(arguments['<text2>'], encoding='utf-8') as file:
        text2 = file.read()
    # store their texts and filenames
    c = Comparator(a=text1,
                   b=text2,
                   a_name=arguments['<text1>'],
                   b_name=arguments['<text2>'])
    # get and reduce initial matches
    matches = c.get_matches(min_length=int(arguments['--n']))
    # if requested, remove matches without graphic variation
    if arguments['--variants-only']:
        matches = c.matches_with_graphic_variation(matches)
    # group matches and format for output
    groups = Comparator.group_matches(matches)
    output = c.resolve_groups(groups)
    # write to a file if requested
    if arguments['--output']:
        with open(arguments['--output'], mode='w', encoding='utf8') as file:
            file.write(output)
    # otherwise write to stdout
    else:
        stdout.buffer.write(output.encode('utf-8'))
