import sys
import os
# this program take a command line arg which is the path to 
# to the file which needs to be converted into a bed file
# output is a bed file

#header of importance: 
#chr,start,stop,copy_number,strand,phenotype,variant_call_type

#global dictionary to convert
#header in the .submitted.tab file 

headingToIndex = {
    "variant_call_accession": 1,
    "variant_call_id": 2,
    "variant_call_type": 3,
    "experiment_id": 4,
    "sample_id": 5,
    "sampleset_id": 6,
    "assembly": 7,
    "chr": 8,
    "contig": 9,
    "outer_start": 10,
    "start": 11,
    "inner_start": 12,
    "inner_stop": 13,
    "stop": 14,
    "outer_stop": 15,
    "variant_call_length": 16,
    "variant_region_acc": 17,
    "variant_region_id": 18,
    "copy_number": 19,
    "ref_copy_number": 20,
    "description": 21,
    "validation": 22,
    "zygosity": 23,
    "origin ": 24,
    "phenotype": 25,
    "hgvs_name": 26,
    "strand": 27,
    "cytoband": 28,
    "taxonomy_id": 29,
    "alt_status": 30,
    "external_links ": 31,
    "evidence": 32,
    "sequence": 33,
    "support": 34,
    "support_count": 35,
    "log2_values": 36,
    "5'_outer_flank": 37,
    "5'_inner_flank": 38,
    "3'_inner_flank": 39,
    "3'_outer_flank": 40,
    "placement_method": 41,
    "loss_of_heterozygosity": 42
    #"is_low_quality": 43,
    #"remap_coverage": 44,
    #"assembly_unit": 45,
    #"remap_alignment": 46,
    #"breakpoint_order": 47
    }
    

def main():
    fileName = sys.argv[1]
    bedFileName = fileName + ".bed"
    #open bed file 
    fbed = open(bedFileName, 'w')
    with open(fileName) as f:
        counter = 0 #to not include the first two lines
        for line in f:

            if counter < 2:
                counter +=1
                continue 

            #extract relevant bed features from the line
            contents = line.strip().split('\t')
            fbed.write(dbVarLineTobedLine(contents))

    fbed.close()
    #now run uniq on the created bed file
    #os.system("uniq " + bedFileName+" >" + bedFileName) 
    return 

def dbVarLineTobedLine(dbVarLine):
    """
    takes input |dbVarLine| a list of strings obtained from 
    separating on the tab delimiter.
    outputs a string |bedString| which is then appended to the bed file
    format of bed file is :
    chrXX\tchromStart\tChromEnd\tname(here variant_call_type)\t
    score(here copy_number)\tstrand
    """
    bedList = [] 
    #chr,start,stop,copy_number,strand,phenotype,variant_call_type
    headers = ["chr", "inner_start", "inner_stop",
            "variant_call_type","copy_number", "strand"] 
    for header in headers:
        bedList.append(dbVarLine[headingToIndex[header] -1 ])
    bedList[0] = "chr" + bedList[0] # append chr to the chr number

    bedString =  '\t'.join(bedList) + "\n"
    return bedString 


if __name__ == '__main__':
    main() 

