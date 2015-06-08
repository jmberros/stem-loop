#! /usr/bin/env python3.4
# -*- coding: utf-8 -*-

import sys, os, argparse

bin_dir = os.path.dirname(os.path.realpath(__file__))
top_dir = os.path.dirname(bin_dir)
sys.path.append(top_dir)

from glob import glob
from lib.infernal import Infernal


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a cm database and index it")
    parser.add_argument("-o", "--output-file", help="Output results filename")
    options = vars(parser.parse_args())
    covariance_models = glob("*.c.cm")

    if len(covariance_models) == 0:
        print("No covariance models (*.c.cm) found in this directory!")
        sys.exit()
    else:
        output_file = Infernal().cmpress(
            covariance_models, options.get("output_file") or "minifam.cm"
        )
        print(output_file)
