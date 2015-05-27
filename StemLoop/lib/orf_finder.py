import re

from Bio import SeqIO
from Bio.Seq import Seq


class ORF_Finder:
    def find_ORFs_in_fasta(self, fasta_filename):
        seq = SeqIO.read(fasta_filename, "fasta").seq
        orf_list = self.find_ORFs_in_sequence(seq)
        return orf_list

    def find_ORFs_in_sequence(self, seq):
        table = 1  # Standard Code
        strands = [(+1, seq), (-1, seq.reverse_complement())]

        orf_list = []
        for strand, sequence in strands:
            for frame in range(3):
                nucleotide_sequence = sequence[frame:]
                aminoacid_sequence = nucleotide_sequence.translate(table)
                print(aminoacid_sequence)
                orfs = re.findall("(M.*?\*)", str(aminoacid_sequence))
                orfs = [orf for orf in orfs if self.is_a_possible_protein(orf)]

                for orf in orfs:
                    i = aminoacid_sequence.find(protein) * 3
                    j = i + len(protein) * 3 + 3  # include stop codon
                    seq = nucleotide_sequence[i:j]
                    orf_list.append({"seq": seq, "start": i, "end": j})
                    print("{}..{} [ length {}, strand {}, frame {}".format(
                          seq[:30], seq[-6:], len(seq), strand, frame))

        return orf_list

    def is_a_possible_protein(self, aminoacid_sequence):
        print("Is this a possible protein? --> '{}'".format(aminoacid_sequence))
        return len(aminoacid_sequence) >= 2 and aminoacid_sequence[0] == "M"

    def test_sequence(self):
        # This test sequence has two ORFs in both strands and different frames
        start = "ATG"
        stop = "TGA"
        rstart = "CAT"
        rstop = "TCA"
        nn = "NNN"*5
        seq = start + nn + stop + rstop + nn*2 + start + rstart + nn*3 + stop
        return Seq(seq)
