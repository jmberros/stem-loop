# Stem-loop
An ever-growing collection of ruby scripts to deal with RNAs.

<img src="https://github.com/jmberros/stem-loop/blob/master/stem-loop.png" width="350">

## Cheatguide

For starters, clone this repo, copy the scripts to a user-specific directory like `~/bin` and add that directory to your $PATH.

### Full pipeline
It's recommended that you run these commands in a new directory, since they will create several files and it might turn into a mess if the working directory is not empty. You can change the `--cpu 6` to howmuchever CPU cores you want to use.
```shell
$ cat accession-codes | download-stockholms.rb && ls *.sto | cmbuild.rb && for i in $( ls *.cm ); do cmcalibrate --cpu 6 $i; done
```

### Download Stockholm files from Rfam
```shell
$ download-stockholms.rb <accession-code-1> [ <accession-code-2>, ... ]
```

The script will search for the accession codes in Rfam online database and download the files in the working directory. It will also scan the stockholm for a `#GF ID` code, in order to give the file a meaningful name.

You can feed it with STDIN:
```shell
$ cat accession-codes | download-stockholms.rb
```
Or (equivalent):
```
$ download-stockholms.rb < accession-codes
```

### Build covariance models from Stockholm files
```shell
$ cmbuild.rb <stockholm-filename>
```
This script is meant to ease the process of building and forecasting the calibration of many stockholm files in a single command. Given a directory full of stockholm files, you might do this:
```shell
$ cmbuild.rb $( ls *.sto )
```
You will get covariance models and calibration estimated times for each file.

### Calibrate the covariance models
```shell
$ cmcalibrate.rb $( ls *.cm )
```
Or:
```shell
$ ls *.cm | cmcalibrate.rb
```
This process is time and CPU consuming. You should probably run it in a screen or tmux session.
