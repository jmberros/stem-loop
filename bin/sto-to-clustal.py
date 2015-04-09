#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os

from Bio import AlignIO

def sto_to_clustal(stockholm_filename):
    clustal_filename = filename.replace(".sto", ".aln")

    if os.path.isfile(stockholm_filename):
        AlignIO.convert(stockholm_filename, "stockholm",
                        clustal_filename, "clustal")
        print clustal_filename 
    else:
        sys.exit("❌ There's no filename '%s'" % stockholm_filename)


if __name__ == "__main__":
    for line in sys.stdin:
        filename = line.rstrip("\n")
        sto_to_clustal(filename)
