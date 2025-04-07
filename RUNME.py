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
  
    warm_start = True              # True - generates first population from best previous individuals
    print_while_running = False    # True - prints generation, score, and layout data while running
    print_results_long = False     # True - prints long results after running
    print_results_short = True     # True - prints short results after running
    convergence = False            # True - plots convergence graph
    run = False                    # True - runs the program, False runs just stats_warm_start()

    stats_warm_start(5)
    if run:
        num_programs = 1 # Number of programs to run
        for i in range(num_programs):
            # Alternate warm_start between odd and even iterations
            warm_start = (i % 2 == 0)

            # Optimization via genetic algorithm
            data = genetic_algorithm(obj, warm_start, num, perc, roll, tol, gen_limit, string, print_while_running)

            # Unpack data
            best_individuals, best_scores, best_counters = data
            update_warm_start(best_individuals[-1], best_scores[-1], best_counters[-1])
            print_plot_results(data, i+1, num_programs, print_results_long, print_results_short, warm_start, convergence)

