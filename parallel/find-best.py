#!/usr/env/python

from os import listdir
import sys

files = listdir("output")

inputFile = "./in.txt"
expected_length = 444
cables_availability = []

with open(inputFile, 'r') as data:
  distance = data.readline()  
  
  pair = data.readline()
  while (pair):
    if (pair.strip() == "0 0"):
      break
    else:
      line = pair.split(" ")
      cables_availability.append(int(line[1]))
      pair = data.readline()


solutions = []

for filename in files:
  current_solution = []
  current_covered_length = 0
  current_nodes = 0
  if (filename == ".gitkeep"):
    continue

  with open("output/"+filename, "r") as f:
    contents = f.read()

    for line in contents.split('\n'):
      if 'solution:' in line:
        numbers = line.split('[')[1].split(']')[0].split(' ')
        current_solution = list(map(lambda x: int(x), numbers))

      if 'covered_length:' in line:
        current_covered_length = int(line.split(':')[1])

      if 'nodes:' in line:
        current_nodes = int(line.split('nodes: ')[1])

  
  solution = {
    'nodes': current_nodes,
    'solution': current_solution,
    'length': current_covered_length,
    'fileName': filename
  }

  solutions.append(solution)


# Filter out bad solutions
usable_solutions = []
for solution in solutions:
  correct_length = False
  availability_violated = False
  if solution["length"] == expected_length:
    correct_length = True

  for i in range(len(cables_availability)):
    if solution["solution"][i] > cables_availability[i]:
      availability_violated = True
  
  if (availability_violated == False and correct_length):
    usable_solutions.append(solution)

best_solution = None
if len(usable_solutions) > 0:
  # select the best
  min_nodes = sys.maxsize
  for solution in usable_solutions:
    if solution["nodes"] < min_nodes:
      best_solution = solution

else:
  print("No solution found. The saness...")

if best_solution is not None:
  print("Best solution")
  print(best_solution)