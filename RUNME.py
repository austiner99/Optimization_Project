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
import numpy as np
from parameters import num, perc, roll, tol, gen_limit
from string_paragraph import string_index as string
from genetic_algorithm import genetic_algorithm_optimized as genetic_algorithm
from Objective_func_v3 import parallel_objective_function as obj
from functions import print_plot_results
from warm_start import update_warm_start, stats_warm_start

# Optimize
if __name__ == '__main__': # Necessary to run multiprocessing on Windows
  
    warm_start = False
    # if warm_start:

    # stats_warm_start()
    data = genetic_algorithm(obj, warm_start, num, perc, roll, tol, gen_limit, string)
    best_individuals, best_scores, best_counters = data
    best_data = [best_individuals[-1], best_scores[-1], best_counters[-1]]
    update_warm_start(best_data)
    print_plot_results(data)
