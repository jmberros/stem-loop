# Stem-loop
An ever-growing collection of ruby scripts to deal with RNAs.

<img src="https://github.com/jmberros/stem-loop/blob/master/stem-loop.png" width="350">

## Cheatguide

For starters, clone this repo, copy the scripts to a user-specific directory like `~/bin` and add that directory to your $PATH.

### Downloading Stockholm files from Rfam
```shell
$ download-stockholms.rb ACCESSION_CODE_1 ACCESSION_CODE_2 ACCESSION_CODE_3
```
This script will create a sub-directory named `stockholms/` in the current directory. Then it will procede to download the files there. It will also scan the Stockholm file for a `#GF ID` code, in order to give the file a meaningful name.
