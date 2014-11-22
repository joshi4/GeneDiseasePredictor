GeneDiseasePredictor
====================

Combined project for CS273A and CS221. 

### Steps

1. Split vcf data into diseased and healthy DONE
2. Convert each to a .bed file with all the data we need DONE (added a unique field ) 
3. Run a feature extractor on these bed files to get every feature we want IN PROGRESS (featureExtractor.py)
4. Split data into testing and training DONE 
5. Train
6. Test
7. Finish write-up

## TODO's 

* Ask sandeep for the ontology (MGI) inforomation
* Always predict healthy --> expect to get very good accuracy, run this for the poster session. 

## Nagging Questions 

* working with .vcf files and .bed files ? 

So for my logistic regression i'll work on a vcf-feature vector extractor while for overlap select, the files will have to be converted to .bed 
and then you need a feature extractor for the bed files. 

Similar to Info in .vcf i think there's a field in bed to which we can tack on random stuff

* confirm the meaning of same chrom,start,end but different nssv id ? 
* Ask Sandeep about overlap with coding exons right now we can say it overlapped with A coding exon, but we want to know which ones as well? 


### Notes

Here are some resources on understanding the .vcf file format, its pretty simple and should take about 30 minutes to get all of it down: 

* Looking at nstd100_formatting.py
* http://pyvcf.readthedocs.org/en/latest/INTRO.html online docs found here 
  * reading the intro and API section should be more than enough 
* Official pdf doucmentation: for some of the finer details http://samtools.github.io/hts-specs/VCFv4.1.pdf
* Download code for this here: https://github.com/jdoughertyii/PyVCF

* dbVarData/utilCode has the shell scritps to process data from the .vcf files
* The files of interest are nstd100.healthy.vcf and nstd100.diseased.vcf
* NOTE: the .vcf header should be present in all .vcf files. 

--------------------------------
