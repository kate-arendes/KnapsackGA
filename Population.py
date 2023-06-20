# Kate Arendes - Population.py
# This file contains the Population class used to simulate and manage a collection of chromosomes

from Chromosome import Chromosome
from Chromosome import CHROM_LENGTH
import random


# The Population class takes a size for the number of chromosomes to generate and capacity as a problem parameter

class Population:

    # Initialized the population with a given number of chromosomes

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

    # get_best() returns the best valid solution in the population

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

    # penalty_static() recalculates fitness values of invalid solutions using a constant penalty calculation scheme

    def penalty_static(self):

        # If solutions are valid, their fitness is unchanged. Otherwise, they are penalized

        for i in range(self.size):
            if self.chromosomes[i].is_valid():
                self.fitnesses.append(self.chromosomes[i].get_value())
            else:

                # The difference between the solution's weight and the capacity is subtracted from the value

                new_fitness = self.chromosomes[i].get_value() - (self.chromosomes[i].get_diff())

                # Prevents divide-by-zero errors

                if new_fitness <= 0:
                    new_fitness = 0.001
                self.fitnesses.append(new_fitness)

    # penalty_dynamic() recalculates fitness values of invalid solutions using a penalty scheme based on the generation

    def penalty_dynamic(self):

        # If solutions are valid, their fitness is unchanged. Otherwise, they are penalized

        for i in range(self.size):
            if self.chromosomes[i].is_valid():
                self.fitnesses.append(self.chromosomes[i].get_value())
            else:

                # The penalty increases with each subsequent generation, progressively prioritizing valid solutions

                new_fitness = self.chromosomes[i].get_value() - (1 + 0.6 * self.gen) * (self.chromosomes[i].get_diff())

                # Prevents divide-by-zero errors

                if new_fitness <= 0:
                    new_fitness = 0.001
                self.fitnesses.append(new_fitness)

    # prop_selection() generates a distribution on which sampling can be performed

    def prop_selection(self):

        # Sums up the fitnesses

        fit_sum = 0.0
        for i in range(self.size):
            fit_sum += self.fitnesses[i]

        # Creates the distribution

        prob_sum = 0.0
        for i in range(self.size):
            self.dist.append(prob_sum + (self.fitnesses[i] / fit_sum))
            prob_sum += self.fitnesses[i] / fit_sum

    # stoch_uni_sampling() performs stochastic universal sampling on the distribution

    def stoch_uni_sampling(self):

        # Generates an initial point and calculates the intervals for the others

        point = random.uniform(0, 1)
        interval = 1.0 / self.size

        # Samples the chromosomes from the distribution based on the generated points

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

        # Clears the lists for the next generation

        self.chromosomes.clear()
        self.fitnesses.clear()
        self.dist.clear()

    # one_point_cross performs single-point crossover on the sampled chromosomes

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

        # Generates crossover point

        point = random.randint(1, len(first_chrom.bitstring) - 1)

        # Creates resulting child bit strings

        child1 = (first_chrom.bitstring[0:point] + second_chrom.bitstring[point:])
        child2 = (second_chrom.bitstring[0:point] + first_chrom.bitstring[point:])

        # Replaces parental bit strings with children's bit string

        first_chrom.bitstring = child1
        second_chrom.bitstring = child2

    # uni_cross() performs 0.5-uniform crossover on the sampled chromosomes

    def uni_cross(self):

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

            # On each pair, 0.5-uniform crossover is performed

            self.perform_uni_cross(chrom1, chrom2)

            # The crossed chromosomes are saved for mutation

            self.crossed.append(chrom1)
            self.crossed.append(chrom2)

        # Handles scenario in which there may be an odd number of chromosomes

        if self.sampled:
            self.crossed.append(self.sampled[0])

    # perform_uni_cross() takes two chromosomes and performs 0.5-uniform crossover on them

    def perform_uni_cross(self, first_chrom, second_chrom):

        # Creates two new bit strings for the children

        child1 = ""
        child2 = ""

        # Randomly determines which parent will donate bits to each child

        for i in range(len(first_chrom.bitstring)):
            prob = random.randint(0, 1)
            if prob == 0:
                child1 += first_chrom.bitstring[i]
                child2 += second_chrom.bitstring[i]
            else:
                child1 += second_chrom.bitstring[i]
                child2 += first_chrom.bitstring[i]

        # Assigns children's bit strings to the parent chromosomes

        first_chrom.bitstring = child1
        second_chrom.bitstring = child2

    # multi_parent_cross() randomly picks three parents to create each child

    def multi_parent_cross(self):

        # Picks three parents and performs majority voting to create a new child

        for i in range(self.size):
            parents = []
            for j in range(3):
                index = random.randint(0, (len(self.sampled) - 1))
                parents.append(self.sampled[index])
            self.crossed.append(self.maj_vote(parents))

        # Clears the sampled list for the next generation

        self.sampled.clear()

    # maj_vote takes a list of parents and does majority voting to generate their child

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

    # mutation() goes through the list of crossed chromosomes and performs mutation

    def mutation(self, prob_m):

        # Performs mutation and places the resulting chromosomes in the chromosomes list

        for i in range(len(self.crossed)):
            self.crossed[i].mutate(prob_m)
            self.chromosomes.append(self.crossed[i])

        # Clears the list of crossed chromosomes

        self.crossed.clear()

        # Since mutation occurs last, increments the population's generation

        self.gen += 1
