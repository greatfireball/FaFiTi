#!/usr/bin/env python3
"""Fasta Filter by TaxID
Usage:
  fafiti.py init
  fafiti.py filter TaxId <file.fasta>...
  fafiti.py -h | --help
  fafiti.py --version

Options:
  -h --help  Show this help.
  --version  Show version.

"""
#
#"""
from docopt import docopt

if __name__ == '__main__':
    args = docopt(__doc__, version='Fasta Filter By TaxID Version 0.1')
    print(args)
