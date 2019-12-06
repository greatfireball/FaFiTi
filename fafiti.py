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


dump = "data/nodes_dump.p"


def init():
    dt = datetime.now()
    if not os.path.isfile(dump):
        print("Initializing dump file: {}".format(dump))
        nodes_url = "ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdmp.zip"
        print("Downloading nodes.dmp from {}".format(nodes_url))
        response = urllib.request.urlopen(nodes_url).read()
        print("File read!")
        nodes_dict = {}
        with zipfile.ZipFile(io.BytesIO(response)) as nodes_zip_archive:
            nodes_file = nodes_zip_archive.read("nodes.dmp")
            for line in nodes_file.split(b"\n"):
                if line:
                    line = line.split(b'\t|\t')[0:2]
                    try:
                        nodes_dict[int(line[0])] = int(line[-1])
                    except ValueError:
                        print(line)
        print("Read {} Tax IDs".format(len(nodes_dict)))
        nodes_dict["timestamp"] = dt
        pickle.dump(nodes_dict,open(dump,"wb"))
        print("dump stored under {}".format(dump))
        return(nodes_dict)
    else:
        print("Already initialized! Doing nothing")

def filter(files, key, taxid):
    if not os.path.isfile(dump):
        nodes_dict = init()
    else: 
        nodes_dict = pickle.load(open(dump,"rb"))
    print("Loaded dumped file from {}".format(nodes_dict["timestamp"]))
    for fasta_file in files:
        pass


if __name__ == '__main__':
    args = docopt(__doc__, version='Fasta Filter By TaxID Version 0.1')
    print(args)
    if(args['init']):
        init()
    elif(args['filter']):
        filter(args["<file.fasta>"], args["<KEY>"], args["<TaxId>"])
