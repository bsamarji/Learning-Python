# Create a forest fire animation using cellular automata. 
# packages:
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib import colors

# assign the cells:
empty_cell, tree_cell, fire_cell = 0, 1, 2
# chance of a tree setting on fire by 'lightning':
lightning = 0.0001
# chance of a tree growing out of an empty space:
tree_growth = 0.05
# dimensions for the forest grid:
ny = 100
nx = 100
# how many time steps the simulation will run for:
NUMBER_OF_STEPS = 500
# the neighbourhood of cells (Moore neighbourhood):
neighbourhood = ((-1,-1), (-1,0), (-1,1), (0,-1), (0, 1), (1,-1), (1,0), (1,1))

# function that updates the forest according to the forest fire model:
def update_state(X): 
    """Update the forest according to the forest-fire model."""

    # Make a grid of zeros (empty cells):
    X1 = np.zeros_like((X))
    
    # for a cell at row y, column x in grid (forest):
    for ix in range(1, nx-1):
        for iy in range(1, ny-1):
             # an empty cell grows into a tree cell:             
            if X[iy, ix] == empty_cell and np.random.random() <= tree_growth:
                X1[iy, ix] = tree_cell
            # a tree cell remains a tree cell:
            if X[iy, ix] == tree_cell:
                X1[iy, ix] = tree_cell
                # add the fire spread mechanics:
                for dx, dy in neighbourhood:
                    if abs(dx) == abs(dy) and np.random.random() < 0.6:
                        continue
                    if X[iy + dy, ix + dx] == fire_cell:
                        X1[iy, ix] = fire_cell
                        break
                # add the lightning strike probability:
                if X[iy, ix] == tree_cell and np.random.random() <= lightning:
                    X1[iy, ix] = fire_cell
                    
    return X1

# create a forest of empty cells:
X = np.zeros((ny, nx))

# Colours for visualization: brown for empty cell, dark green for tree cell and orange for fire cell. 
# Note that for the colormap to work, this list and the bounds list must be one larger than the number of different values in the array:
colors_list = [(0.2,0,0), (0,0.5,0), (1,0,0), 'orange']
cmap = colors.ListedColormap(colors_list)
bounds = [0,1,2,3]
norm = colors.BoundaryNorm(bounds, cmap.N)

# Generate a figure using matplotlib:
fig = plt.figure(figsize = (25 / 3, 6.25))
ax = fig.add_subplot(111)
ax.set_axis_off()
im = ax.imshow(X, cmap = cmap, norm = norm)

# Create an animation function to produce a frame for each generation:
def animate(i):
    im.set_data(animate.X)
    animate.X = update_state(animate.X)
    
# Bind our grid to the identifier X in the animate function's namespace:
animate.X = X
# Interval between frames (ms):
interval = 100

# Create the animation using the figure we generated and the animate function:
anim = animation.FuncAnimation(fig, animate, interval = interval, frames = 200)
# Visualise the animation:
plt.show()
            
                
    