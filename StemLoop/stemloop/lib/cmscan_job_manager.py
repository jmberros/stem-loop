from Infernal import cmscan_pretty_filename
import subprocess


class CmscanJobManager:
    def __init__(self):
        self.template_path = "templates/cmscan-job.mustache"
        self.default_options = {
            "cmscan_path": subprocess.check_output(["which", "cmscan.py"])
                                     .decode("utf-8").strip(),
            "queue_name": "default",
            "nodes": 1,
            "cores": 1
        }

    def write_job_script(self, database, fasta, cores=1):
        """Write a job script for the cmscan enqueue"""

        job_filename = cmscan_pretty_filename(database, fasta) + ".cmscan-job"
        options = self.default_options.update({
            "cores": cores,
            "job_name": job_filename,
            "database": database,
            "fasta": fasta,
            "output_filename": job_filename + ".output",
            "error_filename": job_filename + ".errors"
        })

    def enqueue_job(self, job_script_path):
        """Enqueue the job in the given path"""
        pass


