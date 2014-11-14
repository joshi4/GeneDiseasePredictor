import vcf
import collections

"""
This file converts .vcf files to .bed files, so we can then run them through the feature extractor
each output .bed line contains:

chrom 	start	end 	name

We use the name column to tack on all the data here: svtype;uniqueID

This should be all the information we need for our feature extractor
"""

#original_vcf_file = "../dbVarData/nstd100.vcf"
input_diseased_vcf_file = "../dbVarData/nstd100.diseased.vcf"
input_healthy_vcf_file = "../dbVarData/nstd100.healthy.vcf"
files_to_convert = [input_diseased_vcf_file, input_healthy_vcf_file]

for file in files_to_convert:
	f_out = open(file+".bed", 'w')
	vcf_reader = vcf.Reader(open(file, 'r'))
	for record in vcf_reader:
		chrom = record.CHROM
		start = record.POS
		end = record.INFO["END"]
		svtype = record.INFO["SVTYPE"]
        unique_id = record.ID
		f_out.write("chrom%s\t%s\t%s\t%s;%s\n" % (chrom, start, end, svtype,unique_id))
	f_out.close()