#!/usr/bin/python3.4

import argparse

# This should be done better
import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                             os.pardir))

from infernal import InfernalOutputParser


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Compile cmsearch result CSV")
    parser.add_argument('hits_csv')
    parser.add_argument('--accessory-csv',
                        help="accesory CSV with coordinates")
    options = vars(parser.parse_args())

    InfernalOutputParser().parse_results_from_files(options['hits_csv'],
                                                    options['accessory_csv'])
