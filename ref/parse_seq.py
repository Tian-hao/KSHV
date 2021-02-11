#!/usr/bin/env python
import sys
from Bio import SeqIO

infile = open(sys.argv[1])
outfile = open(sys.argv[1].replace('0',''),'w')
for record in SeqIO.parse(infile,'fasta'):
  outfile.write(record.format('fasta'))
infile.close()
outfile.close()
