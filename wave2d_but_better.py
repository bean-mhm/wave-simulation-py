"""

This is a more optimized and experimental version of wave2d.py.
Modify the on_update() function to add custom behavior.

Repo:
https://github.com/bean-mhm/wave-simulation-py

"""

import time
import numpy as np
import matplotlib
import matplotlib.pyplot as plt



# Grid resolution
nx, ny = 140, 140

# Minimum distance in the grid
step = 0.01

# Grid dimensions
dims = [(nx - 1) * step, (ny - 1) * step]

# Propagation speed in 2D
speed = 10.0

# Minimum wavelength
# At least 8 steps needed for a perfectly smooth spherical wave.
min_wavelength = step * np.sqrt(2.0) * 8.0

# Maximum frequency
max_frequency = speed / min_wavelength

# Maximum timestep
max_dt = step / (speed * np.sqrt(2.0))

# Timestep
dt = 0.95 * max_dt

# Time elapsed in the simulation world
total_time = 0

# Stiffness
# Must be greater than or equal to 1 to function properly.
# The formula is made up and likely not physically correct.
stiffness = 1.0

# Print some details
print(f'res = {nx} x {ny}')
print(f'dims = {dims[0]:.3f} m x {dims[1]:.3f} m')
print(f'{step = :.3f} m')
print(f'{speed = :.3f} m/s')
print(f'{min_wavelength = :.3f} m')
print(f'{max_frequency = :.3f} Hz')
print(f'{max_dt = :.9f} s')
print(f'{dt = :.9f} s')
print(f'{stiffness = :.1f}')



# Initial values
u = np.zeros(shape=(nx, ny), dtype=np.float32, order='C')

# Previous values
u_last = np.copy(u)



# Shifting functions

def shift_2d_x_fill(arr: np.ndarray, num, fill_value = 0.0):
    result = np.empty_like(arr)
    if num > 0:
        result[:num] = fill_value
        result[num:] = arr[:-num]
    elif num < 0:
        result[num:] = fill_value
        result[:num] = arr[-num:]
    else:
        result[:] = arr
    return result

def shift_2d_y_fill(arr, num, fill_value = 0.0):
    result = np.empty_like(arr)
    if num > 0:
        for x in range(np.shape(arr)[0]):
            result[x][:num] = fill_value
            result[x][num:] = arr[x][:-num]
    elif num < 0:
        for x in range(np.shape(arr)[0]):
            result[x][num:] = fill_value
            result[x][:num] = arr[x][-num:]
    else:
        result[:] = arr
    return result

# Get bound value from an array, returns the default value for
# out-of-bound indices.
def get_bound(arr, index: int, default=0.0):
    if index < 0 or index >= len(arr):
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
    global total_time
    
    # Calculate what should be the second partial derivative of
    # u(x, y, t) with respect to t. I shouldn't call it
    # acceleration.
    
    # Note that we're finding the central finite difference here.
    
    acc = \
        ((shift_2d_x_fill(u, -1) - u) - (u - shift_2d_x_fill(u, 1))) \
        + ((shift_2d_y_fill(u, -1) - u) - (u - shift_2d_y_fill(u, 1)))
        
    acc *= (speed**2) / (step**2)
    
    # Calculate the current "velocity" (first order derivative)
    vel = (u - u_last) / dt
    
    # Adjust the velocity based on the acceleration
    vel += (acc * dt)
    
    # Stiffen
    vel *= (stiffness ** (-dt))
    
    # Update the values
    u_last = np.copy(u)
    u += (vel * dt)
    
    # Update the total sim time elapsed
    total_time += dt
    
    # Do arbitrary things to the wave field
    on_update()

# Optionally modify the values after every iteration. Everything
# here is just an experiment.
def on_update():    
    osc_types = [
        'value'
    ]

    if 'value' in osc_types:
        value_freq = max_frequency * 1.0
        u[nx//2, ny//2] = np.sin(2*np.pi * value_freq * total_time) * 1.0
    
    if 'monopole' in osc_types:
        monopole_value = 1.2
        monopole_travel_dist = 0.03
        monopole_travel_max_freq = speed / (2*np.pi * monopole_travel_dist)
        monopole_travel_freq = 0.7 * monopole_travel_max_freq
        
        # max speed = 2pi * travel_freq * travel_dist
        
        pos_x = np.sin(2*np.pi * monopole_travel_freq * total_time) * monopole_travel_dist + (dims[0] / 2.0)
        
        index_x = int(np.floor(pos_x / step))
        u[index_x, ny//2] = monopole_value



# Visualize

plt.ion()
fig = plt.figure()
img: matplotlib.image.AxesImage = plt.imshow(u.T, cmap='twilight', interpolation='bicubic')
img.set_clim(vmin=-.8, vmax=.8)

itersPerSecond = 60.0
secondsPerIter = 1.0 / itersPerSecond

render_iter = 0
last_render_time = time.time()

while 1:
    if time.time() - last_render_time >= secondsPerIter:
        last_render_time = time.time()
        
        if render_iter not in range(0, 0):
            increment()
            img.set_data(u.T)
            #img.autoscale()
        
        render_iter += 1

    fig.canvas.flush_events()
