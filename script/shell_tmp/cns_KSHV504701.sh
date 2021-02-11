bcftools view -O z -o /u/scratch/t/tianhao/NovaSeq020821/KSHV/analysis/KSHV504701_lofreq_round2_filtered.vcf.gz /u/scratch/t/tianhao/NovaSeq020821/KSHV/analysis/KSHV504701_lofreq_round2_filtered.vcf
bcftools index /u/scratch/t/tianhao/NovaSeq020821/KSHV/analysis/KSHV504701_lofreq_round2_filtered.vcf.gz
cat ../ref/KSHV.fasta | bcftools consensus /u/scratch/t/tianhao/NovaSeq020821/KSHV/analysis/KSHV504701_lofreq_round2_filtered.vcf.gz > /u/scratch/t/tianhao/NovaSeq020821/KSHV/analysis/KSHV504701_lofreq_cns.fasta
