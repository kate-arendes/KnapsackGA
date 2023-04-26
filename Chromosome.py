import random

CHROM_LENGTH = 20
CAPACITY = 65
WEIGHTS = [8.599796663725433, 7.821589626462722, 4.7851442274776055, 3.3302507526366703, 5.601472492317477,
           4.644407237053729, 8.054187301312954, 3.7298145347103473, 5.2893725873712025, 6.250438355095281,
           9.173015966758017, 5.542181702356512, 3.5365405995973345, 7.802237837415015, 6.565320970077985,
           3.254557072261965, 9.187716303714161, 9.845069284338878, 8.291955123969306, 9.119493553956245]

VALUES = [13.599796663725433, 12.821589626462721, 9.785144227477605, 8.33025075263667, 10.601472492317477,
          9.644407237053729, 13.054187301312954, 8.729814534710346, 10.289372587371203, 11.25043835509528,
          14.173015966758017, 10.542181702356512, 8.536540599597334, 12.802237837415015, 11.565320970077984,
          8.254557072261965, 14.187716303714161, 14.845069284338878, 13.291955123969306, 14.119493553956245]


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
        if self.get_weight() > CAPACITY:
            return False
        else:
            return True

    def get_diff(self):
        return self.get_weight() - CAPACITY

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