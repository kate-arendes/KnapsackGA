# Kate Arendes - CS 5320 - Project 4 - main.py
# This program uses a GA to solve the 0-1 Knapsack Problem with various capacities

from Chromosome import Chromosome
from Chromosome import CHROM_LENGTH
from Chromosome import WEIGHTS
from Chromosome import VALUES
from Population import Population
import random
import statistics

RUNS = 30  # Number of times algorithm executes per problem instance

# CAPACITIES stores the capacities of two extreme cases and one regular case of the 0-1 Knapsack Problem

CAPACITIES = [0, 65.21228109630442, 130.42456219260885]


# evolve() takes problem parameters as well as a user's choice of penalty and crossover policies to perform the GA

def evolve(members, generations, capacity, cross_prob, mut_prob, pen_type, cross_type):

    # Instantiates population and best solution, which the function returns

    pop = Population(members, capacity)

    best_solution = pop.get_best()
    best_fit = pop.get_best().get_value()

    # Performs the steps of the GA based on the penalty and crossover types the user selected

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

        # Updates best solution

        if pop.get_best().get_value() > best_fit:
            best_solution = pop.get_best()
            best_fit = pop.get_best().get_value()

    # Returns the best solution found over all generations

    return best_solution


# run_algo() takes a penalty type and crossover type from the user and calls evolve() for three problem instances

def run_algo(penalty, cross):

    # Prints weights and values for all items. Only capacities change between instances to demonstrate extreme cases

    prob_string = " Problem Instance "
    print("\n" + prob_string.center(80, "=") + "\n")
    print("Weights:\n[", end="")
    for i in range(len(WEIGHTS)):
        print(str(WEIGHTS[i]), end="")
        if i == (len(WEIGHTS) - 1):
            print("]")
        elif i % 4 == 3:
            print()
        else:
            print(", ", end="")
    print("\nValues:\n[", end="")
    for i in range(len(VALUES)):
        print(str(VALUES[i]), end="")
        if i == (len(VALUES) - 1):
            print("]")
        elif i % 4 == 3:
            print(",")
        else:
            print(", ", end="")
    print()

    # Gets results for each problem instance

    for k in range(3):

        # Collects the best solution from each run and its fitness value

        best_solutions = []
        best_f_vals = []

        # Tracks the best solution over all independent runs

        overall_f_best = 0
        overall_best_chrom = Chromosome(CAPACITIES[k])
        overall_best_chrom.bitstring = ""
        for i in range(CHROM_LENGTH):
            overall_best_chrom.bitstring += "0"

        # Conducts independent runs

        for j in range(RUNS):

            # Seeds random so that results are reproducible

            random.seed(j)

            # Adds the best solution to the running list

            best_solutions.append(evolve(30, 50, CAPACITIES[k], 0.7, 0.05, penalty, cross))
            best_f_vals.append(best_solutions[j].get_value())

            # Determines if the best solution is the overall best

            if best_solutions[j].get_value() > overall_f_best:
                overall_best_chrom = best_solutions[j]
                overall_f_best = best_solutions[j].get_value()

        # Prints all the results from the independent runs for the given capacity

        result_string = " Results from 30 Independent Runs for Capacity = " + str(CAPACITIES[k]) + " "
        print("\n" + result_string.center(80, "=") + "\n")
        print(str("Mean of Best Fitness Values:\t\t\t" + str('{:.20f}'.format(statistics.mean(best_f_vals)))))
        print(str("Overall Best Fitness Value:\t\t\t\t" + str('{:.20f}'.format(overall_f_best))))
        print(str("Overall Best Bit-String:\t\t\t\t" + overall_best_chrom.bitstring))
        print(str("Overall Best Weight of Items:\t\t\t" + str('{:.20f}'.format(overall_best_chrom.get_weight()))))
        print(str("Overall Best Value of Items:\t\t\t" + str('{:.20f}'.format(overall_f_best))))
        print()


if __name__ == '__main__':

    # Prompts the user for penalty type and crossover type

    print("\n1. Static Penalty\n2. Dynamic Penalty\n")
    p_type = int(input("Please select a type of penalty: "))

    print("\n1. One-Point\n2. 0.5 Uniform\n3. Multi-Parent (Majority Voting)\n")
    c_type = int(input("Please select a type of crossover: "))

    print("\nRunning the genetic algorithm . . .\n")

    # Runs the algorithm with the user-selected penalty and crossover types

    run_algo(p_type, c_type)
