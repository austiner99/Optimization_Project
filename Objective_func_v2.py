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


#---------------------------------
# Functions
#---------------------------------
def string_to_index(string):
    # Convert string to lower case
    string = string.lower()
    # Remove spaces from the string
    string = string.replace(" ", "")
    # Convert letters and punctuation in the string to index where a is 0, b is 1, etc.
    index = []
    for char in string:
        if char.isalpha():
            index.append(ord(char) - 97)
        elif char == '.':
            index.append(26)
        elif char == ',':
            index.append(27)
        elif char == '?':
            index.append(28)
        elif char == "'":
            index.append(29)
    return index
    
def objective_function(x): #take in an individual, x, which is a 30x2 matrix (30 rows for different keys, 2 columns for x and y positions)
    #initialize resting finger positions - assume that each finger comes to rest after pressing a key UNLESS the next key is pressed by the same finger
    f0 = np.array([1.5,2]) #pinky finger
    f1 = np.array([3.5,2.5]) #ring finger
    f2 = np.array([5.5,2.5]) #middle finger
    f3 = np.array([7.5,2.5]) #index finger
    home_positions = np.array([f0,f1,f2,f3])

    #initialize counters
    pinky_finger_count = 0
    ring_finger_count = 0
    middle_finger_count = 0
    index_finger_count = 0
    same_finger_penalty_count = 0

    # Penalty Values
    pinky_penalty = 0.5
    ring_penalty = 0
    middle_penalty = 0
    index_penalty = 0
    same_finger_penalty_value = 0.5
    
    #take in some string of letters (paragraph from chatgpt)
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

    string_index = string_to_index(string) #convert string to index in function above    
    score = 0 # initialize total_dist to 0
    prev_active_finger = np.inf # initialize active_finger_prev to a value that is not 0,1,2,3
    for j in range(len(string_index)):

        # Where is the key?
        next_key = string_index[j]
        next_finger_position = x[next_key]

        if x[next_key][0] <= 2:   # pinky finger
            next_active_finger = 0
            active_finger_penalty = pinky_penalty
            pinky_finger_count += 1
        elif x[next_key][0] <= 4: # ring finger
            next_active_finger = 1
            active_finger_penalty = ring_penalty
            ring_finger_count += 1
        elif x[next_key][0] <= 6: # middle finger
            next_active_finger = 2
            active_finger_penalty = middle_penalty
            middle_finger_count += 1
        else:                       # index finger
            next_active_finger = 3
            active_finger_penalty = index_penalty
            index_finger_count += 1
            
        # Calc current_finger_position
        if j != 0 and next_active_finger == prev_active_finger:     # Same finger
            current_finger_position = prev_finger_position
            same_finger_penalty = same_finger_penalty_value
            same_finger_penalty_count += 1
        else:                                                       # Different finger
            current_finger_position = home_positions[next_active_finger]
            same_finger_penalty = 0
        
        # Reset prev_finger_position and prev_active_finger
        prev_finger_position = next_finger_position
        prev_active_finger = next_active_finger
        
        # Calc distance
        distance = np.linalg.norm(current_finger_position - x[next_key])

        # Calc score
        score += distance + active_finger_penalty + same_finger_penalty

    # Combine counters
    counters = [pinky_finger_count, ring_finger_count, middle_finger_count, index_finger_count, same_finger_penalty_count]
    return score, counters

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

def generate_population(num_people):
    # Create a population of num_people persons
    population = []
    for i in range(num_people):
        person = generate_individual()
        population.append(person)
    return population

