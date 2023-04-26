from Chromosome import Chromosome
from Chromosome import CHROM_LENGTH
from Population import Population
import random
import statistics

RUNS = 30


def evolve(members, generations, cross_prob, mut_prob, pen_type, cross_type):
    pop = Population(members)

    best_solution = pop.get_best()
    best_fit = pop.get_best().get_value()

    for i in range(generations):
        if pen_type == 1:
            pop.penalty_static()
        else:
            pop.penalty_dynamic()

        pop.prop_selection()
        pop.stoch_uni_sampling()

        if cross_type == 1:
            pop.one_point_cross(cross_prob)
        elif cross_type == 2:
            pop.uni_cross()
        else:
            pop.multi_parent_cross()

        pop.mutation(mut_prob)

        if pop.get_best().get_value() > best_fit:
            best_solution = pop.get_best()
            best_fit = pop.get_best().get_value()

    return best_solution


if __name__ == '__main__':

    # Prompts the user for penalty type and crossover type

    print("\n1. Static Penalty\n2. Dynamic Penalty\n\nPlease select a type of penalty:\n")
    p_type = int(input("Penalty type: "))

    print("\n1. One-Point\n2. 0.5 Uniform\n3. Multi-Parent (Majority Voting)\n\nPlease select a type of penalty:\n")
    c_type = int(input("Crossover type: "))

    print("\nRunning the genetic algorithm . . .\n")

    # Collects the best solution from each run and its fitness value

    best_solutions = []
    best_f_vals = []

    # Tracks the best solution over all independent runs

    overall_f_best = 0
    overall_best_chrom = Chromosome()
    overall_best_chrom.bitstring = ""
    for i in range(CHROM_LENGTH):
        overall_best_chrom.bitstring += "0"

    # Conducts independent runs

    for j in range(RUNS):

        # Seeds random so that results are reproducible

        random.seed(j)

        # Adds the best solution to the running list

        best_solutions.append(evolve(30, 50, 0.7, 0.05, p_type, c_type))
        best_f_vals.append(best_solutions[j].get_value())

        # Determines if the best solution is the overall best

        if best_solutions[j].get_value() > overall_f_best:
            overall_best_chrom = best_solutions[j]
            overall_f_best = best_solutions[j].get_value()

    # Prints all the results from the independent runs

    print("\n============ Results from Thirty Independent Runs ============\n")
    print("Overall Best Fitness Value: " + str('{:.20f}'.format(overall_f_best)))
    print("Mean of Best Fitness Values: " + str('{:.20f}'.format(statistics.mean(best_f_vals))))
    print("Stdev of Best Fitness Values: " + str('{:.20f}'.format(statistics.stdev(best_f_vals))))

    print("\n\n==================== Best Overall Solution ====================\n")
    print("Bit-String Chromosome:\n" + overall_best_chrom.bitstring)
    print("\nWeight of Items:\n" + str('{:.20f}'.format(overall_best_chrom.get_weight())))
    print("\nValue of Items:\n" + str('{:.20f}'.format(overall_f_best)))
    print()
