import random
import numpy as np
from tabulate import tabulate
import random

def simulate_gender(fate):
    if fate == "f":
        return 1
    elif fate == "m":
        return 2

# Function to simulate one step for a single bacterium
def simulate_bacterium(fate):
    if fate == "split":
        # Calculate how  many females and males are produced
        
        return 2  # If the bacterium splits, return 2 for two offspring
    elif fate == "stay":
        return 1  # If the bacterium stays, return 1 for itself
    else:
        return 0  # If the bacterium dies, return 0 for no offspring
    
def mating_function(available_males, available_females):
    couples = []
    singles = []
    random.shuffle(available_males)
    random.shuffle(available_females)
    for male, female in zip(available_males, available_females):
        couples.append([male, female])
    
    if len(available_males) > len(couples):
        singles.extend(available_males[len(couples):])
    elif len(available_females) > len(couples):
        singles.extend(available_females[len(couples):])
    
    return couples, singles

def generate_tree(N, steps = 5):
    # Root level and first level special case
    all_trees = {i: [[(0,)]] for i in range(N)}
    all_genders = {i: [[(0,)]] for i in range(N)}
    all_couples = []
    all_singles = []
    all_data = {i: [] for i in range(N)}

    for n in range(N):
        fate_of_root = np.random.choice(['die', 'stay', 'split'], p=[0.1, 0.4, 0.5])
        if fate_of_root == 'die':
            return 0,0,0
        first_generation_count = simulate_bacterium(fate_of_root)
        level1 = []
        genders1 = []
        for i in range (first_generation_count):
            level1.append((i+1,))
            gender = np.random.choice(['f', 'm'], p=[0.5, 0.5])
            genders1.append(gender)
        all_trees[n].append(level1)
        all_genders[n].append(genders1)
        all_data[n].append([0, 'Root', 'No gender', first_generation_count, '-', '-'])
    #Iterate over levels, then trees
    for level in range(1, steps+1):
        females = []
        males = []
        for n in range(N):
            current_level = []
            current_gender_level = []
            for parent_index, parent in enumerate(all_trees[n][level]):
                fate = np.random.choice(['die', 'stay', 'split'], p=[0.25, 0.25, 0.5])
                single_parent = (n,) + parent
                relationship = '-'
                partner = '-'
                for single in all_singles:
                    if single_parent in single:
                        fate = 'die'
                        relationship = 'single'
                for couple in all_couples:
                    if single_parent in couple:
                        relationship = 'couple'
                        partner = couple[1-couple.index(single_parent)]
                offspring_count = simulate_bacterium(fate)
                all_data[n].append([level, parent, all_genders[n][level][parent_index], offspring_count, relationship, partner])
                for child in range(1, offspring_count+1):
                    gender_fate = np.random.choice(['f', 'm'], p=[0.5, 0.5])
                    child_node = parent + (child,)
                    if gender_fate == 'f':
                        females.append((n,) + child_node)
                    elif gender_fate == 'm':
                        males.append((n,) + child_node)
                    current_gender_level.append(gender_fate)
                    current_level.append(child_node)
            all_trees[n].append(current_level)
            all_genders[n].append(current_gender_level)
        couples, singles = mating_function(males, females)
        all_couples.extend(couples)
        all_singles.append(singles)
    return all_trees, all_genders, all_data
    
def explain_process(N, steps=5):
    all_trees, all_genders, all_data = generate_tree(N, steps=steps)
    col_names = ['Level', 'Node', 'Gender', 'Number of offspring', 'Relationship Status', 'Mate']
    if all_trees == 0:
        print('A root died')
        return
    for i in range(N):
        data = all_data[i]
        print('Table for tree number', i+1)
        print(tabulate(data, headers=col_names, tablefmt='pretty'))

explain_process(3, 3)

# couples, singles = mating_function([(1, 1, 1), (1, 1, 2), (1, 2, 1)], [(1, 2, 2), (1, 2, 3), (1, 3, 1)])
# print('Couples', couples)
# print('Singles', singles)

