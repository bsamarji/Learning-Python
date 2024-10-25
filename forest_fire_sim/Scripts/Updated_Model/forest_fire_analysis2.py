# Analyse how tree growth and lightning strike probabilities effect the steady-state. 

# packages:
import numpy as np
import matplotlib.pyplot as plt
from statistics import mean

# empty lists to add the mean number of trees and fires to for each iteration:
mean_trees = []
mean_fires = []

# assign probabilities of tree growth and lightning:
lightning = 0.0001
tree_growth = 0.05

def analysis(tree_growth, lightning):
    # assign the cells:
    empty_cell, tree_cell, fire_cell = 0, 1, 2
    # dimensions for the forest grid:
    ny = 100
    nx = 100
    # how many time steps the simulation will run for:
    NUMBER_OF_STEPS = 100
    # the neighbourhood of cells (von Neumann neighbourhood):
    # the neighbourhood of cells (Moore neighbourhood):
    neighbourhood = ((-1,-1), (-1,0), (-1,1), (0,-1), (0, 1), (1,-1), (1,0), (1,1))

    # function that updates the forest according to the forest fire model:
    def update_state(X): 
        """Update the forest according to the forest-fire model."""

        # Make a grid of zeros (empty cells):
        X1 = np.zeros_like((X))

        th1 = 0 # tree counter 
        fh1 = 0 # fire counter

        # for a cell at row y, column x in grid (forest):
        for ix in range(1, nx-1):
            for iy in range(1, ny-1):
                 # an empty cell grows into a tree cell:             
                if X[iy, ix] == empty_cell and np.random.random() <= tree_growth:
                    X1[iy, ix] = tree_cell
                    th1 += 1
                # a tree cell remains a tree cell:
                if X[iy, ix] == tree_cell:
                    X1[iy, ix] = tree_cell
                    th1 += 1
                    # add the fire spread mechanics:
                    for dx, dy in neighbourhood:
                        if abs(dx) == abs(dy) and np.random.random() < 0.6:
                            continue
                        if X[iy + dy, ix + dx] == fire_cell:
                            X1[iy, ix] = fire_cell
                            fh1 += 1
                            th1 -= 1
                            break
                    # add the lightning strike probability:
                    if X[iy, ix] == tree_cell and np.random.random() <= lightning:
                        X1[iy, ix] = fire_cell
                        fh1 += 1
                        th1 -= 1 

        return X1, th1, fh1

    # create lists to record the tree and fire counts (they both start at zero):
    # this is to replicate a forest growing from scratch!
    tree_history = [0]
    fire_history = [0]
    # create a forest of empty cells:
    X = np.zeros((ny, nx))

    # a loop that simulates the update_state function (per number of steps):
    for t in range(1, NUMBER_OF_STEPS):
            X, th, fh = update_state(X)
            # add tree count and fire count to their repsective lists every iteration:
            tree_history.append(th)
            fire_history.append(fh)
   
    return tree_history, fire_history

# run analysis on tree growth probability:
for i in range(1, 101):
    th, fh = analysis(i / 100, lightning)
    mean_trees.append(mean(th))
    mean_fires.append(mean(fh))
    
plt.figure()
plt.plot(mean_trees, label = 'tree cells')
plt.plot(mean_fires, label = 'fire cells')
plt.xlabel('Tree Growth Probability')
plt.ylabel('Average Number of Cells')
plt.legend()
plt.savefig("tree_growth.png")

# Reset the lists:
mean_trees = []
mean_fires = []

# run analysis on lightning strike probability:
for i in range(1, 101):
    th, fh = analysis(tree_growth, i / 10000)
    mean_trees.append(mean(th))
    mean_fires.append(mean(fh))

plt.figure()
plt.plot(mean_trees, label = 'tree cells')
plt.plot(mean_fires, label = 'fire cells')
plt.xlabel('Lightning Strike Probability')
plt.ylabel('Average Number of Cells')
plt.legend()
plt.savefig("lightning.png")
plt.show()  
