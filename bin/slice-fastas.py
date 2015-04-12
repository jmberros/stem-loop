#!/usr/bin/python
#-*- encoding:utf-8 -*-

import sys
import os
import argparse
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord

def slice_fasta(filename, subseq_name, start, end):
    is_antisense = end < start
    seq_record = SeqIO.read(filename, "fasta")
    subseq_filename = filename.replace(".fa", "__{}.fa".format(subseq_name))

    if is_antisense:
        subseq_filename = subseq_filename.replace(".fa", "-antisense.fa")
        seq = seq_record.reverse_complement().seq
        subseq_record = SeqRecord(seq[end-1:start]) # Include limits of range
    else:
        seq = seq_record.seq
        subseq_record = SeqRecord(seq[start-1:end])

    subseq_record.id = "{}_{}".format(seq_record.name, subseq_name)
    with open(subseq_filename, "w") as file:
        file.write(subseq_record.format("fasta"))
    return subseq_filename if os.path.isfile(subseq_filename) else None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Slice FASTAs")
    parser.add_argument("filename", help="FASTA to slice")
    parser.add_argument("--name", help="Subsequence name")
    parser.add_argument("-f", "--from", type=int, help="Start nucleotide", required=True)
    parser.add_argument("-t", "--to", type=int, help="End nucleotide", required=True)

    for line in sys.stdin:
        args = line.rstrip("\n").split(" ")
        args = vars(parser.parse_args(args))

        subseq_filename= slice_fasta(
            filename=args['filename'], subseq_name=args['name'],
            start=args['from'], end=args['to']
        )
        print subseq_filename
