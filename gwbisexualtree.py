from matplotlib.collections import LineCollection
import numpy as np
import matplotlib.pyplot as plt

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

# Function to generate the tree structure
def generate_tree(steps=5):
    tree_levels = [[(0, 0)]]  # Starting point of the tree (x, y) coordinates
    gender_levels = [[0]]
    lines = []  # To store lines connecting nodes
    
    
    for level in range(1, steps + 1):
        current_level = []
        current_gender_level = []
        for parent_index, (px, py) in enumerate(tree_levels[level - 1]):
            fate = np.random.choice(['die', 'stay', 'split'], p=[0.25, 0.25, 0.5])
            offspring_count = simulate_bacterium(fate)
            for child in range(offspring_count):
                gender_fate = np.random.choice(['f', 'm'], p=[0.5, 0.5])
                gender = simulate_gender(gender_fate)
                current_gender_level.append(gender)
                # Strakar og stelpur : lita með 0.5 likum annan lit
                # Calculate new position for child
                cx = px + child - offspring_count / 2 + 0.5 * (offspring_count - 1)
                cy = py - 1  # Move down the y-axis for child nodes
                while (cx, cy) in current_level:
                    cx += 1  # Increment cx until a unique position is found
                current_level.append((cx, cy))
                
                # Add line from parent to child
                lines.append([(px, py), (cx, cy)])
        tree_levels.append(current_level)
        gender_levels.append(current_gender_level)
    return tree_levels, lines, gender_levels

def get_color(gender):
    if ( gender == 1):
        return 'red'
    elif ( gender == 2):
        return 'blue'
    else:
        return 'black'

# Generate tree and lines
tree_levels, lines, gender_levels = generate_tree(steps=10)  # Reduced steps for simplicity
print(gender_levels)
# Plotting
fig, ax = plt.subplots()
lc = LineCollection(lines, colors='black', linewidths=0.5)
ax.add_collection(lc)


min_value = 0
max_value = 0
chldr_cnt = []
# Plot nodes
for i, level in enumerate(tree_levels):
    chldr_cnt.append(len(level))
    # Separate x and y coordinates for plotting
    xs, ys = zip(*level) if level else ([], [])
    if xs: 
        if min(xs) < min_value:
            min_value = min(xs)
        if max(xs) > max_value:
            max_value = max(xs)
    for child, (x, y) in zip(gender_levels[i], level):
        ax.plot(x, y, 'o', markersize=3, color=get_color(child))

def mating_function(available_males, available_females, child_parent):
    couples = []
    singles = []
    random.shuffle(available_males)
    random.shuffle(available_females)

    for male in available_males:
        siblings = []
        print('Finding mate for', male)
        for female in available_females:
            print('Checking female', female)
            if child_parent != {}:
                if child_parent[male] == child_parent[female]:
                    siblings.append(female)
                    print('Sibling found, skipping...', female)
                    break
            
        print('Checking if male has sibling')
        if siblings:
            print('siblings:', siblings)
            couples.append([male, siblings[0]])                
    
    if len(available_males) > len(couples):
        singles.extend(available_males[len(couples):])
    elif len(available_females) > len(couples):
        singles.extend(available_females[len(couples):])
    
    return couples, singles
# Add text labels for each generation
for i in range(len(tree_levels)):
    x = min_value - 5
    y = i * -1
    ax.text(x, y, r'$Z_{%s}$ = %s' % (i, chldr_cnt[i]), verticalalignment='center')

# Set the limits of the plot to show all contents
if xs:
    ax.set_xlim(min_value - 6, max_value + 2)
else:
    ax.set_xlim(-6, 6)
ax.set_ylim(-len(tree_levels), 1)

plt.axis('off')
plt.show()