#! /usr/bin/env python3.4
# -*- coding: utf-8 -*-

import sys, os, argparse
import fileinput

bin_dir = os.path.dirname(os.path.realpath(__file__))
top_dir = os.path.dirname(bin_dir)
sys.path.append(top_dir)

from lib.infernal import Infernal


if __name__ == "__main__":
    if sys.stdin.isatty():
        parser = argparse.ArgumentParser(description="Scan all fastas in this dir "\
                                                    "with a given model database")
        parser.add_argument("cm_database")
        options = vars(parser.parse_args())

        Infernal().cmscan(options["cm_database"]) 
    else:
        for line in fileinput.input():
            filename = line.strip()
            if len(filename) > 0:
                Infernal().cmscan(filename)
