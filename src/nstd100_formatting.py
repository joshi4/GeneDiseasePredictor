"""
This program takes in a .vcf file and augments its INFO section with other fields
as needed for feature extraction. 

"""

DISEASED_SAMPLE_IDS="../dbVarData/nstd100_sampleID.txt"

class DiseasedSampleID():
    def __init__(self, filename):
        """
        takes as argument |filename| and reads each line of the file.
        convert the strings to int and put them in the set |self.sample_id_set| 
        REMEMBER: to remove the title string from the first line
        NOTE: the utilCode director has code to do this for you. 
        """
        self.sample_id_set = set()
        with open(filename, 'r') as f:
            cnt = 0 
            for line in f:
                self.sample_id_set.add(int(line.strip()))


def main():
    diseased = DiseasedSampleID(DISEASED_SAMPLE_IDS)
    print "set has %d elements" %(len(diseased.sample_id_set))


if __name__ == '__main__':
    main()
        
