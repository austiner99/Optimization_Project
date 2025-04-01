import numpy as np
from multiprocessing import Pool
from Objective_func_v2_2 import objective_function_optimized

def generate_individual():  
    # Initialize person 
    person = np.zeros((30,2))
    used_pairs = set()

    for i in range(30):
        while True:
            x_val = np.random.randint(1, 9)         # Random x value between 1 and 8
            if x_val == 1 or x_val == 2:            # Pinky range
                y_val = np.random.randint(1, 4)     # Choose y value between 1 and 3
            else:                                   # Other fingers range
                y_val = np.random.randint(1, 5)     # Choose y value between 1 and 4

            if (x_val, y_val) not in used_pairs:
                used_pairs.add((x_val, y_val))
                person[i] = (x_val, y_val)
                break
    return person

def generate_individual_parallel(_):
    # This function is used by Pool to generate a single individual
    return generate_individual()

def generate_population_parallel(num_people):
    # Use a Pool to generate individuals in parallel
    with Pool() as pool:
        population = pool.map(generate_individual_parallel, range(num_people))
    return population

def parallel_objective_function(args):
    x, string_index = args
    return objective_function_optimized(x, string_index)