# Stem-loop
Just a handy summary of some Bioinformatics tools I'm learning.

## Infernal

## RNAz

`Aligned sequences --> SVM (z-score and SCI) --> "RNA" vs. "OTHER"`

### Explanation

RNAz is based on minimum free energy (MFE) structure prediction algorithms. It
relies on the fact that structural RNAs have (i) unusual tehermodynamic stability
and (ii) conservation of secondary structure.

i. MFE depends on length and base composition of the sequence, it's difficult
   to interpret in absolute terms. RNAz calculates a *normalized* measure of
   thermodynamic stability by comparing:

   *m*: the MFE of a given sequence

   μ: the mean MFE of a large number of random sequences

   A **z-score** is calculated thus (where σ is the MFE standard deviation):

   `z = (m - μ) / σ`

   Negative z-scores mean a sequence is more stable than expected by chance.

ii. RNAz predicts a consensus secondary structure for an alignment. The *consensus*
    MFE (E<sub>A</sub>) is compared to the average MFE (E) of the individual
    sequences in the alignment, to obtain a structure conservation index:
    SCI = E<sub>A</sub> / E

    SCI will be high if the sequences fold togther 'equally well as if folded
    individually'. Low SCI means no consensus fold can be found.

Finally, RNAz uses a support vector machine (SVM) learning algorithm, trained
on a large test set of well known ncRNAs. The z-score and SCI are used with this
SVM to classify an alignment of sequences as either [Structural] "RNA" or "OTHER".

### Cheatsheet

- RNAz takes a multiple sequence alignment as input: Clustal W or MAF formats.
- In its most basic form, it would be run as `RNAz tRNA.maf` to score an alignment.
- Use `--forward`, `--reverse`, and `--both-strands` to explicitely specify
reading direction.
- `rnazWindow.pl --window=120 --slide=40 unknown.aln | RNAz --both-strands`
- `| grep Prediction` to get a quick overview on the results.
- `rnazSelectSeqs.pl -n 5 miRNA.maf | RNAz` to select an optimal subset of sequences.
- ```shell
rnazWindow.pl --min-seqs=4 input.maf | tee windows.maf | \
RNAz --both-strands --no-shuffle -cutoff=0.5 | tee rnaz.out | \
rnazCluster.pl --html > results.dat
```
- `rnazCluster.pl --html results.dat > results/results.html` to generate an
`index.html` file.
- `rnazFilter.pl "P>0.9" results.dat` will list windows with a P-value higher than 0.9.

### Links

- Source: https://www.tbi.univie.ac.at/~wash/RNAz/#download
- Manual: https://www.tbi.univie.ac.at/~wash/RNAz/manual.pdf

## ViennaRNA

## NCBI BLAST

- Source: ftp://ftp.ncbi.nlm.nih.gov/blast/executables/LATEST/
- Docs: http://www.ncbi.nlm.nih.gov/books/NBK52640/

