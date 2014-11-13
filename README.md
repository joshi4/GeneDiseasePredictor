GeneDiseasePredictor
====================

Combined project for CS273A and CS221. 

Here are some resources on understanding the .vcf file format, its pretty simple and should take about 30 minutes to get all of it down: 

* Looking at nstd100_formatting.py
* http://pyvcf.readthedocs.org/en/latest/INTRO.html online docs found here 
  * reading the intro and API section should be more than enough 
* Official pdf doucmentation: for some of the finer details http://samtools.github.io/hts-specs/VCFv4.1.pdf

* dbVarData/utilCode has the shell scritps to process data from the .vcf files
* The files of interest are nstd100.healthy.vcf and nstd100.diseased.vcf
* To construct our training and test sets, I propose we take every alternate line from the above two files and create a training and test dataset. 
* NOTE: the .vcf header should be present in all the files. 
* Being able to do that should be a good way to become familiar with .vcf 
* I've mentioned this in the code as well, but the study we are using, nstd100 does not explicitly mention the copy number instead, it gives us the type of the structural variation and start and end points. Given the type and length of the variation we should have enough info to approximate the copy number I feel. 

--------------------------------

## TODO's 

## Nagging Questions 

* working with .vcf files and .bed files ? 
