#!/usr/bin/bash 

######
# this file divides up the generated bed files into a training and testing dataset. 
######

awk 'NR%2' ../nstd100.healthy.vcf.bed > ../nstd100.healthy.vcf.train.bed #selects all even lines 
awk 'NR%2 == 1' ../nstd100.healthy.vcf.bed > ../nstd100.healthy.vcf.test.bed #selects all odd lines 

awk 'NR%2' ../nstd100.diseased.vcf.bed > ../nstd100.diseased.vcf.train.bed #selects all even lines 
awk 'NR%2 == 1' ../nstd100.diseased.vcf.bed > ../nstd100.diseased.vcf.test.bed #selects all odd lines 

