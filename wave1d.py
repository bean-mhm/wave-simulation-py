"""

This is a 1D wave simulation test for education, it is by no means
optimized, and I don't fully guarantee its correctness.

Repo:
https://github.com/bean-mhm/wave-simulation-py

"""

import math
import numpy as np
import matplotlib.pyplot as plt
import time



# Number of points on the string
n = 30

# Distance between each point
dx = 0.5

# Propagation speed
c = 10



# Initial values / vertical positions of the points
pos = [0.0] * n

# Previous values / positions
pos_last = pos.copy()



# Maximum timestep
# dt <= (dx / c)
max_dt = dx / c

# Timestep
dt = 0.5 * max_dt

# Stiffness
# Must be greater than or equal to 1 to function properly.
# The formula is made up and likely not physically correct.
stiffness = 10.0

# Time elapsed in the simulation world
total_time = 0



# Get bound value from an array, returns the default value for
# out-of-bound indices.
def get_bound(arr, index: int, default=0.0):
    if (index < 0 or index >= len(arr)):
        return default
    return arr[index]

# Advance the simulation by dt
def increment():
    global pos
    global pos_last
    global total_time
    
    # Make a backup of the current positions
    temp = pos.copy()
    
    # Create an array to store the velocities
    vel = [0.0] * n
    
    # We could alternate between two buffers instead of copying
    # and allocating new arrays every iteration, but I'm not
    # focusing on performance here.
    
    # You can also precalculate constant coefficients outside the loop.

    # Go through the points
    for i in range(n):
        # Calculate the second derivative with respect to x
        grad = ((get_bound(pos, i + 1) - get_bound(pos, i)) -
                (get_bound(pos, i) - get_bound(pos, i - 1))) / (dx**2)
        
        # Calculate how much we need to adjust the velocity
        acc = c**2 * grad

        # Get the current velocity
        vel[i] = (pos[i] - pos_last[i]) / (dt)
        
        # Adjust the velocity
        vel[i] += acc * dt
        
        # "Stiffen"
        vel[i] /= stiffness**dt
    
    # Go through the points and adjust the positions based on the
    # velocities that we calculated before
    for i in range(n):
        pos[i] += vel[i] * dt

    # Use the backup we made before
    pos_last = temp
    
    total_time += dt
    
    # Oscillate a specific point
    osc_time = 3.0
    if (total_time < osc_time):
        strength = 1.0 - (total_time / osc_time)
        
        amp = 0.3 * strength
        freq = 40 * strength
        
        pos[10] = math.sin(total_time * freq) * amp

# Make an interactive plot
plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_ylim([-1.0, 1.0])
line1, = ax.plot(pos, '-o')

# Update the plot

stepsPerSecond = 30.0
secondsPerStep = 1.0 / stepsPerSecond

last = time.time()
while 1:
    if time.time() - last >= secondsPerStep:
        last = time.time()
        
        increment()
        
        line1.set_ydata(pos)

    fig.canvas.draw()
    fig.canvas.flush_events()
