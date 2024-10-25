# Create an animation of a forest fire using cellular automata:

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib import colors

# Assign the cells:
empty_cell, tree_cell, fire_cell = 0, 1, 2
# Chance of a tree setting on fire by 'lightning':
lightning = 0.0001
# Chance of a tree growing out of an empty space:
tree_growth = 0.05
# Dimensions for the forest grid:
ny = 100
nx = 100
# The neighbourhood of cells (von Neumann neighbourhood):
neighbourhood = ((-1, 0), (0, -1), (0, 1), (1, 0))

def update_state(X): 
    """Update the forest according to the forest-fire rules."""
    # Make a grid of zeros (empty cells):
    X1 = np.zeros_like((X))
    # For a cell at row y, column x in grid (forest):
    for ix in range(1, nx-1):
        for iy in range(1, ny-1):
             # An empty cell grows into a tree cell:             
            if X[iy, ix] == empty_cell and np.random.random() <= tree_growth:
                X1[iy, ix] = tree_cell
            # A tree cell remains a tree cell:
            if X[iy, ix] == tree_cell:
                X1[iy, ix] = tree_cell
                # Add the fire spread mechanics:
                for dx, dy in neighbourhood:
                    if X[iy + dy, ix + dx] == fire_cell:
                        X1[iy, ix] = fire_cell
                        break
                # Add the lightning strike probability:
                if X[iy, ix] == tree_cell and np.random.random() <= lightning:
                    X1[iy, ix] = fire_cell
                    
    return X1

# Create a forest of empty cells:
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


            
            
                
            
            
           