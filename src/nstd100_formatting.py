import vcf
import collections

"""
This program takes in a .vcf file and augments its INFO section with other fields
as needed for feature extraction. It also creates two files which are filtered to have only
healthy or diseased variant calls. 
"""

DISEASED_SAMPLE_IDS="../dbVarData/nstd100_sampleID.txt"
input_vcf_file = "../dbVarData/nstd100.vcf"
output_diseased_vcf_file = "../dbVarData/nstd100.diseased.vcf"
output_healthy_vcf_file = "../dbVarData/nstd100.healthy.vcf"

class DiseasedSampleID():
    def __init__(self, filename):
        """
        takes as argument |filename| and reads each line of the file.
        and puts each sample id in the set |self.sample_id_set| 
        REMEMBER: to remove the title string from the first line
        NOTE: the utilCode directory has code to do this for you. 
        IMP: the elements in the set are left as strings due to the format in .vcf file 
        """
        self.sample_id_set = set()
        with open(filename, 'r') as f:
            cnt = 0 
            for line in f:
                self.sample_id_set.add(line.strip())

def filter_and_augment_vcf(input_vcf_file,diseased,output_diseased_vcf_file, output_healthy_vcf_file):
    """
    takes as argument |input_vcf_file| , |diseased| object of DiseasedSampleID class, |output_diseased_vcf_file| and |output_healthy_vcf_file|
    get a Reader object for |input_vcf_file| and modify the 
    Reader.infos orderedDict to include any additional headers we want
    in the new |output_diseased_vcf_file|. 

    Info added:
    1.  vcf_reader.infos['copyNumber'] =
             _Info('copyNumber', 1, 'Integer', 'copy number taken from the .tab/.csv files and integrated into here', None, None)
    2. NOTE: none of the csv, tab files have this info, so WHEN MAKING FEATURES HAVE ONE FOR LENGTH from the start and end positions
    that coupled with the type of Structural Variation: Ins, DUP,INV .. etc should allow us to replace the copy number (i:e 0,1,2,3,4) 

    Filtering:
    1. use the |diseased| object to check if particular record is diseased or not. 
       second check is to look at 'SAMPLESET' key in record.info and if it exists ensure it is 1.
       if the sample ID is in the |diseased.sample_id_set| or 'SAMPLESET' == 1 then we accept. 

    Write all filtered records to |output_diseased_vcf_file|
    Write all other record to |output_healthy_vcf_file|
    """
    vcf_reader = vcf.Reader(open(input_vcf_file, 'r'))
    #modifying the infos dict to add new key in it. 
    _Info = collections.namedtuple('Info', ['id', 'num', 'type', 'desc', 'source', 'version'])
    vcf_reader.infos['copyNumber'] = _Info('copyNumber', 1, 'Integer', 'copy number taken from the .tab/.csv files and integrated into here', None, None)
    vcf_diseased_writer = vcf.Writer(open(output_diseased_vcf_file, 'w'), vcf_reader)
    vcf_healthy_writer = vcf.Writer(open(output_healthy_vcf_file, 'w'), vcf_reader)

    for record in vcf_reader:
        if ('SAMPLESET' in record.INFO and record.INFO['SAMPLESET'] == 1) or \
                ('SAMPLE' in record.INFO and record.INFO['SAMPLE'] in diseased.sample_id_set) :
                    vcf_diseased_writer.write_record(record)
        else:
            vcf_healthy_writer.write_record(record)

def main():
    diseased = DiseasedSampleID(DISEASED_SAMPLE_IDS)
    filter_and_augment_vcf(input_vcf_file,diseased, output_diseased_vcf_file, output_healthy_vcf_file)  
    print "set has %d elements" %(len(diseased.sample_id_set))


if __name__ == '__main__':
    main()
