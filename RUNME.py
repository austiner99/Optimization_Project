'''
Purpose:
    Find the optimal layout of a keyboard using a genetic algorithm. 

Authors:
 - Austin Erickson "The Brain"
 - Isaac Detiege "The Muscle"
 - Ammon Miller "The Milkman" (Copilot generated, lol)

Last updated: 
    4/02/2025 

Notes:
- Roll the dice method (40% p1, 40% p2, 20% mutation)

'''

# Import
from parameters import num, perc, roll, tol, gen_limit
from string_paragraph import string_index as string
from genetic_algorithm import genetic_algorithm_optimized as genetic_algorithm
from Objective_func_v3 import parallel_objective_function as obj

# Optimize
if __name__ == '__main__': # Necessary to run multiprocessing on Windows
  
    data = genetic_algorithm(obj, num, perc, roll, tol, gen_limit, string)