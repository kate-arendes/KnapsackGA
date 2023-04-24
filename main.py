from Chromosome import Chromosome

if __name__ == '__main__':
    chrom = Chromosome()
    print(chrom.bitstring)
    print(chrom.get_weight())
    print(chrom.get_value())
    print(chrom.get_diff())
    print(chrom.is_valid())
