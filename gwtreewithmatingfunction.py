import random
from matplotlib.collections import LineCollection
import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate

existing_postitions = []

def simulate_gender(fate):
    return 1 if fate == "f" else 2

def simulate_bacterium(fate):
    return 2 if fate == "split" else 1 if fate == "stay" else 0

def get_color(gender):
    if ( gender == 1):
        return 'red'
    elif ( gender == 2):
        return 'blue'
    else:
        return 'black'

def mating_function(available_males, available_females, child_parent):
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
    
def generate_offspring(parents, level):
    current_level = []
    lines = []
    base_spacing = 10
    min_spacing = 2
    parent_offpring = {}
    child_parent = {}
    offspring_cnt = 0
    
    for parent in parents:
        # p0 = 0.10, p1 = 0.09, p2 = 0.26, p3 = 0.25, p4 = 0.23, p5 = 0.05, p6 = 0.02
        # p=[0.10,0.09,0.26,0.25,0.23,0.05,0.02]
        fate = np.random.choice([0, 1, 2, 3], p = [0.1, 0.35, 0.40, 0.15])
        offspring_count = fate
        offspring_cnt += offspring_count
        spacing = max(base_spacing / (2 ** level), min_spacing)
        start_x = parent[0] - (offspring_count - 1) * spacing / 2
        children = []
        for child in range(offspring_count):
            gender_fate = np.random.choice(['f', 'm'], p=[0.5, 0.5])
            gender = simulate_gender(gender_fate)
            cx = start_x + child * spacing
            cy = parent[1] - 1
            child_parent[(cx,cy,gender)] = parent
    
            while any((cx, cy) == pos for pos in current_level):
                cx += min_spacing
            
            current_level.append((cx, cy, gender))
            children.append((cx, cy, gender))
            lines.append([(parent[0], parent[1]), (cx, cy)])
        
        parent_offpring[parent] = children
    
    return current_level, lines, parent_offpring, offspring_cnt, child_parent

def draw_trees(N, steps=5):
    # Figure and plot config
    fig, ax = plt.subplots()
    ax.axis('off')
    ax.set_xlim(-15, 15 + N * 10)
    ax.set_ylim(-steps - 1, 1)
    child_parent = {}
    # Intialize tree
    all_nodes = [[(i*10,0,1) if i < np.floor(N/2) else (i*10,0,2) for i in range(N)]]
    
    # Data analysis
    tot_num_offpring = {}
    nodes_and_forfathers = {all_nodes[0][i]: [all_nodes[0][i]] for i in range(N)}
    forfather_fraction_d = {}
    # Plot the roots
    for node in all_nodes[0]:
        color = get_color(node[2])
        ax.plot(node[0], node[1], 'o', markersize=3, color=color)
    plt.savefig(f'coupleTree-{0}.png', bbox_inches='tight')
    # Initialize table data
    all_data = []
    
    for level in range(0, steps + 1):
        lines = []  # All lines for this level across all trees
        current_level_parents = []
        current_level_nodes = []
        couples = []    
        males = []
        females = []
        offpring_cnt = 0
        current_level_nodes_and_forfathers = {}
        current_forfather_fraction = {}
        for node in all_nodes[-1]:
            gender = node[2]
            if gender == 1:
                females.append(node)
            elif gender == 2:
                males.append(node)
        couples, singles = mating_function(males, females, child_parent)
        if len(couples) == 0:
            print('No couples, population cannot grow')
            break
        for single in singles:
            all_data.append([level, single, single[2], '-'])
            
        parents_to_parent_node = {}
        for couple in couples:
            
            # Add current known data to table
            all_data.append([level, couple[0], couple[0][2], couple[1]])
            all_data.append([level, couple[1], couple[1][2], couple[0]])
            
            # Get all forfather nodes from both parents
            forfather1 = nodes_and_forfathers[couple[0]]
            forfather2 = nodes_and_forfathers[couple[1]]
            forfathers = []
            for father in forfather1 + forfather2:
                if father not in forfathers:
                    forfathers.append(father)
            
            forfather_fraction = len(forfathers) / N
                

            # Create black node for ea ch couple
            px, py = (couple[0][0] + couple[1][0]) / 2, (couple[0][1] + couple[1][1]) / 2 - 1
            while any((px, py) == pos for pos in current_level_parents):
                px += 4
                
            current_level_nodes_and_forfathers[(px, py, 0)] = forfathers
            current_forfather_fraction[(px, py, 0)] = forfather_fraction
            current_level_parents.append((px, py))
            parents_to_parent_node[(px,py)] = [couple[0], couple[1]]
            current_level_nodes.append((px, py, 0))
            lines.append([(couple[0][0], couple[0][1]), (px, py)])
            lines.append([(couple[1][0], couple[1][1]), (px, py)])
            
        # Generate offspring for the black nodes
        current_level, current_lines, parent_offpring, curr_offspring_cnt, crr_child_parent = generate_offspring(current_level_nodes, level)
        offpring_cnt += curr_offspring_cnt
        current_level_nodes.extend(current_level)
        lines.extend(current_lines)
        all_nodes.append(current_level_nodes)
        child_parent.update(crr_child_parent)
         # Add to offpring count table
        tot_num_offpring[level] = offpring_cnt
        
        # Add to offspring dictionary
        for parent in parent_offpring:
            for child in parent_offpring[parent]:
                nodes_and_forfathers[child] = current_level_nodes_and_forfathers[parent]
                forfather_fraction_d[child] = current_forfather_fraction[parent]
        
        print('Level:', level, 'N:', N)
        # Draw lines
        lc = LineCollection(lines, colors='black', linewidths=0.5)
        ax.add_collection(lc)
     
        # Draw nodes
        for node in current_level_nodes:
            color = get_color(node[2])
            ax.plot(node[0], node[1], 'o', markersize=3, color=color)
        
        #input("Press Enter to plot the next point...")      
        #plt.pause(0.9)  
    plt.savefig('coupleTreeN2.png')
    plt.show()
    return all_nodes, tot_num_offpring, nodes_and_forfathers, all_data, forfather_fraction_d

all_nodes_1, tot_num_offpring_1, nodes_and_forfathers_1, all_data_1, forfather_fraction_1 = draw_trees(3, 5)



