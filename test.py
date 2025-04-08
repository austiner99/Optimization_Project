import numpy as np
import math
import random

def generate_individual():
    """Generate a random keyboard layout."""
    keys = list("abcdefghijklmnopqrstuvwxyz.,'")  # 30 keys
    random.shuffle(keys)
    return keys

def string_to_index_optimized(input_string):
    """Convert input string to key index representation (dummy implementation)."""
    return [ord(char) % 30 for char in input_string.lower() if char in "abcdefghijklmnopqrstuvwxyz.,'"]

def objective_function_optimized(layout, string_index):
    """Evaluate the cost of a keyboard layout (dummy implementation)."""
    cost = sum(abs(i - string_index[i % len(string_index)]) for i in range(len(layout)))
    return cost, {}

def print_keyboard_layout(layout):
    """Print the keyboard layout in a formatted manner."""
    print("""
    {} {} {} {} {} {}
    {} {} {} {} {} {}
    {} {} {} {} {} {}
    {} {} {} {} {} {}
    {} {} {} {} {} {}
    {} {}
    """.format(*layout))

def simulated_annealing(objective_function, initial_solution, string_index, max_iterations=1000, initial_temp=100, cooling_rate=0.99):
    """
    Performs simulated annealing to optimize a keyboard layout.
    
    :param objective_function: Function to evaluate the layout score
    :param initial_solution: Initial keyboard layout as a list
    :param string_index: Index mapping for characters
    :param max_iterations: Number of iterations to run
    :param initial_temp: Starting temperature for annealing
    :param cooling_rate: Factor by which the temperature cools each iteration
    :return: Best found keyboard layout and its score
    """
    current_solution = initial_solution[:]
    best_solution = current_solution[:]
    current_score, _ = objective_function(current_solution, string_index)  # Extract numeric cost
    best_score = current_score
    temp = initial_temp
    
    for _ in range(max_iterations):
        # Ensure indices are valid
        if len(current_solution) < 2:
            break
        
        # Select two distinct indices to swap
        i, j = random.sample(range(len(current_solution)), 2)
        
        # Create a new solution by swapping two characters
        new_solution = current_solution[:]
        new_solution[i], new_solution[j] = new_solution[j], new_solution[i]
        new_score, _ = objective_function(new_solution, string_index)  # Extract numeric cost
        
        # Determine if we accept the new solution
        if new_score < current_score or random.random() < math.exp((current_score - new_score) / temp):
            current_solution = new_solution[:]
            current_score = new_score
            
            if new_score < best_score:
                best_solution = new_solution[:]
                best_score = new_score
        
        # Cool down temperature
        temp *= cooling_rate
    
    return best_solution, best_score


# Run the test
initial_solution = generate_individual()
string_index = string_to_index_optimized("example test string")

best_layout, best_score = simulated_annealing(objective_function_optimized, initial_solution, string_index)

print("Optimized Keyboard Layout:")
print_keyboard_layout(best_layout)
print("Best Score:", best_score)
