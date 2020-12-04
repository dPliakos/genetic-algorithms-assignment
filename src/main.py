import pygad
import numpy
import random

print("🐍")
inputFile = "./in.txt"

# Read file

distance = -1
dimensions = []
cables_availability = []
hall_of_fame = []

with open(inputFile, 'r') as data:
  distance = data.readline()  
  
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

# Create genotype
print("distance: ", distance)
print("dimensions: ", dimensions)
print("cables_availability: ", cables_availability)


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
    original_fitness = 1.0 / ((0.3*length_difference) + (0.6*quantity_violations) + (0.1*nodes))
    

    random.seed(str(original_fitness) + str(random.random()) + str(solution_idx) + "lala")
    lolo = random.random()
    if (lolo > 0.8):
      lala = random.random()
      random.seed(str(original_fitness) + str(solution_idx))
      if (lala < 0.4):
        # print("Kaboom!")
        return original_fitness + lala
      else:
        return original_fitness  
    else:
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
    print("Generation : ", ga_instance.generations_completed, " - Fitness:", f, " - sol: ", solution, " - Distance: ", covered_length, " - nodes:", nodes)

def on_parents(ga_instance, selected_parents):
    lala = []
    for parent in selected_parents:
      lala.append(str(parent))

    all_par = set(lala)
    # print("parents: ", len(all_par), " - par: ", str(all_par))
    print("parent type: ", len(all_par), " - parents:", len(selected_parents), end=" - ")



fitness_function = fitness_func

num_generations = 12000
num_parents_mating = 600
sol_per_pop = 1000
keep_parents = 300
parent_selection_type = "tournament"

mutation_percent_genes = 40
crossover_type = "two_points" # 
mutation_type = "random"

num_genes = len(dimensions)
desired_output = distance
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
                       keep_parents=keep_parents,
                       crossover_type=crossover_type,
                       mutation_type=mutation_type,
                       callback_generation=callback_gen,
                       on_parents=on_parents,
                       mutation_percent_genes=mutation_percent_genes)

ga_instance.run()

solution, solution_fitness, solution_idx = ga_instance.best_solution()
print("Parameters of the best solution : {solution}".format(solution=solution))
print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))

print("solution: ", solution)

covered_length = 0
for i in range(len(solution)):
      covered_length += solution[i] * dimensions[i]

print("covered_length: ", covered_length)
