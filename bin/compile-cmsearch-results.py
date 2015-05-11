#!/usr/bin/python3.4


from __future__ import division
from __future__ import print_function

import os
import re
import argparse
import csv
import ipdb  # Debug

from pprint import pprint  # Debug
from subprocess import check_output
from Bio import SeqIO


class InfernalOutputParser:
    def parse_results(self, hits_filename, accessory_filename=None):
        hits_per_scaffold = {}

        # Read the hits CSV passed as first argument and parse its rows
        with open(hits_filename, 'r') as results_csv:
            results = csv.reader(results_csv)
            for row in results:
                hit = self.parse_cmsearch_hit(row)
                if not hit['scaffold'] in hits_per_scaffold.keys():
                    hits_per_scaffold[hit['scaffold']] = []
                hits_per_scaffold[hit['scaffold']].append(hit)

        # Read extra elements from accessory file with coordinates and names
        with open(accessory_filename, 'r') as accessory_csv:
            results = csv.reader(accessory_csv)
            for row in results:
                element = self.parse_accessory_element(row)
                if not element['scaffold'] in hits_per_scaffold.keys():
                    hits_per_scaffold[element['scaffold']] = []
                hits_per_scaffold[element['scaffold']].append(element)

        # Deal with duplicate hits
        for scaffold, hits in hits_per_scaffold.items():
            unique_hits = [dict(tuples) for tuples in set(tuple(hit.items())
                           for hit in hits)]
            pprint(unique_hits)
            selected = [
                h for h in unique_hits
                if not self.is_a_dupe_hit(h, hits_per_scaffold[scaffold])
            ]
            hits_per_scaffold[scaffold] = selected

        # Write a file with the hits by scaffold
        output_filename = hits_filename + ".parsed-by-scaffold"
        with open(output_filename, 'w+') as output_file:
            for scaffold, hits in hits_per_scaffold.items():
                title = scaffold
                seq_record = self.find_fasta_by_id(scaffold)
                if seq_record:
                    title += " ({} pb)".format(len(seq_record))
                print(title, file=output_file)
                for hit in sorted(hits, key=lambda hit: hit['seq_from']):
                    print(self.prettify_hit(hit), file=output_file)
                print("-----", file=output_file)

    # Helper methods #

    def is_a_dupe_hit(self, hit, hits):
        # Checks if this is a duplicated hit and NOT the top one
        similar_hits = [h for h in hits
                        if h['model'] == hit['model'] and
                        h['seq_from'] == hit['seq_from'] and
                        h['seq_to'] == hit['seq_to']]
        if len(similar_hits) == 1:
            return False
        else:
            top_hit = min(similar_hits, key=lambda hit: hit['e_value'])
            return hit != top_hit

    def files(self):
        return [f for f in os.listdir(os.getcwd())]

    def fasta_files(self):
        return [f for f in self.files() if ".fa" in f or ".fna" in f]

    def models(self):
        return [f for f in self.files() if ".c.cm" in f]

    def find_fasta_by_id(self, id):
        for fasta in self.fasta_files():
            records = \
                [r for r in SeqIO.parse(fasta, "fasta") if r.id == id]
            if len(records) > 0:
                return records[0]

    def prettify_hit(self, hit):
        hit['trunc_3'] = "x" if hit.get('trunc_3') else " "
        hit['trunc_5'] = "x" if hit.get('trunc_5') else " "
        if hit.get('accession'):
            hit['model'] = "{model} ({accession})".format(**hit)
        if hit.get('e_value'):
            hit['extra_info'] = ("{mdl_percentage}% "
                                 "({mdl_from}-{mdl_to}/{mdl_length}), "
                                 "E-value: {e_value}").format(**hit)
        else:
            hit['extra_info'] = hit.get('extra_info') or ""

        return ("{trunc_3}{seq_from}..{seq_to}{trunc_5}""({strand}) "
                "{model}, {extra_info}").format(**hit)

    def parse_accessory_element(self, row):
        element = {
            'scaffold': row[0],
            'seq_from': int(row[1]),
            'seq_to': int(row[2]),
            'model': row[3],
        }

        try:
            element['extra_info'] = row[4]
        except IndexError:
            pass

        # Swap start and end for elements in the antisense strands
        if element['seq_from'] > element['seq_to']:
            element['seq_from'] = int(row[2])
            element['seq_to'] = int(row[1])
            element['strand'] = "-"
        else:
            element['strand'] = "+"

        return element

    def parse_cmsearch_hit(self, row):
        hit = {
            'scaffold': row[0],
            'model': row[2],
            'accession': row[3],
            'mdl_from': int(row[5]),
            'mdl_to': int(row[6]),
            'seq_from': int(row[7]),
            'seq_to': int(row[8]),
            'strand': row[9],
            'gc_content': float(row[12]),
            'bias': float(row[13]),
            'bit_score': float(row[14]),
            'e_value': float(row[15]),
            'inclussion': row[16],
        }

        hit['trunc_3'] = row[10] == "3'"
        hit['trunc_5'] = row[10] == "5'"
        # TODO: What's the notation for truncation in both ends?

        # Swap start and end for antisense hits
        if hit['strand'] == '-':
            hit['seq_from'] = int(row[8])
            hit['seq_to'] = int(row[7])

        hit['match_length'] = hit['mdl_to'] - hit['mdl_from'] + 1
        # 'mdl_from' .. 'mdl_to is inclusive, that's why I add + 1 ^

        # Check the model length
        output = check_output("cat *{}* | grep LENG".format(hit['accession']),
                              shell=True).decode("utf-8")
        m = re.search('(\d+)', output)
        hit['mdl_length'] = int(m and m.group(0))
        hit['mdl_percentage'] = int(100 * hit['match_length'] /
                                    hit['mdl_length'])

        return hit


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Compile cmsearch result CSV")
    parser.add_argument('hits_filename')
    parser.add_argument('accessory_filename', default=None)
    options = vars(parser.parse_args())

    InfernalOutputParser().parse_results(options['hits_filename'],
                                         options['accessory_filename'])
