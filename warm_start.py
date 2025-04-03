import numpy as np
import pickle
from functions import print_keyboard_layout

INDIVIDUALS_FILE = "Optimization_Project/warm_start_individuals.npy"
SCORES_FILE = "Optimization_Project/warm_start_scores.npy"
COUNTERS_FILE = "Optimization_Project/warm_start_counters.npy"
MAX_PARENTS = 100  # Keep only the top 100 individuals

def load_warm_start():
    """Load individuals, scores, and counters from separate files."""
    try:
        individuals = np.load(INDIVIDUALS_FILE, allow_pickle=True)
        scores = np.load(SCORES_FILE, allow_pickle=True)
        counters = np.load(COUNTERS_FILE, allow_pickle=True)
        return individuals, scores, counters
    except FileNotFoundError:
        return np.array([], dtype=object), np.array([], dtype=float), np.array([], dtype=int)

def save_warm_start(individuals, scores, counters):
    """Save individuals, scores, and counters to separate files."""
    np.save(INDIVIDUALS_FILE, individuals, allow_pickle=True)
    np.save(SCORES_FILE, scores, allow_pickle=True)
    np.save(COUNTERS_FILE, counters, allow_pickle=True)

def update_warm_start(new_individual, new_score, new_counter):
    """Insert a new individual, score, and counter if it's better than the worst in the list."""
    individuals, scores, counters = load_warm_start()

    # Append the new individual, score, and counter
    individuals = np.append(individuals, [new_individual], axis=0) if individuals.size > 0 else np.array([new_individual], dtype=object)
    scores = np.append(scores, new_score)
    counters = np.append(counters, new_counter)

    # Sort by scores (ascending) on every run
    sorted_indices = np.argsort(scores)
    individuals = individuals[sorted_indices]
    scores = scores[sorted_indices]
    counters = counters[sorted_indices]

    # Keep only the best 100 individuals if exceeding MAX_PARENTS
    if len(scores) > MAX_PARENTS:
        individuals = individuals[:MAX_PARENTS]
        scores = scores[:MAX_PARENTS]
        counters = counters[:MAX_PARENTS]

    save_warm_start(individuals, scores, counters)
    print("Updated warm start list")

def stats_warm_start():
    individuals, scores, counters = load_warm_start()

    if len(scores) == 0:
        raise ValueError("Warm start list is empty.")
    elif len(scores) == 1:
        raise ValueError("Warm start list has only one individual.")
    else:
        print("=" * 40)
        print("Warm Start List Statistics:")
        print("=" * 40)
        print(scores)
        print("Number of individuals:", len(scores))
        print("Best individual score:", scores[0])
        print("Worst individual score:", scores[-1])
        print("Best keyboard layout:")
        print_keyboard_layout(individuals[0]) 
        print("Worst keyboard layout:")
        print_keyboard_layout(individuals[-1])
        print("Average fitness:", np.mean(scores))

def population_warm_start(number_people, roll_dice_parent):
    population = []
    individuals, scores, counters = load_warm_start()
    number_offspring = number_people // (len(individuals) // 2)  # Calculate the number of offspring
    if number_offspring == 0:
        number_offspring = 1

    while len(population) < number_people:
        # Randomly select two parents
        indices = np.random.choice(len(individuals), size=2, replace=False)  # Sample indices
        parent1, parent2 = individuals[indices[0]], individuals[indices[1]]  # Select parents using indices

        # Each pair produces number_offspring offspring
        for _ in range(number_offspring):
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