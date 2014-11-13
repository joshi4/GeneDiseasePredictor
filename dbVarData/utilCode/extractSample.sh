#!/usr/bin/bash
#I've downloaded the samples for the first sampleset for nstd100
# this is cause in the vcf file, in the INFO field, we sometimes have sampleID or SampleSet
#we are interested in all cases where SampleSet = 1 or the sampleID belongs to one specified in the file here
# samples_for_nstd100_1.csv

#We are interested in the third column and we perform some of the cleanup here as well. 

cat ../samples_for_nstd100_1.csv | cut -d',' -f3 > tmp.txt #../nstd100_sampleID.txt
sed '1d' tmp.txt > tmp2.txt # removing the tile line 
sed 's/\"//g' tmp2.txt > ../nstd100_sampleID.txt
rm tmp.txt tmp2.txt



