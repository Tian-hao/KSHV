#!/usr/bin/env python
#samtools
#bowtie2
#gatk
from Bio import SeqIO
import os
from Bio.Seq import Seq

reffile = open('../ref/KSHV.fasta')
for record in SeqIO.parse(reffile,'fasta'):
  refseq = str(record.seq)
mutfile = open('../ref/KCP.fasta')
for record in SeqIO.parse(mutfile,'fasta'):
  mutid = str(record.id)
  mutseq = str(record.seq)
  start = refseq.find(mutseq[:30])
  end = refseq.find(mutseq[-30:])+30
  print(start,end)
  outfile = open('../ref/'+mutid+'.fasta','w')
  record.seq = Seq(refseq[:start]+mutseq+refseq[end:]) 
  outfile.write(record.format('fasta'))
  outfile.close()
  shfile = open('shell_tmp/makeref_'+mutid+'.sh','w')
  shfile.write('#!/bin/bash\n')
  shfile.write('bowtie2-build ../ref/'+mutid+'.fasta ../ref/'+mutid+'\n')
  shfile.write('samtools faidx ../ref/'+mutid+'.fasta\n')
  shfile.write('java -jar /u/local/apps/picard-tools/current/picard.jar CreateSequenceDictionary R=../ref/'+mutid+'.fasta O=../ref/'+mutid+'.dict\n')
  shfile.close()
  os.system('chmod 777 shell_tmp/makeref_'+mutid+'.sh')
  #os.system('qsub -cwd -V -N PJ -l h_data=2G,h_rt=0:30:00 shell_tmp/makeref_'+mutid+'.sh')
