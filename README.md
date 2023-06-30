# Wave Simulation Experiment in Python

## Introduction

This is a small experiment with wave simulations in up to 3 dimensions. The 3D version can be visualized with a volume rendering technique or by making a 2D slice.

[Here's a Short video I've made about this on YouTube.](https://www.youtube.com/shorts/5mN1zTjf8vo)

[Here's a video demo of what I achieved by experimenting with the code.](https://www.youtube.com/watch?v=JeGbCcvAqc8)

## Performance

You shouldn't expect too much performance out of a single-threaded Python script, but this is enough for getting started. I'm currently working on a C++ version with multithreading and a whole lot of optimizations. We could also utilize discrete GPUs to speed up the simulation even more, since it's fairly parallelizable (kinda sorta).

**Update:** I've added `wave2d_but_better.py` which is more optimized and makes it easier to do random experiments.

**Update:** [Check out the WIP C++ version](https://github.com/bean-mhm/wave-tracing)

## Shadertoy

You can also check out these wave simulation shaders (in GLSL) on Shadertoy:

- [3D Wave Simulation](https://www.shadertoy.com/view/mdBcz3)

![image](https://github.com/bean-mhm/wave-simulation-py/assets/98428255/74693b04-74c5-40fa-b663-e48ba90bfda8)

- [Interactive 2D Wave Simulation](https://www.shadertoy.com/view/mdScW1)

![image](https://github.com/bean-mhm/wave-simulation-py/assets/98428255/93b85d7e-8c78-46bd-8b16-19ea09360444)

## Eye Candy

![Screenshot](images/screenshot-1.png)

![Screenshot](images/screenshot-2.png)

![Screenshot](images/screenshot-3.png)

![Screenshot](images/screenshot-4.png)

## Equation

The following is the general equation that we need to use.

![Equation](images/equation.png)

You can think of u(x, y, z, t) as a function that takes in the position and time, and returns the value at that point and time. The left side of the equation can be thought of as the rate of change *of the rate of change* of the value at that point with respect to time (I just call it acceleration, although it's probably not the best term to use here). The right side is speed^2 times the sum of the second gradients of the value in each dimension, while time stays constant.

## Resources

 - [Wave equation - Wikipedia](https://en.wikipedia.org/wiki/Wave_equation)
 - [Partial derivative - Wikipedia](https://en.wikipedia.org/wiki/Partial_derivative)

## Disclaimer

I am not an expert nor a scientist, just a learner. If you find any mistakes, feel free to create an issue about it.
