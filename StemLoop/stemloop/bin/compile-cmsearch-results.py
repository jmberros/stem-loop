#!/usr/bin/env python3.4

import os, sys, argparse

bin_dir = os.path.dirname(os.path.realpath(__file__))
top_dir = os.path.dirname(bin_dir)
sys.path.append(top_dir)

from lib.infernaloutput import InfernalOutputParser


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Compile cmsearch result CSV")
    parser.add_argument('hits_csv')
    parser.add_argument('--accessory-csv',
                        help="accesory CSV with coordinates")
    options = vars(parser.parse_args())

    InfernalOutputParser().parse_results_from_files(options['hits_csv'],
                                                    options['accessory_csv'])
