'''
This module...
'''
# Import necessary libraries
import heapq
from pathos.multiprocessing import ProcessingPool as Pool
from functions import generate_population_parallel, generate_offspring, print_keyboard_layout


def genetic_algorithm_optimized(f, num, perc, roll, tol, gen_limit, string_index):
    number_people = num[0]
    number_offspring = num[1]
    perc_clone = perc[0]
    perc_parents = perc[1]
    perc_offspring = perc[2]
    roll_dice_parent = roll[0]
    roll_dice_mutation = roll[1]

    population = generate_population_parallel(number_people)
    best_score_unchanged_count = 0
    history_best_score = float('inf')
    best_individuals = []
    best_scores = []
    best_counters = []
    gen_counter = 0

    while gen_counter < gen_limit:
        gen_counter += 1

        # Parallel fitness evaluation using Pool
        with Pool() as pool:
            fitness_results = pool.map(f, [(p, string_index) for p in population])

        # Partial sort (percentage_clone)
        top_k = int(number_people * max(perc_clone, perc_parents))
        best_individuals_data = heapq.nsmallest(top_k, zip(population, fitness_results), key=lambda x: x[1][0])

        sorted_population = [x[0] for x in best_individuals_data]
        best_score, best_counter = best_individuals_data[0][1]
        
        # Store the best individual data
        best_individuals.append(sorted_population[0])
        best_scores.append(best_score)
        best_counters.append(best_counter)
        
        # Update convergence criteria
        if best_score < history_best_score:
            history_best_score = best_score
            best_score_unchanged_count = 0
            print("Generation:", gen_counter)
            print("Best Score:", best_score)
            print_keyboard_layout(sorted_population[0])
        else:
            best_score_unchanged_count += 1

        if best_score_unchanged_count >= tol:
            break

        ## Selection ##
        clone = sorted_population[:int(number_people * perc_clone)]
        parents = sorted_population[:int(number_people * perc_parents)]

        ## Crossover ##
        offspring = generate_offspring(parents, number_people, number_offspring, perc_offspring, roll_dice_parent)

        population = clone + offspring

    return best_individuals, best_scores, best_counters