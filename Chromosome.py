import random

CHROM_LENGTH = 20
WEIGHT = 200
WEIGHTS = [20, 20, 20, 20, 20, 20, 20, 20, 20, 20,
           20, 20, 20, 20, 20, 20, 20, 20, 20, 20]
VALUES = [20, 20, 20, 20, 20, 20, 20, 20, 20, 20,
            20, 20, 20, 20, 20, 20, 20, 20, 20, 20]


class Chromosome:

    def __init__(self):
        self.bitstring = ""
        for i in range(CHROM_LENGTH):
            self.bitstring += str(random.randint(0, 1))

    def get_weight(self):
        weight = 0
        for i in range(CHROM_LENGTH):
            if self.bitstring[i] == '1':
                weight += WEIGHTS[i]

        return weight

    def get_value(self):
        value = 0
        for i in range(CHROM_LENGTH):
            if self.bitstring[i] == '1':
                value += VALUES[i]

        return value

    def is_valid(self):
        if self.get_weight() > WEIGHT:
            return False
        else:
            return True

    def get_diff(self):
        return self.get_weight() - WEIGHT

    def mutate(self, prob_mutate):
        for i in range(CHROM_LENGTH):
            if random.uniform(0, 1) < prob_mutate:
                if self.bitstring[i] == '1':
                    edited_string = list(self.bitstring)
                    edited_string[i] = '0'
                    self.bitstring = ''.join(edited_string)
                else:
                    edited_string = list(self.bitstring)
                    edited_string[i] = '1'
                    self.bitstring = ''.join(edited_string)

    def print_chrom(self):
        print(self.bitstring)

    def chrom_copy(self, chromosome):
        self.bitstring = str(chromosome.bitstring)