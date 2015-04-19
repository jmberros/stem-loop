#!/usr/bin/python
#-*- encoding:utf-8 -*-

import sys
import os
import argparse
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord

def slice_fasta(filename, subseq_name, start, end, subdir):
    # "Negative" nucleotides won't work for the slicing
    if start < 0:
        start = 0
        print "Warning! {} had a negative start nucleotide. I assigned 0.".format(filename)
    if end < 0:
        end = 0
        print "Warning! {} had a negative end nucleotide. I assigned 0.".format(filename)

    is_antisense = end < start
    seq_record = SeqIO.read(filename, "fasta")
    if not os.path.exists(subdir):
        os.makedirs(subdir)
    subseq_filename = subdir + "/" + \
        filename.replace(".fa", "__sliced_{}.fa".format(subseq_name))

    if is_antisense:
        seq = seq_record.reverse_complement().seq
        subseq_record = SeqRecord(seq[end-1:start]) # Include limits of range
    else:
        seq = seq_record.seq
        subseq_record = SeqRecord(seq[start-1:end]) # Include limits of range

    subseq_record.id = "{}_{}".format(seq_record.name, subseq_name)
    with open(subseq_filename, "w") as file:
        file.write(subseq_record.format("fasta"))
    return subseq_filename if os.path.isfile(subseq_filename) else None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Slice FASTAs")
    parser.add_argument("filename", help="FASTA to slice")
    parser.add_argument("--subdir", default="sliced-fastas", help="Subdirectory to move sliced files")
    parser.add_argument("--name", help="Subsequence name")
    parser.add_argument("-f", "--from", type=int, help="Start nucleotide", required=True)
    parser.add_argument("-t", "--to", type=int, help="End nucleotide", required=True)

    for line in sys.stdin:
        args = line.rstrip("\n").split(" ")
        args = vars(parser.parse_args(args))

        subseq_filename= slice_fasta(
            filename=args['filename'], subseq_name=args['name'],
            start=args['from'], end=args['to'], subdir=args['subdir']
        )
        print subseq_filename
