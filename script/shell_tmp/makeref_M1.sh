#!/bin/bash
bowtie2-build ../ref/M1.fasta ../ref/M1
samtools faidx ../ref/M1.fasta
java -jar /u/local/apps/picard-tools/current/picard.jar CreateSequenceDictionary R=../ref/M1.fasta O=../ref/M1.dict
