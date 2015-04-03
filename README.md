# Stem-loop
An ever-growing collection of ruby scripts to deal with RNAs.

<img src="https://github.com/jmberros/stem-loop/blob/master/stem-loop.png" width="350">

## Cheatguide

For starters, clone this repo, copy the scripts to a user-specific directory like `~/bin` and add that directory to your $PATH.

### Download Stockholm files from Rfam
```shell
$ download-stockholms.rb <accession-code-1> [ <accession-code-2>, ... ]
```
This script will create a sub-directory named `stockholms/` in the current directory. Then it will procede to download the files there. It will also scan the Stockholm file for a `#GF ID` code, in order to give the file a meaningful name.

### Build covariance models from Stockholm files
```shell
$ cmbuild.rb <stockholm-filename>
```
This script is meant to ease the process of building and forecasting the calibration of many stockholm files in a single command. Given a directory full of stockholm files, you might do this:
```shell
$ cmbuild.rb $( ls *.sto )
```
You will get covariance models and calibration estimated times for each file.
