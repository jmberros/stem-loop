# Stem-loop

## Infernal

## RNAz
RNAz is based on minimum free energy (MFE) structure prediction algorithms. It
relies on the fact that structural RNAs have (i) unusual tehermodynamic stability
and (ii) conservation of secondary structure.

(i) MFE depends on length and base composition of the sequence, it's difficult
    to interpret in absolute terms. RNAz calculates a *normalized* measure of
    thermodynamic stability by comparing:
    *m*: the MFE of a given sequence
    μ: the mean MFE of a large number of random sequences

    A **z-score** is calculated thus:
    ```
    z = (m - μ) / σ
    ```

- Source: https://www.tbi.univie.ac.at/~wash/RNAz/#download
- Manual: https://www.tbi.univie.ac.at/~wash/RNAz/manual.pdf

## ViennaRNA

## NCBI BLAST

- Source: ftp://ftp.ncbi.nlm.nih.gov/blast/executables/LATEST/
- Docs: http://www.ncbi.nlm.nih.gov/books/NBK52640/

