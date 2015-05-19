#!/usr/bin/python3.4


from __future__ import division
from __future__ import print_function

import sys
import os
import re
import argparse
import csv
import pystache
import logging

# from pprint import pprint  # Debug
from subprocess import check_output
from Bio import SeqIO

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


class InfernalOutputParser:
    def __init__(self):
        self.scaffold_lengths = {}

    def parse_results(self, hits_filename, accessory_filename=None):
        # logging.debug("hits_filename: {}".format(hits_filename))
        # logging.debug("accessory_filename: {}".format(accessory_filename))
        hits_per_scaffold = {}

        # Read the hits CSV and parse its rows
        with open(hits_filename, 'r') as results_csv:
            results = csv.reader(results_csv)
            for row in results:
                # logging.debug("parse hit:\n->{}".format(row))
                hit = self.parse_cmsearch_hit(row)
                if not hit['scaffold'] in hits_per_scaffold.keys():
                    hits_per_scaffold[hit['scaffold']] = []
                hits_per_scaffold[hit['scaffold']].append(hit)

        # Read extra elements from an accessory file with coordinates and names
        if accessory_filename:
            with open(accessory_filename, 'r') as accessory_csv:
                results = csv.reader(accessory_csv)
                for row in results:
                    # logging.debug("parse this row:\n\t{}".format(row))
                    element = self.parse_accessory_element(row)
                    if not element['scaffold'] in hits_per_scaffold.keys():
                        hits_per_scaffold[element['scaffold']] = []
                    hits_per_scaffold[element['scaffold']].append(element)

        # Deal with duplicate hits
        for scaffold, hits in hits_per_scaffold.items():
            # logging.debug("check if {} hits are dupes".format(scaffold))
            unique_hits = [dict(tuples) for tuples in set(tuple(hit.items())
                           for hit in hits)]
            selected = [
                h for h in unique_hits
                if not self.is_a_dupe_hit(h, hits_per_scaffold[scaffold])
            ]
            hits_per_scaffold[scaffold] = selected

        # Write a CSV file with the hits by scaffold
        output_filename = hits_filename + ".parsed-by-scaffold"
        # logging.debug("write to {}".format(output_filename))
        with open(output_filename, 'w+') as output_file:
            for scaffold, hits in hits_per_scaffold.items():
                title = scaffold
                seq_length = self.scaffold_length(scaffold)

                if seq_length:
                    title += " ({} pb)".format(seq_length)
                print(title, file=output_file)
                for hit in sorted(hits, key=lambda hit: hit['seq_from']):
                    print(hit, file=output_file)
                print("", file=output_file)

        # Write an HTML file
        html_filename = hits_filename + ".html"
        templ = self.formatted_hits_template()
        # logging.debug("write to {}".format(html_filename))
        with open(html_filename, 'w+') as html, open(templ, 'r') as template:
            hits_per_scaffold_list = [
                {'scaffold': scaffold,
                 'scaffold_length': self.scaffold_length(scaffold),
                 'hits': sorted(hits, key=lambda hit: hit['seq_from'])}
                for scaffold, hits in hits_per_scaffold.items()
            ]
            template_data = {
                'hits_per_scaffold': hits_per_scaffold_list,
                'input_filename': hits_filename,
                'output_filename': output_filename,
            }
            rendered_template = pystache.render(template.read(),
                                                template_data)
            print(rendered_template, file=html)

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

    def scaffold_length(self, id):
        # logging.debug("--> search for {}".format(id))
        if not self.scaffold_lengths.get(id):
            for fasta in self.fasta_files():
                records = \
                    [r for r in SeqIO.parse(fasta, "fasta") if r.id == id]
                if len(records) > 0:
                    self.scaffold_lengths[id] = len(records[0])
                    # logging.debug(self.scaffold_lengths)

        return self.scaffold_lengths[id]

    def formatted_hits_template(self):
        return os.path.normpath(os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "../templates/formatted_hits.html.mustache"
        ))

    def parse_accessory_element(self, row):
        element = {
            'scaffold': row[0],
            'seq_from': int(row[1]),
            'seq_to': int(row[2]),
            'model': row[3],
            'inclussion': "!",  # Assume we're sure of the element's presence
        }

        try:
            element['extra_info'] = row[4]
        except IndexError:
            pass

        self.add_seq_data(element)
        # Swap start and end for elements in the antisense strands
        if element['seq_from'] > element['seq_to']:
            element['seq_from'] = int(row[2])
            element['seq_to'] = int(row[1])
            element['strand'] = "-"
        else:
            element['strand'] = "+"

        return element

    def parse_cmsearch_hit(self, row):
        # logging.debug("-> parse cmsearch hit")
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
            'inclussion': row[16] == "!",
        }

        hit['trunc_3'] = row[10] == "3'"
        hit['trunc_5'] = row[10] == "5'"
        # TODO: What's the notation for truncation in both ends?

        self.add_seq_data(hit)
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

    def add_seq_data(self, element):
        # logging.debug("add_seq_data to {}".format(element))
        seq_length = self.scaffold_length(element['scaffold'])
        element['seq_length'] = abs(element['seq_to']-element['seq_from']) + 1
        element['seq_percentage'] = round(100 * element['seq_length'] /
                                          seq_length, 2)
        first_nucleotide = min(element['seq_from'], element['seq_to'])
        element['seq_offset_percentage'] = round(100 * first_nucleotide /
                                                 seq_length, 2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Compile cmsearch result CSV")
    parser.add_argument('hits_filename')
    parser.add_argument('--accessory-filename',
                        help="accesory CSV with coordinates")
    options = vars(parser.parse_args())

    InfernalOutputParser().parse_results(options['hits_filename'],
                                         options['accessory_filename'])
