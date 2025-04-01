'''
The purpose of this code is...


Authors:
 - Austin Erickson "The Brain"
 - Isaac Detiege "The Muscle"
 - Ammon Miller "The Milkman" (Copilot generated, lol)

Last updated: 3/27/2025 around 3pm

Notes:
- Roll the dice method (40% p1, 40% p2, 20% mutation)

'''
#---------------------------------
# Import 
#---------------------------------
import numpy as np
import matplotlib.pyplot as plt
from pathos.multiprocessing import ProcessingPool as Pool
import heapq


#---------------------------------
# Functions
#---------------------------------

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

def string_to_index_optimized(string):
    # Vectorized approach for string-to-index conversion
    string = string.lower().replace(" ", "")
    char_map = {chr(i + 97): i for i in range(26)}
    char_map.update({'.': 26, ',': 27, '?': 28, "'": 29})
    return np.array([char_map.get(char, -1) for char in string])
    
def objective_function_optimized(x, string_index):
    home_positions = np.array([[1.5, 2], [3.5, 2.5], [5.5, 2.5], [7.5, 2.5]])  # Predefine finger positions
    penalties = [0.5, 0, 0, 0]  # Pinky, Ring, Middle, Index penalties
    same_finger_penalty = 0.5
    
    # Initialize counters
    finger_counts = [0, 0, 0, 0, 0]  # Pinky, Ring, Middle, Index, Same Finger
    score = 0
    
    prev_active_finger = -1
    prev_finger_position = np.inf
    
    for key in string_index:
        next_finger_position = x[key]
        if next_finger_position[0] <= 2:
            next_active_finger = 0
        elif next_finger_position[0] <= 4:
            next_active_finger = 1
        elif next_finger_position[0] <= 6:
            next_active_finger = 2
        else:
            next_active_finger = 3

        # Apply penalties
        active_finger_penalty = penalties[next_active_finger]
        finger_counts[next_active_finger] += 1
        
        # Same finger penalty logic
        if prev_active_finger == next_active_finger:
            finger_counts[-1] += 1
            same_finger_penalty_value = same_finger_penalty
        else:
            same_finger_penalty_value = 0

        # Calculate distance
        current_finger_position = home_positions[next_active_finger] if prev_active_finger != next_active_finger else prev_finger_position
        distance = ((current_finger_position[0] - next_finger_position[0])**2 + (current_finger_position[1] - next_finger_position[1])**2)**0.5
        
        # Update score
        score += distance + active_finger_penalty + same_finger_penalty_value
        
        # Update previous finger position and active finger
        prev_active_finger = next_active_finger
        prev_finger_position = next_finger_position
    
    return score, finger_counts

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
            fitness_results = pool.map(parallel_objective_function, [(p, string_index) for p in population])

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
        

