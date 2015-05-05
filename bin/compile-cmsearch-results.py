#!/usr/bin/python
#-*- encoding: utf-8 -*-

from __future__ import division
from __future__ import print_function
import ipdb # DEBUG
import re
import os
import sys
from subprocess import check_output
import csv
from pprint import pprint
from Bio import SeqIO

def main() :
    hits_per_scaffold = {}

    # Read the hits CSV and parse the rows
    hits_filename = sys.argv[1]
    with open(hits_filename, 'r') as results_csv :
        results = csv.reader( results_csv )

        for row in results :
            hit = parse_csv_row( row )
            if not hit['scaffold'] in hits_per_scaffold.keys() :
                hits_per_scaffold[ hit['scaffold'] ] = []
            hits_per_scaffold[ hit['scaffold'] ].append( hit )

    # Deal with duplicate hits
    for scaffold, hits in hits_per_scaffold.iteritems() :
        unique_hits = [dict(tuples) for tuples in set(tuple(hit.items())
                       for hit in hits)]
        selected = [ h for h in unique_hits
                     if not is_a_dupe_hit(h, hits_per_scaffold[scaffold]) ]
        hits_per_scaffold[scaffold] = selected

    # Write a file with the hits by scaffold
    output_filename = hits_filename + ".parsed-by-scaffold"
    with open(output_filename, 'w+') as output_file :
        for scaffold, hits in hits_per_scaffold.iteritems() :
            print(scaffold, file=output_file)
            seq_record = find_fasta_by_id( scaffold )
            for hit in sorted(hits, key=lambda hit: hit['seq_from']) :
                print(prettify_hit( hit ), file=output_file)
            print("-----", file=output_file)


## Helper methods ##

def is_a_dupe_hit(hit, hits) :
    # Checks if this is a duplicated hit and NOT the top one
    similar_hits = [ h for h in hits if h['accession'] == hit['accession'] and \
                                        h['seq_from'] == hit['seq_from'] and \
                                        h['seq_to'] == hit['seq_to'] ]
    top_hit = min(similar_hits, key=lambda hit: hit['e_value'])
    return hit != top_hit

def files() :
    return [ f for f in os.listdir( os.getcwd() ) ]

def fasta_files() :
    return [ f for f in files() if ".fa" in f or ".fna" in f ]

def models() :
    return [ f for f in files() if ".c.cm" in f ]

def find_fasta_by_id( id ) :
    for fasta in fasta_files() :
        records = \
            [r for r in SeqIO.parse( fasta, "fasta" ) if r.id == id ]
        if len(records) > 0 :
            return records[0]

def prettify_hit( hit ) :
    # This could be done better. Maybe a mustache template?
    entry  = ""
    entry += " ⨉" if hit['trunc'] == "3'" else "  "
    entry += "{seq_from}..{seq_to}"
    entry += " ⨉" if hit['trunc'] == "5'" else "  "
    entry += " ({strand})"
    entry += " {model} ({accession}), {mdl_percentage}% ({mdl_from}-{mdl_to}/{mdl_length})"
    entry += ", E-value: {e_value}"
    return entry.format(**hit)

def parse_csv_row( row ) :
    hit = {
        'scaffold': row[0],
        'model': row[2],
        'accession': row[3],
        'mdl_from': int( row[5] ),
        'mdl_to': int( row[6] ),
        'seq_from': int( row[7] ),
        'seq_to': int( row[8] ),
        'strand': row[9],
        'trunc': row[10],
        'gc_content': float( row[12] ),
        'bias': float( row[13] ),
        'bit_score': float( row[14] ),
        'e_value': float( row[15] ),
        'inclussion': row[16],
    }

    # Swap start and end for antisense hits
    if hit['strand'] == '-' :
        hit['seq_from'] = int( row[8] )
        hit['seq_to'] = int( row[7] )

    hit['match_length'] = hit['mdl_to'] - hit['mdl_from'] + 1
    # 'mdl_from' .. 'mdl_to is inclusive, that's why I add + 1 ^

    # Check the model length
    output = check_output("cat *{}* | grep LENG".format(hit['accession']),
                            shell=True)
    m = re.search('(\d+)', output)
    hit['mdl_length'] = int( m and m.group(0) )
    hit['mdl_percentage'] = int(100 * hit['match_length'] / hit['mdl_length'])

    return hit


if __name__ == '__main__' :
    main()
