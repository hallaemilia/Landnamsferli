from matplotlib.collections import LineCollection
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


# Function to simulate one step for a single bacterium
def simulate_bacterium(fate):
    if fate == "split":
        return 2  # If the bacterium splits, return 2 for two offspring
    elif fate == "stay":
        return 1  # If the bacterium stays, return 1 for itself
    else:
        return 0  # If the bacterium dies, return 0 for no offspring


# Function to generate the tree structure
def generate_tree(steps=5, p_input=[0.1, 0.35, 0.40, 0.15]):
    tree_levels = [[(0, 0)]]  # Starting point of the tree (x, y) coordinates
    lines = []  # To store lines connecting nodes
    offspring_per_generation = [1]
    base_spacing = 30
    min_spacing = 5
    
    for level in range(1, steps+1):
        current_level = []
        current_lines = []
        curr_offspring = 0
        for parent_index, (px, py) in enumerate(tree_levels[level - 1]):
            spacing = base_spacing / level  # Adjusted spacing formula
            offspring_count = np.random.choice([0, 1, 2, 3],p = p_input)
            start_x = px - (offspring_count - 1) * spacing / 2
            curr_offspring += offspring_count
            for child in range(offspring_count):
                # Calculate new position for child
                cx = start_x + child * spacing
                cy = py - 1  # Move down the y-axis for child nodes
                
                while any((cx, cy) == pos for pos in current_level):
                    cx += min_spacing  # Increment cx until a unique position is found
                
                current_level.append((cx, cy))
                
                # Add line from parent to child
                current_lines.append([(px, py), (cx, cy)])
        tree_levels.append(current_level)
        lines.append(current_lines)
        offspring_per_generation.append(curr_offspring)
    return tree_levels, lines

# Generate tree and lines
tree_levels, lines = generate_tree(steps=5)  # Reduced steps for simplicity

# Plotting
fig, ax = plt.subplots()
plt.axis('off')

min_value = 0
max_value = 0
chldr_cnt = []
frames = []
accumulated_lines = []
accumulated_nodes = []
accumulated_texts = []

# Plot nodes
for i, level in enumerate(tree_levels):
    if i < len(lines):
        lc = LineCollection(lines[i], colors='black', linewidths=0.5)
        ax.add_collection(lc)
        accumulated_lines.append(lc)
    chldr_cnt.append(len(level))
    ax.add_collection(lc)
    # Separate x and y coordinates for plotting
    xs, ys = zip(*level) if level else ([], [])

    
    # Adding text for the current level
    if(xs): text_x = min(xs) - 10 if xs else -5
    text = ax.text(text_x, -i, f'$Z_{{{i}}} = {chldr_cnt[i]}$', verticalalignment='center', fontsize=9)
    accumulated_texts.append(text)
    ax.plot(xs, ys, 'ob', markersize=3)
    accumulated_nodes.append(ax.lines[-1])
    
    if(xs): ax.set_xlim(min(xs) - 10, max(xs) + 10)  # Set x limits with some padding
    if(xs): ax.set_ylim(min(ys) - 1, 1)
    
    current_frame = [item for sublist in [accumulated_lines, accumulated_nodes, accumulated_texts] for item in sublist]
    frames.append(current_frame)
    plt.savefig(f'treePlot-{i}.png', bbox_inches='tight')

plt.savefig('treeStatic2.png')
ani = animation.ArtistAnimation(fig, frames, interval=1000, blit=True)
plt.savefig('treeAnimation.png', bbox_inches='tight')


plt.show()

