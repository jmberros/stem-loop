from __future__ import print_function

import re

from Bio import SeqIO
from Bio.Seq import Seq


class ORF_Finder:
    def __init__(self, table=1):
        self.table = table  # 1 = Standard Code

    def find_ORFs_in_fasta(self, fasta_filename, min_nucleotides=300):
        record = SeqIO.read(fasta_filename, "fasta")
        orf_list = self.find_ORFs_in_sequence(record.seq, min_nucleotides)
        for orf in orf_list:
            orf["target_name"] = record.id

        # FIXME: Deal with MULTIfastas!!!
        return orf_list

    def find_ORFs_in_sequence(self, seq, min_nucleotides):
        strands = [("+", seq), ("-", seq.reverse_complement())]

        orf_list = []
        for strand, sequence in strands:
            for frame in range(3):
                nucleotides_to_add = 3 - (len(sequence) % 3)
                nucleotide_sequence = sequence[frame:] + "N"*nucleotides_to_add
                aminoacid_sequence = nucleotide_sequence.translate(self.table)
                orfs = re.findall("(M.*?\*)", str(aminoacid_sequence))
                min_aminoacids = min_nucleotides // 3
                orfs = [orf for orf in orfs
                        if self.is_a_possible_protein(orf, min_aminoacids)]

                for orf in orfs:
                    i = aminoacid_sequence.find(orf) * 3 + frame
                    j = i + len(orf) * 3
                    seq = sequence[i:j]
                    if strand == "-":
                        i = len(sequence) - i
                        j = len(sequence) - j
                        i, j = j, i
                        seq = sequence.reverse_complement()[i:j]

                    orf_list.append({
                        "seq": seq, "strand": strand, "from": i, "to": j,
                        "length": abs(j - i)
                    })

        return orf_list

    def is_a_possible_protein(self, aminoacid_sequence, min_aminoacids):
        is_long_enough = len(aminoacid_sequence) >= min_aminoacids
        starts_with_methionine = aminoacid_sequence[0] == "M"
        return is_long_enough and starts_with_methionine

    def test_sequence(self):
        # This test sequence has these ORFs:
        # (+) 1:22
        # (+) 55:109
        # (-) 22:61
        start = "ATG"
        stop = "TGA"
        rstart = "CAT"
        rstop = "TCA"
        nn = "NNN"*5
        seq = "n" + start + nn + stop + rstop + nn*2 + start + rstart + nn*3 + stop + "n"
        return Seq(seq)
