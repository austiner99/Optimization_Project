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


def parallel_objective_function(args):
    x, string_index = args
    home_positions = np.array([[1.5, 2], [3.5, 2.5], [5.5, 2.5], [7.5, 2.5]])  # Predefine finger positions
    penalties = [0.5, 0.2, 0, 0]  # Pinky, Ring, Middle, Index penalties
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
