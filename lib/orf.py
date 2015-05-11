from Bio.Data import CodonTable


class ORF:
    def __init__(self):
        self.standard_table = CodonTable.unambiguous_dna_by_name["Standard"]
        self.stop_codons = self.standard_table.stop_codons
        self.start_codons = self.standard_table.start_codons

    def getORF(self, sequence, threshold):
        start_codon_index = 0
        end_codon_index = 0
        start_codon_found = False

        orfs = []

        for j in range(0, 3):
            for indx in range(j, len(sequence), 3):
                current_codon = sequence[indx:indx+3]
                if current_codon in self.start_codons and not start_codon_found:
                    start_codon_found = True
                    start_codon_index = indx
                if current_codon in self.stop_codons and start_codon_found:
                    end_codon_index = indx
                    length = end_codon_index - start_codon_index + 1
                    if length >= threshold * 3:
                        orfs.append(start_codon_index)
                    start_codon_found = False

            start_codon_index = 0
            end_codon_index = 0
            start_codon_found = False

        return len(orfs), orfs

    def getComplementORF(self, sequence, threshold):
        start_codon_index = 0
        end_codon_index = 0
        start_codon_found = False

        complement_orfs = []

        for j in range(0, 3):
            for indx in range(j, len(sequence), 3):
                current_codon = sequence[indx:indx+3]
                if current_codon in self.start_codons and not start_codon_found:
                    start_codon_found = True
                    start_codon_index = indx
                if current_codon in self.stop_codons and start_codon_found:
                    end_codon_index = indx
                    length = end_codon_index - start_codon_index + 1
                    if length >= threshold * 3:
                        complement_orfs.append(len(sequence)-end_codon_index-3)
                    start_codon_found = False

            start_codon_index = 0
            end_codon_index = 0
            start_codon_found = False

        return len(complement_orfs), complement_orfs
