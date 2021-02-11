#!/bin/bash
bowtie2-build ../ref/M3.fasta ../ref/M3
samtools faidx ../ref/M3.fasta
java -jar /u/local/apps/picard-tools/current/picard.jar CreateSequenceDictionary R=../ref/M3.fasta O=../ref/M3.dict
