# Import necessary libraries
import numpy as np

# Parameters
number_of_people = 50 # Number of people in the population
number_of_offspring = 10 # Number of offspring per pair of parents

percentage_clone = 0.1  # Percentage of the population to clone (top 10%)
percentage_parents = 0.2  # Percentage of the population to use as parents (top 50%)
percentage_offspring = 0.9  # Percentage of the population to be offspring (90% of the population)

tol = 100

gen_limit = 100000

roll_dice_mutation = 0.2
roll_dice_parent = (1 - roll_dice_mutation) / 2

# Make sure the values are valid
if percentage_clone + percentage_offspring != 1:
    raise ValueError("The sum of percentage_clone and percentage_offspring must equal 1. Please adjust the values.")

#      900 > 1000  Not true, good!     1000 - 1000 * 0.1  > 4 * 1000 * 0.5 / 2 
#      900 > 1000                      1000 - 1000 * 0.1  > 10 * 1000 * 0.2 / 2 
offspring_needed = number_of_people - number_of_people * percentage_clone
offspring_produced = number_of_offspring * number_of_people * percentage_parents / 2
if offspring_needed > offspring_produced:
    raise ValueError("The number of people after cloning is too small to produce the required offspring. Please adjust the values.")


num = np.array([number_of_people, number_of_offspring])
perc = np.array([percentage_clone, percentage_parents, percentage_offspring])
roll = np.array([roll_dice_parent, roll_dice_mutation])  # Roll the dice method for parent selection and mutation

