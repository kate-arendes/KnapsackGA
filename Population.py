from Chromosome import Chromosome
import random
import math

class Population:
    def __init__(self, size, gen):
        self.size = size

        self.chromosomes = []

        for i in range(self.size):
            self.chromosomes.append(Chromosome())
