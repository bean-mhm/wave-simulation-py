"""

This is a 3D wave simulation test for education, it is by no means
optimized, and I don't fully guarantee its correctness.

Repo:
https://github.com/bean-mhm/wave-simulation-py

"""

import time
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import plotly.graph_objects as go



# Visualization method
# 'slice': Advance the simulation live and render a 2D slice
# 'volume': Visualize the 3D volume as a whole in constant time
visual = 'slice'

# Z index for slices
slice_z_index = 10

# How many times to increment before volume visualization
volume_iters = 10



# Grid resolution
nx, ny, nz = 20, 20, 20

# Minimum distance in the grid
step = 0.5

# Propagation speed in 3D
speed = 10



# Initial values
u = np.zeros(shape=(nx, ny, nz), dtype=float, order='C')

# Boost a specific point's value
# You can modify this to have different initial values.
u[10, 10, 10] = 1.0

# Previous values
u_last = np.copy(u)

# Velocities
vel = np.zeros(shape=(nx, ny, nz), dtype=float, order='C')



# Maximum timestep
max_dt = step / (speed * np.sqrt(3.0))
print(f'{max_dt = }')

# Timestep
dt = 0.9 * max_dt

# Stiffness
# Must be greater than or equal to 1 to function properly.
# The formula is made up and likely not physically correct.
stiffness = 2.0



# Get bound value from an array, returns the default value for
# out-of-bound indices.
def get_bound(arr, index: int, default=0.0):
    if (index < 0 or index >= len(arr)):
        return default
    return arr[index]

# Get bound value in a multidimensional array
def get_bound_md(arr: np.ndarray, indices: tuple, default=0.0):
    for i in range(len(indices)):
        if indices[i] < 0 or indices[i] >= arr.shape[i]:
            return default
        
    return arr[indices]

# Advance the simulation by dt
def increment():
    global u
    global u_last
    global vel

    # Make a backup of the current values
    temp = np.copy(u)

    # Precalculate constants
    step2 = step**2
    speed2 = speed**2
    stiffen_mul = stiffness ** (-dt)

    # Go through the points
    for z in range(nz):
        for y in range(ny):
            for x in range(nx):
                # Get the current value
                curr = u[x, y, z]
                
                # Calculate the second gradients with respect to x, y, and z
                
                grad_x = ((get_bound_md(u, (x + 1, y, z)) - curr) -
                        (curr - get_bound_md(u, (x - 1, y, z)))) / step2

                grad_y = ((get_bound_md(u, (x, y + 1, z)) - curr) -
                        (curr - get_bound_md(u, (x, y - 1, z)))) / step2
                
                grad_z = ((get_bound_md(u, (x, y, z + 1)) - curr) -
                        (curr - get_bound_md(u, (x, y, z - 1)))) / step2

                # Calculate how much we need to adjust the velocity
                acc = speed2 * (grad_x + grad_y + grad_z)
                
                # Get the current velocity
                currVel = (curr - u_last[x, y, z]) / dt
                
                # Adjust the velocity
                currVel += acc * dt
                
                # "Stiffen"
                currVel *= stiffen_mul
                
                # Store the velocity
                vel[x, y, z] = currVel

    # Go through the points and adjust the values based on the
    # velocities that we calculated before
    for z in range(nz):
        for y in range(ny):
            for x in range(nx):
                u[x, y, z] += vel[x, y, z] * dt

    # Use the backup we made before
    u_last = temp

# Get a 2D slice of the 3D grid
def get_slice():
    global u
    
    slice = np.zeros(shape=(nx, ny), dtype=float, order='C')
    for y in range(ny):
        for x in range(nx):
            slice[x, y] = u[x, y, slice_z_index]
            
    return slice



# Visualize

if visual == 'volume':
    for i in range(volume_iters):
        increment()
    
    X, Y, Z = np.mgrid[:nx, :ny, :nz]

    fig = go.Figure(data=go.Volume(
        x=X.flatten(),
        y=Y.flatten(),
        z=Z.flatten(),
        value=u.flatten(),
        colorscale='twilight',
        isomin=-0.1,
        isomax=0.1,
        opacity=0.1, # needs to be small to see through all surfaces
        surface_count=50, # needs to be a large number for good volume rendering
        ))
    
    fig.show()
    
elif visual == 'slice':
    plt.ion()
    fig = plt.figure()
    img: matplotlib.image.AxesImage = plt.imshow(get_slice().T, cmap='twilight', interpolation='bicubic')
    img.set_clim(vmin=-.1, vmax=.1)

    stepsPerSecond = 30.0
    secondsPerStep = 1.0 / stepsPerSecond
    
    last = time.time()
    while 1:
        if time.time() - last >= secondsPerStep:
            last = time.time()
            
            increment()
            
            img.set_data(get_slice().T)
            #img.autoscale()

        fig.canvas.draw()
        fig.canvas.flush_events()
    
else:
    print('Invalid visualization method')
