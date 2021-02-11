#!/usr/bin/env python
#GATK
#samtools
import os
import glob

reffile = open('../ref/tag_020821')
refdict = {}
for line in reffile:
  line = line.rstrip().rsplit('\t')
  refdict[line[1]] = line[2]
reffile.close()
workpath = '/u/scratch/t/tianhao/NovaSeq020821/KSHV/'
for infile in sorted(glob.glob(workpath+'mapped/KSHV*.sam')):
  sample = infile.rsplit('/')[-1].rsplit('.sam')[0]
  ref = refdict[sample[4:]]
  shfile = open('shell_tmp/depth_'+sample+'.sh','w')
  shfile.write('#!/bin/bash\n')
  shfile.write('samtools view -b -F 4 '+infile+' > '+workpath+'mapped/'+sample+'_unsorted.bam\n')
  shfile.write('java -jar /u/local/apps/picard-tools/current/picard.jar AddOrReplaceReadGroups I='+workpath+'mapped/'+sample+'_unsorted.bam O='+workpath+'mapped/'+sample+'_rg.bam RGLB=lib2 RGPL=illumina RGPU=unit2 RGSM=S2\n')
  shfile.write('samtools sort -o '+workpath+'mapped/'+sample+'_sorted.bam '+workpath+'mapped/'+sample+'_rg.bam\n')
  shfile.write('samtools index '+workpath+'mapped/'+sample+'_sorted.bam\n')
  shfile.write('java -jar /u/local/apps/gatk/3.8.0/GenomeAnalysisTK.jar -T DepthOfCoverage -R ~/KSHV/ref/'+ref+'.fasta -I '+workpath+'mapped/'+sample+'_sorted.bam -o '+workpath+'analysis/'+sample+'_depth.txt\n')
  shfile.close()
  os.system('chmod 777 shell_tmp/depth_'+sample+'.sh')
  os.system('qsub -cwd -V -N PJ -l h_data=6144M,h_rt=6:00:00 shell_tmp/depth_'+sample+'.sh') 
