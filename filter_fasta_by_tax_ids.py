#!/usr/bin/env python3
"""Filter Fasta By Tax Ids
Usage:
  filter_fasta_by_tax_ids.py init
  filter_fasta_by_tax_ids.py filter TaxId <file.fasta>...
  filter_fasta_by_tax_ids.py -h | --help
  filter_fasta_by_tax_ids.py --version

Options:
  -h --help  Show this help.
  --version  Show version.

"""
#
#"""
from docopt import docopt

if __name__ == '__main__':
    args = docopt(__doc__, version='Filter Fasta By Tax Ids Version 0.1')
    print(args)
