#!/usr/bin/python
#-*- encoding: utf-8 -*-


import sys
import argparse
from Bio import SeqIO

def split_multifasta(multifasta_filename, batch_size=1000):
    record_iterator = SeqIO.parse(open(multifasta_filename), "fasta")
    for i, batch in enumerate(batch_iterator(record_iterator, batch_size)):
        offset = (i * batch_size) + 1
        limit = offset + batch_size - 1
        batch_filename = multifasta_filename + \
            "__batch-{}__{}-{}.fasta".format((i+1), offset, limit)
        with open(batch_filename, "w") as batch_file:
            count = SeqIO.write(batch, batch_file, "fasta")
            print "Wrote {} records to {}".format(count, batch_filename)

def batch_iterator(iterator, batch_size):
    """Returns lists of length batch_size.

    This can be used on any iterator, for example to batch up
    SeqRecord objects from Bio.SeqIO.parse(...), or to batch
    Alignment objects from Bio.AlignIO.parse(...), or simply
    lines from a file handle.

    This is a generator function, and it returns lists of the
    entries from the supplied iterator.  Each list will have
    batch_size entries, although the final list may be shorter.
    """
    entry = True #Make sure we loop once
    while entry:
        batch = []
        while len(batch) < batch_size:
            try:
                entry = iterator.next()
            except StopIteration:
                entry = None
            if entry is None:
                #End of file
                break
            batch.append(entry)
        if batch:
            yield batch

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split MultiFASTA")
    parser.add_argument("filename", help="MultiFASTA to split")
    parser.add_argument("-n", default=1000, type=int,
                        help="Batch size: How many FASTAs per file")
    args = parser.parse_args()

    split_multifasta(args.filename, args.n)

