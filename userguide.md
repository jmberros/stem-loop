## From an accesion codes list to the calibrated models

Create a new folder for you work and then save there a plain-text file with
the Rfam accession codes of the families you want to download.
Write one accession code per line. 

Supposing you named the file `accesion-codes`, this command will download the
stockholm alignments from Rfam, build the covariance models and enqueue a
calibration job for each model. You must run this in the server:

`cat accession-codes | download-stockholms.rb | cmbuild.rb | cmcalibrate-enqueue.rb --cpu=1`

You can modify the `--cpu=1` option to specify more cores for the calibration.

If you want to download the alignments and build the models, but you're not
interested in the calibration, you can remove the last part of the previous command:

`cat accession-codes | download-stockholms.rb | cmbuild.rb`

Simlarly, remove the `| cmbuild.rb` bit to download the alignments, but
not build the covariance models.

Finally, if you happen to want the calibration job files written, but not yet
enqueued, you can run this:

`cat accession-codes | download-stockholms.rb | cmbuild.rb | cmcalibrate-job --cpu=1`

Every new file is created in the working directory.

## From models and FASTAs to results in a csv

Once you have the covariance models calibrated (files ending in `c.cm`), copy
them to a new folder with the FASTAs you want to query. The wrapper command
`cmsearch.rb` (don't miss the `.rb` part!) will use each model in the directory
to perform a `cmsearch` in each FASTA (`.fa` or `.fna` fliles) it can find in
the same directory.

You can also add the `--max` flag like this: `cmsearch.rb --max`. According to
Infernal's man pages:

    --max  Turn off all filters, and run non-banded Inside on every full-length target sequence.  This  increases
           sensitivity somewhat, at an extremely large cost in speed.

So, after running one of these commands:

`cmsearch.rb`

or

`cmsearch.rb --max`

you will have the results written in a `.tbl` and a `.cmsearch-output` file
for each combination of model and target sequence in the directory. You don't
need to concatenate all the FASTAs in one big multiFASTA for this process.

You can then browse the results separately, or merge them in a CSV file with
the following command:

`cat *.tbl | grep ! | awk '{ s=""; for (i=1; i<=17; i++) s=s $i ","; print s }' > all-results.csv`

Explanation:

* `cat *.tbl` reads all the results tables and prints them to STDOUT. You can
  also run `cat some-file.tbl` to get the results of just one file in the CSV.
* `grep !` filters the hits above the inclusion threshold (marked with "!")
* `awk { ... }` reformats the hits: it selects the first 17 fields and prints them separated by commas
* `> all-results.csv` redirects the output to a CSV file. Name it however you like.

After running the command you should have a new CSV file that can be opened with Excel or Calc.
