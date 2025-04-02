'''
This module...
'''
# Import necessary libraries
import numpy as np
from pathos.multiprocessing import ProcessingPool as Pool


# Functions
def generate_individual(_):  
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

def generate_population_parallel(num_people):
    # Use a Pool to generate individuals in parallel
    with Pool() as pool:
        population = pool.map(generate_individual, range(num_people))
    return population

def generate_offspring(parents, number_people, number_offspring, perc_offspring, roll_dice_parent):
    offspring = []
    while len(offspring) < number_people * perc_offspring:
        # Randomly select two parents
        indices = np.random.choice(len(parents), size=2, replace=False)  # Sample indices
        parent1, parent2 = parents[indices[0]], parents[indices[1]]  # Select parents using indices

        # Each pair produces number_offspring offspring
        for _ in range(number_offspring):  # Each pair produces number_offspring offspring

            # Create offspring from the two parents
            child = np.zeros_like(parent1)  # Initialize empty offspring
            used_keys = set()  # Track which key positions have been used

            while len(used_keys) < 30:  # Ensure all keys are assigned
                for i in range(30):
                    if tuple(child[i]) in used_keys:  # Skip if already used
                        continue

                    rand = np.random.rand()  # Generate a random number between 0 and 1

                    # Choose parent or mutation based on probability
                    if rand < roll_dice_parent:  
                        if tuple(parent1[i]) not in used_keys:
                            child[i] = parent1[i]  # Inherit from parent1
                            used_keys.add(tuple(parent1[i]))
                    elif rand < (2 * roll_dice_parent):  
                        if tuple(parent2[i]) not in used_keys:
                            child[i] = parent2[i]  # Inherit from parent2
                            used_keys.add(tuple(parent2[i]))
                    else:  
                        while True:  # Generate a random position if mutation occurs
                            x_val = np.random.randint(1, 9)
                            y_val = np.random.randint(1, 4) if x_val <= 2 else np.random.randint(1, 5)
                            if (x_val, y_val) not in used_keys:
                                child[i] = [x_val, y_val]  # Assign new random position
                                used_keys.add((x_val, y_val))
                                break

            offspring.append(child)  # Add the child to the offspring list

    return offspring

def print_keyboard_layout(x):
    layout = [[" " for _ in range(8)] for _ in range(4)]
    letters = "abcdefghijklmnopqrstuvwxyz.,?'"
    
    for i in range(30):
        x_pos = int(x[i][0]) - 1
        y_pos = 3 - (int(x[i][1]) - 1)  # Flip the y-axis
        layout[y_pos][x_pos] = letters[i]
    
    print("  1 2 3 4 5 6 7 8")
    print(" +----------------")
    for i in range(4):
        row = f"{4-i}| " + " ".join(layout[i])  # Adjust row numbering
        print(row)