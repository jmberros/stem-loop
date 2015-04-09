# Stem-loop
An ever-growing collection of ruby scripts to deal with RNAs.

## Full pipeline
It's recommended that you run these commands in a new directory, since they will create several files and it might turn into a mess if the working directory is not empty. You can change the `--cpu=1` to howmuchever CPU cores you want to use.

The file `accession-codes` is a plain-text file with one accession code per line.

This will download, build and calibrate each RNA model:
```shell
$ cat accession-codes | download-stockholms.rb | cmbuild.rb | cmcalibrate --cpu=1
```
In order to just generate pbs-job-files but not calibrate them, you should run this:
```shell
$ cat accession-codes | download-stockholms.rb | cmbuild.rb | cmcalibrate-job --cpu=1
```
If you want to generate the job scripts AND enqueue them right away:
```shell
$ cat accession-codes | download-stockholms.rb | cmbuild.rb | cmcalibrate-enueque --cpu=1
```

## Detail of each script
### Download Stockholm files from Rfam, given accession codes in a text file
```shell
$ cat accession-codes | download-stockholms.rb
```

The file `accession-codes` is a plain-text file with one accession code per line. The script will search for the accession codes in Rfam online database and download the files in the working directory. It will also scan the stockholm for a `#GF ID` code, in order to give the file a meaningful name.

### Build covariance models from all Stockholm files in a directory
```shell
$ ls *.sto | cmbuild.rb
```
This script is meant to ease the process of building the covariance models from many stockholm files.

### Calibrate all covariance models in a directory
```shell
$ ls *.cm | cmcalibrate.rb --cpu=1
```
This process is time and CPU consuming. You should probably run it in a screen or tmux session.

### Generate PBS job scripts for the calibration of all covariance models in a directory
```shell
$ ls *.cm | cmcalibrate-job.rb --cpu=1 
```

### Generate PBS job scripts for calibration of all CM in this directory AND enqueue them right away
```shell
$ ls *.cm | cmcalibrate-enqueue.rb --cpu=1 
```

### Convert stockholm files to clustal format (for RNAz)
```shell
$ ls *.sto | sto-to-clustal.py
```

## Installation
- Clone this repo
```shell
$ git clone git@github.com:jmberros/stem-loop.git
```
- Add this repo's bin directory to $PATH
```
PATH=$PATH:$HOME/<path-to-stem-loop>/bin
```
That line goes in your shell config file, usually `~/.bashrc` or `~/.zshrc`.

You will also need:
* Ruby (check rbenv) and these ruby gems:
  * colorize
  * mustache
* Python 2.x
  * Numpy: `sudo apt-get install numpy`
  * (Biopython)[http://biopython.org/wiki/Download]
