~/.local/bin/lofreq call -f ../ref/KSHV.fasta -o /u/scratch/t/tianhao/NovaSeq020821/KSHV/analysis/KSHV503702_lofreq_round1.vcf /u/scratch/t/tianhao/NovaSeq020821/KSHV/mapped/KSHV503702_sorted.bam
java -jar /u/local/apps/gatk/3.8.0/GenomeAnalysisTK.jar -T BaseRecalibrator -R ../ref/KSHV.fasta -I /u/scratch/t/tianhao/NovaSeq020821/KSHV/mapped/KSHV503702_sorted.bam -knownSites /u/scratch/t/tianhao/NovaSeq020821/KSHV/analysis/KSHV503702_lofreq_round1.vcf -o /u/scratch/t/tianhao/NovaSeq020821/KSHV/analysis/KSHV503702_recal_data.table
java -jar /u/local/apps/gatk/3.8.0/GenomeAnalysisTK.jar -T PrintReads -R ../ref/KSHV.fasta -I /u/scratch/t/tianhao/NovaSeq020821/KSHV/mapped/KSHV503702_sorted.bam -BQSR /u/scratch/t/tianhao/NovaSeq020821/KSHV/analysis/KSHV503702_recal_data.table -o /u/scratch/t/tianhao/NovaSeq020821/KSHV/mapped/KSHV503702.BQSR.bam
~/.local/bin/lofreq call --call-indels -f ../ref/KSHV.fasta -o /u/scratch/t/tianhao/NovaSeq020821/KSHV/analysis/KSHV503702_lofreq_round2.vcf /u/scratch/t/tianhao/NovaSeq020821/KSHV/mapped/KSHV503702.BQSR.bam