def genetic_algorithm(f, num, perc, roll, tol, gen_limit):
    # Initialize parameters
    number_people = num[0]      # Number of people in the population
    number_offspring = num[1]   # Number of offspring per pair of parents
    perc_clone = perc[0]        # Percentage of the population to clone (top 10%)
    perc_parents = perc[1]      # Percentage of the population to use as parents (top 50%)
    perc_offspring = perc[2]    # Percentage of the population to be offspring (90% of the population)
    roll_dice_parent = roll[0]  # Probability of selecting parent1 (30%)
    roll_dice_mutation = roll[1] # Probability of mutation (40%)

    # Generate intial population
    population = generate_population(number_people)

    # Initialize convergence criteria
    best_score_unchanged_count = 0
    history_best_score = float('inf')  # Initialize best score to infinity

    # Initialize lists to store best individuals and their scores
    best_individuals = []
    best_scores = []
    best_counters = []

    # Initialize gen_counter
    gen_counter = 0

    while True:
        # Break after gen_limit
        gen_counter += 1
        print("Generation:", gen_counter)
        if gen_counter > gen_limit:
            break

        # Evaluate fitness and sort the population based on scores
        fitness_results = [f(p) for p in population]
        sorted_data = sorted(zip(population, fitness_results), key=lambda x: x[1][0])

        # Extract sorted population and fitness results
        sorted_population = [x[0] for x in sorted_data]
        best_score, best_counter = sorted_data[0][1]

        # Store the best individual data
        best_individuals.append(sorted_population[0])
        best_scores.append(best_score)
        best_counters.append(best_counter)
        
        # Update convergence criteria
        if best_score < history_best_score:
            history_best_score = best_score
            best_score_unchanged_count = 0  # Reset the counter if the best score improves
            print("Best Score:", best_score)  # Print the best score for the current generation
            print(print_keyboard_layout(sorted_population[0]))
        else:
            best_score_unchanged_count += 1  # Increment the counter if the best score remains unchanged

        if best_score_unchanged_count >= tol:
            break

        ## Selection ##
        # Clone the top 10% of the population to be parents for the next generation
        clone = sorted_population[:int(number_people * perc_clone)]  # Top perc_clone% of the sorted population

        # Pick the top 50% to be parents
        parents = sorted_population[:int(number_people * perc_parents)]  # Top 50% of the sorted population

        ## Crossover ##
        # Produce perc_offspring% offspring
        offspring = []
        while len(offspring) < number_offspring:
            # Randomly select two parents
            indices = np.random.choice(len(parents), size=2, replace=False)  # Sample indices
            parent1, parent2 = parents[indices[0]], parents[indices[1]]  # Select parents using indices

            for _ in range(number_offspring):  # Each pair produces number_offspring offspring
                child = np.zeros_like(parent1)
                used_keys = set()

                while len(used_keys) < 30:  # Loop until all keys are used
                    for i in range(30):  # Iterate over all keys
                        if tuple(child[i]) in used_keys:  # Skip if the key is already used
                            continue

                        rand = np.random.rand()
                        if rand < roll_dice_parent:  
                            if tuple(parent1[i]) not in used_keys:
                                child[i] = parent1[i]
                                used_keys.add(tuple(parent1[i]))
                        elif rand < (2*roll_dice_parent):  
                            if tuple(parent2[i]) not in used_keys:
                                child[i] = parent2[i]
                                used_keys.add(tuple(parent2[i]))
                        else:  
                            while True:
                                x_val = np.random.randint(1, 9)
                                y_val = np.random.randint(1, 4) if x_val <= 2 else np.random.randint(1, 5)
                                if (x_val, y_val) not in used_keys:
                                    child[i] = [x_val, y_val]
                                    used_keys.add((x_val, y_val))
                                    break

                offspring.append(child)
                if len(offspring) >= number_offspring:
                    break
        
        population = clone + offspring  # Combine parents and offspring

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


#---------------------------------
# Optimize
#---------------------------------
# Parameters
number_of_people = 10 # Number of people in the population
number_of_offspring = 4 # Number of offspring per pair of parents

percentage_clone = 0.1  # Percentage of the population to clone (top 10%)
percentage_parents = 0.5  # Percentage of the population to use as parents (top 50%)
percentage_offspring = 0.9  # Percentage of the population to be offspring (90% of the population)

tol = 20

gen_limit = 10000

roll_dice_mutation = 0.3
roll_dice_parent = (1 - roll_dice_mutation) / 2

# Make sure the values are valid
if percentage_clone + percentage_offspring != 1:
    raise ValueError("The sum of percentage_clone and percentage_offspring must equal 1. Please adjust the values.")

if number_of_people - number_of_people * percentage_clone > number_of_offspring * number_of_people * percentage_parents / 2:
    raise ValueError("The number of people after cloning is too small to produce the required offspring. Please adjust the values.")



num = np.array([number_of_people, number_of_offspring])
perc = np.array([percentage_clone, percentage_parents, percentage_offspring])
roll = np.array([roll_dice_parent, roll_dice_mutation])  # Roll the dice method for parent selection and mutation

best_individuals, best_scores, best_counters = genetic_algorithm(objective_function, num, perc, roll, tol, gen_limit)


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



