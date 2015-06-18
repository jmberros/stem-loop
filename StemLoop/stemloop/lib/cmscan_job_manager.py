#!/usr/bin/env python.4
#-*- coding: utf-8 -*-

import subprocess
import pystache
import os

from .infernal import Infernal


class CmscanJobManager:
    def __init__(self):
        self.template_path = os.path.join(os.path.dirname(__file__),
                                          "../templates/cmscan-job.mustache")
        self.default_options = {
            "cmscan_path": subprocess.check_output(["which", "cmscan.py"])
                                     .decode("utf-8").strip(),
            "queue_name": "default",
            "nodes": 1,
            "cores": 1
        }

    def write_job_script(self, database, fasta, cores=1):
        """Write a job script for the cmscan enqueue"""

        job_filename = Infernal.pretty_filename_for_search(database, fasta) + \
                       ".cmscan-job"
        job_options = self.default_options.copy()
        job_options.update({
            "cores": cores,
            "job_name": "Search for {} in {}".format(database, fasta),
            "database": database,
            "fasta": fasta,
        })

        with open(job_filename, "w+") as job_file, \
                open(self.template_path, "r") as template:
            job_file.write(pystache.render(template.read(), job_options))

        return job_filename

    def enqueue_job(self, job_filename):
        """Enqueue the job in the given path"""

        if not os.path.isfile(job_filename):
            sys.exit("'{}' doesn't exist".format(job_filename))

        print("⌛ Enqueue the cmscan job:\n{}".format(" ".join(["qsub", job_filename])))
        server_response = subprocess.check_output(["qsub", job_filename])

        return server_response


