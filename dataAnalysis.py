from matplotlib import cm
from matplotlib.collections import LineCollection
import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate
import gwtreewithmatingfunction as gwtmf
import gwtree as gwt

# Generate tree
#all_nodes, tot_num_offpring, nodes_and_forfathers, all_data, forfather_fraction = gwtmf.draw_trees(100, 20)

# Export to a file
# with open("NodesAndForfathers.txt", "w") as f:
    
# with open("ForFatherFraction.txt", "w") as f:
#     f.write(tabulate(forfather_fraction.items(), headers=['Node', 'Forfather Fraction']))

# with open('All Data.txt', 'w') as f:
#     f.write(tabulate(all_data, headers=['Level', 'Node', 'Gender', 'Mate']))
    
# with open('Total Number of Offspring.txt', 'w') as f:
#     f.write(tabulate(tot_num_offpring.items(), headers=['Level', 'Total number of offspring']))

# Distributions
# Define outcomes
outcomes = np.array([0, 1, 2, 3])



# # For EV = 1
# # 0.56 + 0.14 + 0.10 + 0.15 + 0.042 + 0.006 +( 0.002)
# p_ev1 = np.array([0.56, 0.14, 0.10, 0.15, 0.042,0.006, 0.002])

# For EV < 1




# Plotting sub, critical and supercritical distributions

fig, (ax1, ax2, ax3) = plt.subplots(1, 3)

# Critical
tree1, lines1, offspring_per_generation = gwt.generate_tree(15, [0.35, 0.35, 0.25, 0.05])

x1 = [i for i in range(0, 16)]
y1 = offspring_per_generation

colors = colors = cm.viridis(np.linspace(0, 1, 3))
ax1.plot(x1, y1, 'o-', markersize=3, color=colors[0])

variance = np.sum((outcomes - 1) ** 2 * np.array([0.35, 0.35, 0.25, 0.05]))

def f(n):
    return 2/(variance*n)

ax1.plot(x1, [f(i) for i in x1], '-', markersize=2, color='black')
print(f(12))


# Super critical
tree2, lines2, offspring_per_generation2 = gwt.generate_tree(15, [0.1, 0.35, 0.40, 0.15])



y2 = offspring_per_generation2

ax2.plot(x1, y2, 'o-', markersize=3, color=colors[1])


# Sub critical
tree3, lines3, offspring_per_generation3 = gwt.generate_tree(15, [0.40, 0.40, 0.15, 0.05])

y3 = offspring_per_generation3

ax3.plot(x1, y3, 'o-', markersize=3, color=colors[2])

plt.show()



# # Plotting 
# fig_analysis_1, ax_analysis_1 = plt.subplots()

# # # 1

# x_values1 = [10, 50, 10**2, 500, 10**3]
# y_values1 = [5, 7940, 22204, 135922, 320143]

# #y = [10: stofnin dó út eftir 1. kynslód svo 1: 5]
# # 50:{0: 67, 1: 80, 2: 92, 3: 122, 4: 143, 5: 172, 6: 196, 7: 256, 8: 310, 9: 393, 10: 503, 11: 692, 12: 919, 13: 1190, 14: 1581, 15: 2074, 16: 2719, 17: 3614, 18: 4673, 19: 6072, 20: 7940}
# # [100:{0: 121, 1: 166, 2: 214, 3: 269, 4: 333, 5: 420, 6: 557, 7: 717, 8: 864, 9: 1137, 10: 1507, 11: 1906, 12: 2580, 13: 3341, 14: 4309, 15: 5655, 16: 7459, 17: 9688, 18: 12740, 19: 16715, 20: 22204}
# # 500: {0: 634, 1: 804, 2: 1040, 3: 1349, 4: 1840, 5: 2377, 6: 2985, 7: 3865, 8: 5105, 9: 6684, 10: 8825, 11: 11371, 12: 14759, 13: 19536, 14: 25951, 15: 34156, 16: 45103, 17: 59329, 18: 78296, 19: 103815, 20: 135922}
# # 1000: {0: 1285, 1: 1650, 2: 2211, 3: 2930, 4: 3758, 5: 4984, 6: 6502, 7: 8449, 8: 11027, 9: 14393, 10: 18762, 11: 24146, 12: 31698, 13: 41975, 14: 55417, 15: 73714, 16: 97255, 17: 128936, 18: 170587, 19: 224993, 20: 297141}

# # for num_root_nodes in x_values1:
# #     all_nodes, tot_num_offspring, nodes_and_forfathers, all_data = gwtmf.draw_trees(num_root_nodes, 20)
# #     y_values1.append(list(tot_num_offspring)[-1])  # Get the number of nodes in generation 20

# colors = cm.viridis(np.linspace(0, 1, 1))
# ax_analysis_1.plot(x_values1, y_values1, 'o', color=colors[0],  markersize=3)
# ax_analysis_1.set_title('Vöxtur trjáa sem fall af fjölda róta')
# ax_analysis_1.set_xlabel('Fjöldi róta')
# ax_analysis_1.set_ylabel('Fjöldi afkvæma í 20. kynslóð')

# # 2

# fig_analysis_2, ax_analysis_2 = plt.subplots()

# colors = cm.viridis(np.linspace(0, 1, 10))  # Generates 10 colors from the 'viridis' colormap

# for index, i in enumerate([50, 100, 500, 1000]):  # For each number of root nodes
#     all_nodes, tot_num_offpring, nodes_and_forfathers, all_data, forfather_fraction = gwtmf.draw_trees(i, 20)
#     # Calculate average forfather fraction across all nodes in each generation
#     avg_forfather_fractions = []
#     for generation in range(1, 21):  # Assuming 20 generations
#         generation_forfather_fractions = []
#         for node in all_nodes[generation]:
#             if node in forfather_fraction:
#                 # Calculate the fraction for each node as unique ancestors / total possible ancestors
#                 node_fraction = forfather_fraction[node]
#                 generation_forfather_fractions.append(node_fraction)
        
#         # Calculate the average fraction for the generation
#         if generation_forfather_fractions:
#             avg_fraction = sum(generation_forfather_fractions) / len(generation_forfather_fractions)
#             avg_forfather_fractions.append(avg_fraction)
#         else:
#             avg_forfather_fractions.append(0)  # Handle generations with no nodes
    
#     x_values2 = range(1, len(avg_forfather_fractions) + 1)

#     # Use the color from the generated colormap
#     ax_analysis_2.plot(x_values2, avg_forfather_fractions, 'o-', markersize=3, color=colors[index], label=f'N = {i}')

# ax_analysis_2.set_xlabel('Kynslóð')
# ax_analysis_2.set_ylabel('Meðal forföðurhlutfall')
# ax_analysis_2.legend(loc='best')  # Adds a legend to distinguish between the different lines
# plt.show()