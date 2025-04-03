import numpy as np
import pickle
from functions import print_keyboard_layout


FILENAME = "Optimization_Project/warm_start_data.npy"
MAX_PARENTS = 100  # Keep only the top 100 individuals

def load_warm_start():
    """Load the warm start list from a file as a NumPy array."""
    try:
        parents = np.load(FILENAME, allow_pickle=True)
        if parents.ndim == 0:  # Handle cases where loading a single object
            return np.array([], dtype=object)
        return parents
    except FileNotFoundError:
        return np.array([], dtype=object)  # Return empty array if no file exists

def save_warm_start(parents):
    """Save the top 100 parents to a file."""
    np.save(FILENAME, parents, allow_pickle=True)

def update_warm_start(new_individual):
    """Insert a new individual if it's better than the worst in the list."""
    parents = load_warm_start()

    # Ensure parents is a 2D object array for correct stacking
    if parents.size == 0:
        parents = np.array([new_individual], dtype=object)  # Treat new_individual as an object
    else:
        # Stack the new individual properly
        parents = np.vstack([parents, new_individual])

    # Keep only the best 100 individuals (sorted by fitness)
    if parents.shape[0] > MAX_PARENTS:
        # Sort by fitness (assuming fitness is at index 1)
        sorted_indices = np.argsort([p[1] for p in parents])  
        parents = parents[sorted_indices[:MAX_PARENTS]]  # Keep top 100

    save_warm_start(parents)
    print("Updated warm start list")



def stats_warm_start():
    parents = load_warm_start()

    if parents.size == 0:
        raise ValueError("Warm start list is empty.")
    elif parents.size == 1:
        raise ValueError("Warm start list has only one individual.")
    else:    
        print("Warm Start List Statistics:")
        print("Number of individuals:", len(parents))
        print("Best individual:", parents[0][1])
        print("Best keyboard layout:")
        print_keyboard_layout(parents[0][0])  # Assuming p[0] is the keyboard layout
        print("Worst individual:", parents[-1][1])
        print("Worst keyboard layout:")
        print_keyboard_layout(parents[-1][0])  # Assuming p[0] is the keyboard layout
        print("Average fitness:", np.mean([p[1] for p in parents]))  # Assuming p[1] is fitness

def population_warm_start(number_people, roll_dice_parent):
    population = []
    parents = load_warm_start()
    number_offspring = number_people // (len(parents) // 2)  # Calculate the number of offspring
    while len(population) < number_people:
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

            population.append(child)  # Add the child to the offspring list

    return population