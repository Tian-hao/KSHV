#!/usr/bin/env python
# use bowtie2 -local for MHV mapping
#Tian-hao used on 081719 for mapping part of DAPA reads, preparing for Pindel
#Adapted for KSHV genome
import os
import glob
import sys

def main():
  workpath = '/u/scratch/t/tianhao/NovaSeq020821/'
  tagdict = {}
  tagfile = open('../ref/tag_020821')
  for line in tagfile:
    line = line.rstrip().rsplit('\t')
    tagdict[line[0]] = [line[1],line[2]]
  tagfile.close()
  infiles = sorted(glob.glob(workpath+'data/lane1/*/'+'*_R1*'))
  for infile1 in infiles:
    print infile1
    tag = infile1.rsplit('/')[-1].rsplit('_')[0][-6:]
    print(tag)
    if tag not in tagdict: continue
    sample_name = 'KSHV'+tagdict[tag][0]
    ref = tagdict[tag][1]
    print sample_name
    infile2 = infile1.replace('_R1_001.fastq','_R2_001.fastq')
    outfile = workpath+'KSHV/mapped/'+sample_name+'.sam'
    bashfile = open('shell_tmp/bowtie_wrapper'+'_'+sample_name+'.sh','w')
    bashfile.write('#!/bin/bash\n')
    reffile = '../ref/'+ref
    bashfile.write('bowtie2 --very-sensitive-local -x '+reffile+' -1 '+infile1+' -2 '+infile2+' -S '+outfile)
    bashfile.close()
    os.system('chmod 777 shell_tmp/bowtie_wrapper'+'_'+sample_name+'.sh')
    os.system('qsub -cwd -V -N PJ -l h_data=6144M,h_rt=6:00:00 shell_tmp/bowtie_wrapper'+'_'+sample_name+'.sh')

if __name__ == '__main__':
  main()