string = "The sun’s warm glow fell across the field. A breeze stirred, rustling leaves as birds chirped. The dog’s bark echoed while a cat lounged nearby. People walked along quiet paths, sharing thoughts. What joy exists in moments like these? Clouds drifted above, shadows shifting below. Foxes dashed through the brush. Time’s passage often feels swift. Yet, laughter lingers. Jars of jam lined the shelf. Vivid quilts hung, displaying vibrant hues. Zebras grazed in far-off lands. Quirky scenes unfold daily. Few question why. Life’s charm, both simple and profound, remains constant. Is there anything more precious than this? \" \
    Children played along the park’s edge, their laughter mingling with the breeze. Ducks glided across the pond, ripples trailing behind. Tall trees stood in silent watch, their branches swaying softly. Nearby, a gardener tended flowers, carefully pruning each stem. The air smelled of fresh earth and blooming petals. Squirrels scampered up tree trunks, their tails flicking in delight. Nature thrived, unburdened by time’s relentless march. \
    A man with a weathered hat sat upon a bench, his hands clasped together. His eyes traced the flight of a passing bird. What memories lingered within his thoughts? Each wrinkle on his face told a story, shaped by years of joy and sorrow. A nearby jogger passed, earbuds in, oblivious to the world around her. Life continued, ever in motion. \
    By the water’s edge, a family spread a picnic blanket. Sandwiches, fruit, and lemonade filled their basket. The youngest child giggled as she chased a butterfly. The parents watched with gentle smiles, savoring the fleeting moments of innocence. Sunlight dappled the ground, illuminating patches of vibrant green. A dragonfly hovered above the reeds, its wings glinting. \
    In the distance, an old farmhouse stood, its red paint peeling. Wooden shutters, once bright, now bore the marks of age. The wind stirred the tall grass, sending waves across the golden field. A black cat perched on the porch, eyes gleaming. Beside the barn, rusted tools lay abandoned. Yet, even in neglect, beauty endured. \
    A narrow dirt road wound through the countryside. Along its path, wildflowers bloomed in bursts of yellow and purple. Cows grazed lazily, tails flicking away flies. A lone cyclist pedaled past, the hum of tires blending with the chirp of crickets. Overhead, a hawk soared, scanning the ground below. \
    Night approached, and the sky deepened to indigo. Stars blinked into existence, scattered like gems. A crescent moon hung low, casting silver light. In a small town nearby, streetlamps flickered on. Porch lights glowed warmly, welcoming home weary travelers. Laughter spilled from an open window, the sound of a family gathered for dinner. \
    A couple strolled hand in hand, their steps in perfect rhythm. They paused beneath a lamppost, its glow casting a halo around them. The man whispered something, drawing a soft laugh from his companion. Shadows danced along the pavement. Above them, the stars watched in silent approval. \
    Time passed, as it always does. Seasons changed, painting the world in hues of gold, crimson, and green. Children grew, their laughter echoing through the years. Leaves fell, carpeting the ground in a crunchy mosaic. Snow blanketed rooftops, muffling the world in a quiet embrace. Yet, the cycle continued. \
    In spring, blossoms burst forth, coloring branches with pink and white. Bees buzzed, drawn to the sweet nectar. Farmers tilled the soil, their hands darkened with earth. Rain fell in gentle showers, nourishing the eager roots. Frogs croaked from hidden ponds. Life thrived. \
    Summer brought long days of warmth. Fields of wheat swayed under the sun’s golden gaze. Children dashed through sprinklers, squealing with delight. Ice cream dripped from cones, melting faster than it could be licked. Fireflies blinked in the twilight, their glow like tiny stars. Laughter echoed from backyard gatherings. \
    Autumn arrived with a crisp breeze. Leaves turned brilliant shades of amber and scarlet. Pumpkins dotted fields, their orange shells gleaming. Families wandered through corn mazes, laughter guiding their way. Bonfires crackled, sending sparks skyward. The scent of cinnamon and apple cider lingered in the air. \
    Winter followed, wrapping the world in icy stillness. Frost traced delicate patterns upon windowpanes. Children built snowmen, their mittens damp with melted snow. Smoke curled from chimneys, mingling with the cold air. The ground glittered beneath the moonlight, each snowflake unique. Silence reigned, broken only by the crunch of boots upon snow. \
    Yet, through every season, life endured. The fox still leaped, the dog barked, and the cat purred. People gathered, shared stories, and held one another close. Time moved forward, but memories remained. And in those memories, joy blossomed. \
    A robin sang at dawn, its cheerful notes welcoming the sun. Dew clung to blades of grass, shimmering like jewels. A farmer’s rooster crowed, greeting the day with pride. Somewhere, a child stirred beneath warm blankets, dreaming of distant adventures. \
    The ocean’s waves crashed against the shore, sending salty mist into the air. Gulls circled above, their cries mingling with the breeze. A lighthouse stood tall, its beam sweeping across the darkened waters. Sailboats bobbed in the harbor, their sails furled. \
    Farther inland, mountains rose, their peaks kissed by clouds. Pine trees lined the slopes, their needles dusted with snow. Hikers paused to admire the view, their breath visible in the thin air. A hawk soared, its sharp eyes scanning the forest below. \
    In bustling cities, people hurried along crowded sidewalks. Taxi horns blared, and street vendors called to passing customers. Neon signs flickered, illuminating the night. Yet, even amidst the chaos, beauty lingered. Musicians played on street corners, their melodies weaving through the urban hum. \
    In quieter towns, church bells rang, their chimes echoing across the valley. Children rode bicycles along winding paths. Farmers tended their fields, the scent of fresh hay filling the air. Life moved at a gentler pace. \
    As twilight fell, the sky blazed with hues of pink and orange. Couples sat on porches, watching the day’s end. Fireflies emerged, their soft glow dancing in the dark. Stars appeared, each one a reminder of the vastness beyond. \
    The world whispered its stories to those who listened. From the rustle of leaves to the crash of waves, every sound held meaning. Even the silence spoke, offering solace to those who sought it. \
    So, as time marches on, may we pause to savor the moments that remain. The laughter of loved ones, the warmth of the sun, the simple joy of a breeze through the trees. For in these fleeting instants, life’s beauty endures. \
    And perhaps, that is enough. \
    "


#---------------------------------
# Optimize
#---------------------------------
# Parameters
number_of_people = 100 # Number of people in the population
number_of_offspring = 10 # Number of offspring per pair of parents

percentage_clone = 0.1  # Percentage of the population to clone (top 10%)
percentage_parents = 0.2  # Percentage of the population to use as parents (top 50%)
percentage_offspring = 0.9  # Percentage of the population to be offspring (90% of the population)

tol = 500

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



#FIXME
ws_group_size = 20  # Number of warm start individuals

for i in range(ws_group_size)
    best_individuals, best_scores, best_counters = genetic_algorithm_optimized(objective_function_optimized, num, perc, roll, tol, gen_limit, string_to_index_optimized(string))


#---------------------------------
# Print & Plot Results
#---------------------------------
# Print results only when the score changes
previous_score = None
generations = []
filtered_best_scores = []
# Header for Results
print("\n" + "="*40)
print("Genetic Algorithm Optimization Results")
print("="*40 + "\n")

for i, (score, counter, individual) in enumerate(zip(best_scores, best_counters, best_individuals)):
    if score != previous_score:
        print(f"Generation {i + 1}:")
        print(f"Best Score: {score}")
        print(f"Counter: {counter}")
        print_keyboard_layout(individual)
        print()
        previous_score = score
        generations.append(i + 1)  # Track the generation for the convergence graph
        filtered_best_scores.append(score)  # Track the best score only when it changes

plt.figure(figsize=(10, 6))
plt.plot(generations, filtered_best_scores, marker='o', linestyle='-', color='b')
plt.xlabel('Generation')
plt.ylabel('Best Score')
plt.title('Convergence Graph')
plt.grid(True)
plt.locator_params(axis='x', nbins=10)  # Limit the number of x-axis grid lines to 10
plt.savefig('genetic_conv.png')  # Save the figure as genetic_conv.png
plt.show()



