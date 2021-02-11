#!/usr/bin/env python
#module load gatk/3.8.0
#module load bcftools

#try 12 hour job, actually took 1 hour
#try 2 hours for MX2

#only keep dominant variant as known mutation, do a BQSR
import glob
import os
from Bio import SeqIO

reffile = open('../ref/tag_020821')
refdict = {}
for line in reffile:
  line = line.rstrip().rsplit('\t')
  refdict[line[1]] = line[2]
reffile.close()

lendict = {}
for ref in list(set(refdict.values())):
  infile = open('../ref/'+ref+'.fasta')
  for record in SeqIO.parse(infile,'fasta'):
    lendict[ref] = len(record.seq)
  infile.close()

workpath = '/u/scratch/t/tianhao/NovaSeq020821/KSHV/'
for infile in sorted(glob.glob(workpath+'mapped/*.sam')):
  sample = infile.rsplit('/')[-1].rsplit('.sam')[0]
  ref = refdict[sample[4:]]
  shfile = open('shell_tmp/cns_'+sample+'.sh','w')
  #shfile.write('~/.local/bin/lofreq call -f ../ref/KSHV.fasta -o '+workpath+'analysis/'+sample+'_lofreq_round1.vcf '+workpath+'mapped/'+sample+'_sorted.bam\n')
  #shfile.write('java -jar /u/local/apps/gatk/3.8.0/GenomeAnalysisTK.jar -T BaseRecalibrator -R ../ref/KSHV.fasta -I '+workpath+'mapped/'+sample+'_sorted.bam -knownSites '+workpath+'analysis/'+sample+'_lofreq_round1.vcf -o '+workpath+'analysis/'+sample+'_recal_data.table\n')
  #shfile.write('java -jar /u/local/apps/gatk/3.8.0/GenomeAnalysisTK.jar -T PrintReads -R ../ref/KSHV.fasta -I '+workpath+'mapped/'+sample+'_sorted.bam -BQSR '+workpath+'analysis/'+sample+'_recal_data.table -o '+workpath+'mapped/'+sample+'.BQSR.bam\n')
  #second round lofreq calling with indels
  #shfile.write('~/.local/bin/lofreq call --call-indels -f ../ref/KSHV.fasta -o '+workpath+'analysis/'+sample+'_lofreq_round2.vcf '+workpath+'mapped/'+sample+'.BQSR.bam\n')
  #call consensus
  #remember to add contig to vcf file
  ##contig=<ID=MHV68_Mutant_X,length=121282>
  #remove all variants with less than 50% frequency
  infile = open(workpath+'analysis/'+sample+'_lofreq_round2.vcf')
  outfile = open(workpath+'analysis/'+sample+'_lofreq_round2_filtered.vcf','w')
  for line in infile:
    if '#' in line: 
      outfile.write(line)
      if 'reference' in line:
        outfile.write('##contig=<ID='+ref+',length='+str(lendict[ref])+'>\n')
    else:
      af = float(line.rsplit('AF=')[-1].rsplit(';')[0])
      if af > 0.5:
        outfile.write(line)
  infile.close()
  outfile.close()
  shfile.write('bcftools view -O z -o '+workpath+'analysis/'+sample+'_lofreq_round2_filtered.vcf.gz '+workpath+'analysis/'+sample+'_lofreq_round2_filtered.vcf\n')
  shfile.write('bcftools index '+workpath+'analysis/'+sample+'_lofreq_round2_filtered.vcf.gz\n')
  shfile.write('cat ../ref/'+ref+'.fasta | bcftools consensus '+workpath+'analysis/'+sample+'_lofreq_round2_filtered.vcf.gz > '+workpath+'analysis/'+sample+'_lofreq_cns.fasta\n')

  shfile.close()
  os.system('chmod 777 shell_tmp/cns_'+sample+'.sh')
  os.system('qsub -cwd -V -N PJ -l h_data=8G,h_rt=2:00:00 shell_tmp/cns_'+sample+'.sh')
  
