# Kate Arendes - CS5320 - Project 4 - Population.py

from Chromosome import Chromosome
from Chromosome import CHROM_LENGTH
import random


class Population:
    def __init__(self, size, cap):
        self.size = size
        self.gen = 0
        self.cap = cap

        self.chromosomes = []
        self.fitnesses = []
        self.dist = []
        self.sampled = []
        self.crossed = []

        for i in range(self.size):
            self.chromosomes.append(Chromosome(self.cap))

    def print_pop(self):
        for i in range(self.size):
            self.chromosomes[i].print_chrom()
            print(self.chromosomes[i].get_value())

    def get_best(self):
        f_best = 0.0
        best_chrom = Chromosome(self.cap)
        best_chrom.bitstring = ""

        for i in range(CHROM_LENGTH):
            best_chrom.bitstring += "0"

        for i in range(self.size):
            if self.chromosomes[i].get_value() > f_best and self.chromosomes[i].is_valid():
                f_best = self.chromosomes[i].get_value()
                best_chrom = self.chromosomes[i]
        return best_chrom

    def penalty_static(self):
        for i in range(self.size):
            if self.chromosomes[i].is_valid():
                self.fitnesses.append(self.chromosomes[i].get_value())
            else:
                new_fitness = self.chromosomes[i].get_value() - (self.chromosomes[i].get_diff())
                if new_fitness <= 0:
                    new_fitness = 0.001
                self.fitnesses.append(new_fitness)

    def penalty_dynamic(self):
        for i in range(self.size):
            if self.chromosomes[i].is_valid():
                self.fitnesses.append(self.chromosomes[i].get_value())
            else:
                new_fitness = self.chromosomes[i].get_value() - (1 + 0.01 * self.gen) * (self.chromosomes[i].get_diff())
                if new_fitness <= 0:
                    new_fitness = 0.001
                self.fitnesses.append(new_fitness)

    def prop_selection(self):
        fit_sum = 0.0
        for i in range(self.size):
            fit_sum += self.fitnesses[i]

        prob_sum = 0.0
        for i in range(self.size):
            self.dist.append(prob_sum + (self.fitnesses[i] / fit_sum))
            prob_sum += self.fitnesses[i] / fit_sum

    def stoch_uni_sampling(self):
        point = random.uniform(0, 1)
        interval = 1.0 / self.size
        for i in range(self.size):
            current_point = (i * interval) + point
            if current_point > 1:
                current_point -= 1
            for j in range(self.size):
                if current_point < self.dist[j]:
                    new_chrom = Chromosome(self.cap)
                    new_chrom.chrom_copy(self.chromosomes[j])
                    self.sampled.append(new_chrom)
                    break
        self.chromosomes.clear()
        self.fitnesses.clear()
        self.dist.clear()

    def one_point_cross(self, prob_c):
        # Picks pairs of chromosomes and performs crossover

        iterations = int(self.size / 2)

        # When two chromosomes are picked, they are removed from the selected list

        for i in range(iterations):
            index1 = random.randint(0, (len(self.sampled) - 1))
            chrom1 = self.sampled[index1]
            del self.sampled[index1]

            index2 = random.randint(0, (len(self.sampled) - 1))
            chrom2 = self.sampled[index2]
            del self.sampled[index2]

            # Calculates whether crossover occurs and if so, performs the crossover using gene_swap()

            if random.uniform(0, 1) < prob_c:
                self.gene_swap(chrom1, chrom2)

            # Adds the crossed chromosomes back into the population's chromosome list

            self.crossed.append(chrom1)
            self.crossed.append(chrom2)

        # If there's an odd population size, the last chromosome is added to the list of chromosomes to be mutated

        if self.sampled:
            self.crossed.append(self.sampled[0])

    # gene_swap() performs a gene swap operation for two chromosomes starting at a randomized point

    def gene_swap(self, first_chrom, second_chrom):

        # Generate crossover point

        point = random.randint(1, len(first_chrom.bitstring) - 1)

        # Create resulting child bit strings

        child1 = (first_chrom.bitstring[0:point] + second_chrom.bitstring[point:])
        child2 = (second_chrom.bitstring[0:point] + first_chrom.bitstring[point:])

        # Replace parental bit strings with children's bit string

        first_chrom.bitstring = child1
        second_chrom.bitstring = child2

    def uni_cross(self):

        iterations = int(self.size / 2)

        for i in range(iterations):
            index1 = random.randint(0, (len(self.sampled) - 1))
            chrom1 = self.sampled[index1]
            del self.sampled[index1]

            index2 = random.randint(0, (len(self.sampled) - 1))
            chrom2 = self.sampled[index2]
            del self.sampled[index2]

            self.perform_uni_cross(chrom1, chrom2)

            self.crossed.append(chrom1)
            self.crossed.append(chrom2)

        if self.sampled:
            self.crossed.append(self.sampled[0])

    def perform_uni_cross(self, first_chrom, second_chrom):

        child1 = ""
        child2 = ""

        for i in range(len(first_chrom.bitstring)):
            prob = random.randint(0, 1)
            if prob == 0:
                child1 += first_chrom.bitstring[i]
                child2 += second_chrom.bitstring[i]
            else:
                child1 += second_chrom.bitstring[i]
                child2 += first_chrom.bitstring[i]

        first_chrom.bitstring = child1
        second_chrom.bitstring = child2


    def multi_parent_cross(self):

        for i in range(self.size):
            parents = []
            for j in range(3):
                index = random.randint(0, (len(self.sampled) - 1))
                parents.append(self.sampled[index])
            self.crossed.append(self.maj_vote(parents))
        self.sampled.clear()

    def maj_vote(self, chroms):

        child = Chromosome(self.cap)
        child.bitstring = ""

        for i in range(len(chroms[1].bitstring)):
            zeros = 0
            ones = 0
            for j in range(3):
                if chroms[j].bitstring[i] == "0":
                    zeros += 1
                else:
                    ones += 1
            if zeros > ones:
                child.bitstring += "0"
            else:
                child.bitstring += "1"

        return child


    def mutation(self, prob_m):
        for i in range(len(self.crossed)):
            self.crossed[i].mutate(prob_m)
            self.chromosomes.append(self.crossed[i])
        self.crossed.clear()
