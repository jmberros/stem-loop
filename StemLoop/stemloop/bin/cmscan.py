#!/home/cquiroga/juan/opt/bin/python3.4
# -*- coding: utf-8 -*-

import sys, os, argparse

bin_dir = os.path.dirname(os.path.realpath(__file__))
top_dir = os.path.dirname(bin_dir)
sys.path.append(top_dir)

from lib.infernal import Infernal


if __name__ == "__main__":
    description = "Scan all fastas in this dir with a CM database"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("cm_database")
    parser.add_argument("--fasta", help="Limit search to target fasta")
    parser.add_argument("--cpu", help="CPU cores to use (default=1)",
                        default=1, type=int)
    options = vars(parser.parse_args())

    Infernal().cmscan(
        options["cm_database"], options["fasta"], options["cpu"]
    )
