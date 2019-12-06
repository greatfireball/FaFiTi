#!/usr/bin/env python3
"""Fasta Filter by TaxID
Usage:
  fafiti.py init
  fafiti.py filter --key <KEY> --id <TaxId> <file.fasta>...
  fafiti.py -h | --help
  fafiti.py --version

Options:
  -h --help  Show this help.
  --version  Show version.

"""
from docopt import docopt
import urllib.request
import io
import os.path
import zipfile
import pickle
from datetime import datetime
from Bio import SeqIO
import re
import sys


dump = "data/nodes_dump.p"


def init():
    dt = datetime.now()
    if not os.path.isfile(dump):
        print("Initializing dump file: {}".format(dump), file=sys.stderr)
        nodes_url = "ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdmp.zip"
        print("Downloading nodes.dmp from {}".format(nodes_url), file=sys.stderr)
        response = urllib.request.urlopen(nodes_url).read()
        print("File read!", file=sys.stderr)
        nodes_dict = {}
        with zipfile.ZipFile(io.BytesIO(response)) as nodes_zip_archive:
            nodes_file = nodes_zip_archive.read("nodes.dmp")
            for line in nodes_file.split(b"\n"):
                if line:
                    line = line.split(b'\t|\t')[0:2]
                    try:
                        nodes_dict[int(line[0])] = int(line[-1])
                    except ValueError:
                        print(line, file=sys.stderr)
        print("Read {} Tax IDs".format(len(nodes_dict)), file=sys.stderr)
        nodes_dict["timestamp"] = dt
        pickle.dump(nodes_dict,open(dump,"wb"))
        print("dump stored under {}".format(dump), file=sys.stderr)
        return(nodes_dict)
    else:
        print("Already initialized! Doing nothing", file=sys.stderr)

def filter(files, key, taxid):
    if not os.path.isfile(dump):
        nodes_dict = init()
    else: 
        nodes_dict = pickle.load(open(dump,"rb"))
    print("Loaded dumped file from {}".format(nodes_dict["timestamp"]), file=sys.stderr)
    tax_check = {}
    for fasta_file in files:
        for record in SeqIO.parse(open(fasta_file,"r"), format = "fasta"):
            tax = int(re.search("{}=(\d+)".format(key),record.description).group(1))
            if tax not in tax_check:
                current_tax = tax
                all_tax = []
                while( current_tax != taxid and current_tax != 1):
                    all_tax.append(current_tax)
                    current_tax = nodes_dict[current_tax]
                for t in all_tax:
                    if(current_tax == taxid):
                        tax_check[t] = True
                    else:
                        tax_check[t] = False
            if tax_check[tax]:
                SeqIO.write(record,sys.stdout,"fasta")
                    



if __name__ == '__main__':
    args = docopt(__doc__, version='Fasta Filter By TaxID Version 0.1')
    if(args['init']):
        init()
    elif(args['filter']):
        filter(args["<file.fasta>"], args["<KEY>"], int(args["<TaxId>"]))
