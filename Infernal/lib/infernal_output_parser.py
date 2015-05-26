from __future__ import division
from __future__ import print_function

import os
import re
import pystache
import pandas

from subprocess import check_output
from Bio import SeqIO

# import sys
# import logging
# from pprint import pprint  # Debug
# import logging
# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


class InfernalOutputParser:
    def __init__(self):
        self.scaffold_lengths = {}  # For memoization purposes

    def parse_results_from_files(self, hits_csv, accessory_csv=None):
        hits = pandas.read_csv(hits_csv, names=self.cmsearch_headers())
        if accessory_csv:  # expects headers in the CSV
            accessory_elements = pandas.read_csv(accessory_csv)

        self.parse_results(hits, accessory_elements)

        html_filename = hits_csv.replace(".csv", "") + ".html"
        return self.render_as_HTML(self.all_elements, html_filename)

    def parse_results(self, hits, accessory_elements=None):
        [self.parse_cmsearch_hit(i, hit, hits) for i, hit in hits.iterrows()]
        self.hits = self.filter_out_dupe_hits(hits)
        self.hits = self.round_some_fields(self.hits)
        all_elements = self.hits

        if accessory_elements is not None:
            self.parse_accessory_dataframe(accessory_elements)
            self.accessory_elements = self.round_some_fields(accessory_elements)
            all_elements = pandas.concat([self.hits, self.accessory_elements],
                                         ignore_index=True)

        self.all_elements = \
            all_elements.where((pandas.notnull(all_elements)), '')

        return self.render_as_HTML(self.all_elements)

    def render_as_HTML(self, dataframe, html_filename=None):
        hits_per_scaffold = []  # will be a list of dicts

        for target in dataframe.target_name.unique():
            target_elements = dataframe[dataframe.target_name == target]
            hits_in_this_scaffold = [
                dict(row) for i, row in
                target_elements.sort('seq_from').iterrows()
            ]
            hits_per_scaffold.append({
                'target_name': target,
                'target_length': self.sequence_length_from_fasta(target),
                'hits': hits_in_this_scaffold
            })

        template_data = {
            'hits_per_scaffold': sorted(hits_per_scaffold,
                                        key=lambda data: data['target_name']),
            'unique_hits_count': len(self.hits),
        }

        template_filename = self.formatted_hits_template()
        rendered_template = ""
        with open(template_filename, 'r') as template:
            rendered_template = pystache.render(template.read(), template_data)

        if html_filename is not None:
            with open(html_filename, 'w+') as html:
                print(rendered_template, file=html)

        return rendered_template

    # Helper methods #

    def cmsearch_headers(self):
        return [
            "target_name", "target_accession", "query_name", "query_accession",
            "mdl", "mdl_from", "mdl_to", "seq_from", "seq_to", "strand",
            "trunc", "pass", "gc_content", "bias", "bit_score", "e_value",
            "inclussion", "target_description"
        ]

    def files(self):
        return [f for f in os.listdir(os.getcwd())]

    def fasta_files(self):
        return [f for f in self.files() if ".fa" in f or ".fna" in f]

    # def models(self):
        # return [f for f in self.files() if ".c.cm" in f]

    def sequence_length_from_fasta(self, id):
        if not self.scaffold_lengths.get(id):
            for fasta in self.fasta_files():
                records = \
                    [r for r in SeqIO.parse(fasta, "fasta") if r.id == id]
                if len(records) > 0:
                    self.scaffold_lengths[id] = len(records[0])

        return self.scaffold_lengths[id]

    def formatted_hits_template(self):
        return os.path.normpath(os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "../templates/formatted_hits.html.mustache"
        ))

    def filter_out_dupe_hits(self, hits):
        indexes_to_remove = []

        for i, hit in hits.iterrows():
            similar_hits = hits[
                (hits.query_accession == hit['query_accession']) &
                (hits.seq_from == hit['seq_from']) &
                (hits.seq_to == hit['seq_to'])
            ]

            if len(similar_hits) > 1:
                # The lowest the E-value, the better:
                top_hit_index = similar_hits['e_value'].idxmin()
                for i, hit in similar_hits.iterrows():
                    if i == top_hit_index: continue
                    indexes_to_remove.append(i)

        return hits[~hits.index.isin(indexes_to_remove)]

    def parse_accessory_dataframe(self, accessory_elements):
        for i, element in accessory_elements.iterrows():
            if element['seq_from'] > element['seq_to']:
                accessory_elements.loc[i, 'strand'] = '-'
            else:
                accessory_elements.loc[i, 'strand'] = '+'

            accessory_elements.loc[i, 'accessory'] = True
            self.add_seq_data(element, accessory_elements)
            self.swap_coordinates_for_antisense(element, accessory_elements)

    def parse_cmsearch_hit(self, i, hit, hits_dataframe):
        hits_dataframe.loc[i, 'trunc_3'] = hit['trunc'] == "3'"
        hits_dataframe.loc[i, 'trunc_5'] = hit['trunc'] == "5'"
        # TODO: What's the notation for truncation in both ends?

        hits_dataframe.loc[i, 'accessory'] = False
        hits_dataframe.loc[i, 'above_inclussion'] = hit['inclussion'] == "!"

        self.add_seq_data(hit, hits_dataframe)
        self.swap_coordinates_for_antisense(hit, hits_dataframe)

        match_length = int(hit['mdl_to'] - hit['mdl_from'] + 1)
        hits_dataframe.loc[i, 'match_length'] = match_length
        # 'mdl_from' .. 'mdl_to' is an inclusive range, that's why I add 1

        # Check the model length from the model file in the cwd
        grep_model = "cat *{}* | grep LENG".format(hit['query_accession'])
        out = check_output(grep_model, shell=True).decode("utf-8")

        match = re.search('(\d+)', out)
        mdl_length = int(match and match.group(0))
        hits_dataframe.loc[i, 'mdl_length'] = mdl_length
        hits_dataframe.loc[i, 'mdl_percentage'] = \
            int(100*match_length/mdl_length)

    def swap_coordinates_for_antisense(self, element, df):
        if element['seq_from'] > element['seq_to']:
            start = element['seq_to']
            df.loc[element.name, 'seq_to'] = element['seq_from']
            df.loc[element.name, 'seq_from'] = start

    def add_seq_data(self, element, df):
        target_length = self.sequence_length_from_fasta(element['target_name']) 
        df.loc[element.name, 'target_length'] = int(target_length)

        seq_length = abs(element['seq_to']-element['seq_from']) + 1
        df.loc[element.name, 'seq_length'] = seq_length

        df.loc[element.name, 'seq_percentage'] = 100*seq_length / target_length

        first_nucleotide = min(element['seq_from'], element['seq_to'])
        df.loc[element.name, 'seq_offset_percentage'] = \
            100 * first_nucleotide / target_length

    def round_some_fields(self, df):
        try:
            df.match_length.update(df.match_length.astype(int))
            df.mdl_percentage = df.mdl_percentage.round(decimals=0)
            df.mdl_from = df.mdl_from.round(decimals=0)
            df.mdl_to = df.mdl_to.round(decimals=0)
            df.mdl_length = df.mdl_length.round(decimals=0)
            df.e_value = df.e_value.round(decimals=7)
        except AttributeError:
            pass

        df.seq_length = df.seq_length.round(decimals=0)
        df.seq_percentage = df.seq_percentage.round(decimals=0)

        return df

