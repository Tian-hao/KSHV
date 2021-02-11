#!/bin/bash
samtools view -b -F 4 /u/scratch/t/tianhao/NovaSeq020821/KSHV/mapped/KSHV2K.sam > /u/scratch/t/tianhao/NovaSeq020821/KSHV/mapped/KSHV2K_unsorted.bam
java -jar /u/local/apps/picard-tools/current/picard.jar AddOrReplaceReadGroups I=/u/scratch/t/tianhao/NovaSeq020821/KSHV/mapped/KSHV2K_unsorted.bam O=/u/scratch/t/tianhao/NovaSeq020821/KSHV/mapped/KSHV2K_rg.bam RGLB=lib2 RGPL=illumina RGPU=unit2 RGSM=S2
samtools sort -o /u/scratch/t/tianhao/NovaSeq020821/KSHV/mapped/KSHV2K_sorted.bam /u/scratch/t/tianhao/NovaSeq020821/KSHV/mapped/KSHV2K_rg.bam
samtools index /u/scratch/t/tianhao/NovaSeq020821/KSHV/mapped/KSHV2K_sorted.bam
java -jar /u/local/apps/gatk/3.8.0/GenomeAnalysisTK.jar -T DepthOfCoverage -R ~/KSHV/ref/M2.fasta -I /u/scratch/t/tianhao/NovaSeq020821/KSHV/mapped/KSHV2K_sorted.bam -o /u/scratch/t/tianhao/NovaSeq020821/KSHV/analysis/KSHV2K_depth.txt
