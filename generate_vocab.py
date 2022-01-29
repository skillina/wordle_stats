#!/usr/bin/python3
import argparse
import string

def generate_vocabulary(inpath, length, outpath=None):

    # Returns true if word passes length filters and is entirely ascii.
    def matches_filter(word, length):
        if (length is not None) and (len(word) != length):
            return False
        return all(c in string.ascii_letters for c in word)

    def output(outfile, word):
        if outfile is not None:
            outfile.write(word + "\n")
        else:
            print(word)

    with open(inpath, 'r') as dictionary:
        outfile =  open(outpath, 'w') if (outpath is not None) else None
        lastword = None

        vocabulary = []
        for word in dictionary:
            formatted = word.strip().upper()
            if matches_filter(formatted, length):
                if lastword is None or lastword != formatted:
                    vocabulary.append(formatted)
                    output(outfile, formatted)
                    lastword = formatted
        return vocabulary
                

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate a dictionary of available words')
    parser.add_argument("--input", default="/usr/share/dict/words", help="path to the dictionary file", required=False)
    parser.add_argument("--length", default=None, type=int, help="Filter to this length", required=False)
    parser.add_argument("--output", default=None, help="Output file. Default will print to cout.", required=False)
    args = parser.parse_args()
    generate_vocabulary(args.input, args.length, args.output)
