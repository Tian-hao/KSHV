#!/bin/bash
bowtie2-build ../ref/M2.fasta ../ref/M2
samtools faidx ../ref/M2.fasta
java -jar /u/local/apps/picard-tools/current/picard.jar CreateSequenceDictionary R=../ref/M2.fasta O=../ref/M2.dict
