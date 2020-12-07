import pygad
import numpy
import random
import sys
import matplotlib.pyplot as plt

# script options
show_trace = False
show_graph = False

for option in sys.argv:
    if option == "-t" or option == "--trace":
        show_trace = True
    if option == "-g" or option == "--graph":
        show_graph = True

# Global variables to be used in the library hooks
global consecutive_equivalent_solutions
global current_best_solution
global max_consecutive_equivalent_solutions
consecutive_equivalent_solutions = 0
max_consecutive_equivalent_solutions = 50
current_best_solution = []  # placeholder


inputFile = "./in.txt"

if show_graph:
    plot_x = []
    plot_y = []


# Read data
distance = -1
dimensions = []
cables_availability = []

with open(inputFile, 'r') as data:
    distance = int(data.readline())

    pair = data.readline()
    while (pair):
        # read next pair
        if (pair.strip() == "0 0"):
            break
        else:
            line = pair.split(" ")
            dimensions.append(int(line[0]))
            cables_availability.append(int(line[1]))
            pair = data.readline()


# Init alg


def get_current_length(index, nCables):
    return dimensions[index] * nCables


def fitness_func(solution, solution_idx):
    covered_length = 0

    for i in range(len(solution)):
        covered_length += solution[i] * dimensions[i]

    # difference
    length_difference = numpy.abs(numpy.int32(distance) - covered_length)

    # do not violate number of cables
    quantity_violations = 0
    nodes = 0
    for i in range(len(cables_availability)):
        nodes += solution[i]
        if solution[i] > cables_availability[i]:
            quantity_violations += solution[i] - cables_availability[i]
    quantity_violations *= 10
    length_difference *= 10
    nodes = nodes - 1
    original_fitness = 1.0 / \
        ((0.3*length_difference) + (0.6*quantity_violations) + (0.1*nodes))
    return original_fitness


def callback_gen(ga_instance):
    sol = ga_instance.best_solution()
    f = sol[1]

    covered_length = 0
    solution = sol[0]
    for i in range(len(solution)):
        covered_length += solution[i] * dimensions[i]

    quantity_violations = 0
    nodes = 0
    for i in range(len(cables_availability)):
        nodes += solution[i]
        if solution[i] > cables_availability[i]:
            quantity_violations += solution[i] - cables_availability[i]

    nodes = nodes - 1

    global show_trace
    if show_trace:
        print("Generation : ", ga_instance.generations_completed, " - Fitness:", f,
            " - sol: ", solution, " - Distance: ", covered_length, " - nodes:", nodes)

    global consecutive_equivalent_solutions
    global current_best_solution

    solution_representation = str(solution)
    if solution_representation == current_best_solution:
        consecutive_equivalent_solutions += 1
    else:
        current_best_solution = solution_representation
        consecutive_equivalent_solutions = 0


    if show_graph:
        plot_x.append(ga_instance.generations_completed)
        plot_y.append(f)

    if consecutive_equivalent_solutions >= max_consecutive_equivalent_solutions:
        return "stop"


def on_parents(ga_instance, selected_parents):
    lala = []
    for parent in selected_parents:
        lala.append(str(parent))

    all_par = set(lala)

    global show_trace
    if show_trace:
        print("parent types: ", len(all_par), " - parents:",
            len(selected_parents), end=" - ")


fitness_function = fitness_func

num_generations = 12000
num_parents_mating = 600
sol_per_pop = 1000
keep_parents = 300
parent_selection_type = "tournament"
k_tournament= 3

mutation_percent_genes = 40
crossover_type = "two_points"
mutation_type = "random"

num_genes = len(dimensions)
init_range_low = min(cables_availability)
init_range_high = max(cables_availability)


ga_instance = pygad.GA(num_generations=num_generations,
                       num_parents_mating=num_parents_mating,
                       fitness_func=fitness_function,
                       sol_per_pop=sol_per_pop,
                       gene_type=int,
                       num_genes=num_genes,
                       init_range_low=init_range_low,
                       init_range_high=init_range_high,
                       parent_selection_type=parent_selection_type,
                       K_tournament=k_tournament,
                       keep_parents=keep_parents,
                       crossover_type=crossover_type,
                       mutation_type=mutation_type,
                       on_generation=callback_gen,
                       on_parents=on_parents,
                       mutation_percent_genes=mutation_percent_genes)

ga_instance.run()

solution, solution_fitness, solution_idx = ga_instance.best_solution()

covered_length = 0
number_of_cables = 0
nodes = 0
formula_factors = []
for i in range(len(solution)):
    covered_length += solution[i] * dimensions[i]
    number_of_cables += solution[i]
    formula_factors.append("{factor}*{length}".format(factor=solution[i], length=dimensions[i]))
formula = " + ".join(formula_factors)
nodes = number_of_cables - 1

if show_graph:
    plt.plot(plot_x, plot_y, label="Fitness of best solution")
    plt.title('Model training')
    plt.ylabel('Best fitness')
    plt.xlabel('Generations')
    plt.yticks([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
    plt.legend(loc = 'best')
    plt.show()


# Show output
"""
Adds some awesomeness at the output. You should use it as often as possible.
"""
def awesomeness(show_label=False):
    for _ in range(20):
        print("🦄", end="")
    if (show_label):
        print(" ~ Awesomeness ~ ", end="")
    else: 
        for _ in range(8):
            print("🦄", end="")    
    for _ in range(20):
        print("🦄", end="")
    print("")

awesomeness(True)
print("Requirements: ")
print(" - Distance: ", distance, "Km")
print(" - Available dimensions: ", dimensions)
print(" - Cables availability: ", cables_availability)

print("")
print("Solution:")
print(" - Parameters of the best solution: {solution}".format(solution=solution))
print(" - Formula: ", formula)
print(" - Fitness value of the best solution = {solution_fitness}".format(
    solution_fitness=solution_fitness))
print(" - Covered length: ", covered_length, "Km")
print(" - Number of cables: ", number_of_cables)
print(" - Nodes of best solution: ", nodes)
awesomeness()
