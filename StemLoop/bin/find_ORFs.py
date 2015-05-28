#!/usr/bin/python3.4

import argparse
import sys
import os
import glob

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                             os.pardir))

from stemloop import ORF_Finder

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Find ORFs in all FASTA files in this directory"
    )
    # parser.add_argument("fasta_file")
    parser.add_argument("--min-length", default=300, type=int,
                        help="Minimum length in basepairs (default=300)")
    options = vars(parser.parse_args())

    for fasta_filename in glob.glob("*.fa"):
        print(fasta_filename)
        orfs = ORF_Finder().find_ORFs_in_fasta(fasta_filename,
                                               options["min_length"])
        print(" -> {} ORFs found".format(len(orfs)))
        print()
