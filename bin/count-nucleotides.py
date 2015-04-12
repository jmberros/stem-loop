#!/usr/bin/python
#-*- encoding: utf-8 -*-

import sys
from Bio import SeqIO

def count_nucleotides(fasta_filename):
    seq_record = SeqIO.read(fasta_filename, "fasta")
    return len(seq_record.seq)

if __name__ == "__main__":
    for line in sys.stdin:
        fasta_filename = line.rstrip("\n")
        print "{}\t{}".format(count_nucleotides(fasta_filename), fasta_filename)
