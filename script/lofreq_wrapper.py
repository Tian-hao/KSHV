#!/usr/bin/env python
#module load gatk/3.8.0
#module load bcftools

#try 12 hour job, actually took 1 hour
#try 2 hours for MX2

#only keep dominant variant as known mutation, do a BQSR
import glob
import os

reffile = open('../ref/tag_020821')
refdict = {}
for line in reffile:
  line = line.rstrip().rsplit('\t')
  refdict[line[1]] = line[2]
reffile.close()

workpath = '/u/scratch/t/tianhao/NovaSeq020821/KSHV/'
for infile in sorted(glob.glob(workpath+'mapped/*.sam')):
  sample = infile.rsplit('/')[-1].rsplit('.sam')[0]
  ref = refdict[sample[4:]]
  shfile = open('shell_tmp/lofreq_'+sample+'.sh','w')
  shfile.write('~/.local/bin/lofreq call -f ../ref/'+ref+'.fasta -o '+workpath+'analysis/'+sample+'_lofreq_round1.vcf '+workpath+'mapped/'+sample+'_sorted.bam\n')
  shfile.write('java -jar /u/local/apps/gatk/3.8.0/GenomeAnalysisTK.jar -T BaseRecalibrator -R ../ref/'+ref+'.fasta -I '+workpath+'mapped/'+sample+'_sorted.bam -knownSites '+workpath+'analysis/'+sample+'_lofreq_round1.vcf -o '+workpath+'analysis/'+sample+'_recal_data.table\n')
  shfile.write('java -jar /u/local/apps/gatk/3.8.0/GenomeAnalysisTK.jar -T PrintReads -R ../ref/'+ref+'.fasta -I '+workpath+'mapped/'+sample+'_sorted.bam -BQSR '+workpath+'analysis/'+sample+'_recal_data.table -o '+workpath+'mapped/'+sample+'.BQSR.bam\n')
  #second round lofreq calling with indels
  shfile.write('~/.local/bin/lofreq call --call-indels -f ../ref/'+ref+'.fasta -o '+workpath+'analysis/'+sample+'_lofreq_round2.vcf '+workpath+'mapped/'+sample+'.BQSR.bam\n')
  #call consensus
  #remember to add contig to vcf file
  ##contig=<ID=MHV68_Mutant_X,length=121282>
  #remove all variants with less than 50% frequency
  #bcftools view -O z -o /u/scratch/t/tianhao/HiSeq080119/MHV_Mutant/MX2_S2_lofreq_round2.vcf.gz /u/scratch/t/tianhao/HiSeq080119/MHV_Mutant/MX2_S2_lofreq_round2.vcf
  #bcftools index /u/scratch/t/tianhao/HiSeq080119/MHV_Mutant/MX2_S2_lofreq_round2.vcf.gz
  #cat ../Ref/MHV_Mutant_X.fa | bcftools consensus /u/scratch/t/tianhao/HiSeq080119/MHV_Mutant/MX2_S2_lofreq_round2.vcf.gz > /u/scratch/t/tianhao/HiSeq080119/MHV_Mutant/MX2_S2_lofreq_cns.fasta

  shfile.close()
  os.system('chmod 777 shell_tmp/lofreq_'+sample+'.sh')
  os.system('qsub -cwd -V -N PJ -l h_data=8G,h_rt=2:00:00 shell_tmp/lofreq_'+sample+'.sh')
  
