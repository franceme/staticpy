#!
# https://gist.githubusercontent.com/BroHui/aca2b8e6e6bdf3cb4af4b246c9837fa3/raw/6fba96c37d7c967b7a6f1b0110783ffff1a220c4/remove_comments.py

""" Strip comments and docstrings from a file.
"""

import sys, token, tokenize

def do_file(fname):
    """ Run on just one file.

    """
    source = open(fname)
    mod = open(fname + ".strip", "w")

    prev_toktype = token.INDENT
    first_line = None
    last_lineno = -1
    last_col = 0

    tokgen = tokenize.generate_tokens(source.readline)
    for toktype, ttext, (slineno, scol), (elineno, ecol), ltext in tokgen:
        if 0:   # Change to if 1 to see the tokens fly by.
            print("%10s %-14s %-20r %r" % (
                tokenize.tok_name.get(toktype, toktype),
                "%d.%d-%d.%d" % (slineno, scol, elineno, ecol),
                ttext, ltext
                ))
        if slineno > last_lineno:
            last_col = 0
        if scol > last_col:
            mod.write(" " * (scol - last_col))
        if toktype == token.STRING and (prev_toktype == token.INDENT or prev_toktype == token.NEWLINE): #https://gist.github.com/BroHui/aca2b8e6e6bdf3cb4af4b246c9837fa3?permalink_comment_id=3513489#gistcomment-3513489
            # Docstring
            mod.write("#--")
        elif toktype == tokenize.COMMENT:
            # Comment
            mod.write("##\n")
        else:
            mod.write(ttext)
        prev_toktype = toktype
        last_col = ecol
        last_lineno = elineno

def getArgs():
    import argparse
    parser = argparse.ArgumentParser("Following")
    parser.add_argument("-f","--file", help="File to watch",nargs=1, default=None)
    return parser.parse_args()

if __name__ == '__main__':
    args = getArgs()

    logg = do_file(args.file[0])