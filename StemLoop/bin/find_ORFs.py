#!/usr/bin/python3.4

import argparse
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                             os.pardir))

from stemloop import ORF_Finder

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find ORFs in a FASTA file")
    parser.add_argument("fasta_file")
    options = vars(parser.parse_args())

    ORF_Finder().find_ORFs_to_CSV()
