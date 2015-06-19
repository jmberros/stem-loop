#! /usr/bin/env python3.4
# -*- coding: utf-8 -*-

import sys, os, argparse

bin_dir = os.path.dirname(os.path.realpath(__file__))
top_dir = os.path.dirname(bin_dir)
sys.path.append(top_dir)

from lib.cmscan_job_manager import CmscanJobManager


if __name__ == "__main__":
    description = "Scan all fastas in this dir with a CM database"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--fasta", help="Limit search to target fasta")
    parser.add_argument("--cpu", help="CPU cores to use (default=1)",
                        default=1, type=int)
    parser.add_argument("cm_database")
    options = vars(parser.parse_args())

    cmscan_manager = CmscanJobManager()
    job_script = cmscan_manager.write_job_script(
        options["cm_database"], options["fasta"], options["cpu"]
    )
    server_response = cmscan_manager.enqueue_job(job_script).decode("utf-8")\
                                                            .strip()
    print(server_response)
