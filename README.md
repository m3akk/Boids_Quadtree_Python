# Boids with Quadtree optimization


<p align="center">
  <img src="https://github.com/m3akk/Boids_Quadtree_Python/assets/120716573/eccb7028-de37-493b-aee8-feb9a9349b82" alt="python boids">
</p>




Boids with Quadtree Optimization is a program that implements the simulation of bird flock behavior using the Boids (Bird-oid) algorithm and optimization using a quadtree data structure.
The Boids algorithm is inspired by the behavior of flocks of birds in nature. Each bird (boid) moves according to several rules:
1. Separation: The bird repels other birds that are too close to it to avoid collisions.
2. Following: The bird tends to follow the direction of movement of the birds in its vicinity.
3. Cohesion: A bird tends to stay close to other birds in order to maintain the integrity of the flock.
This program additionally uses a quadtree data structure to optimize performance. A Quadtree is a hierarchical data structure that divides space into smaller square regions to reduce search complexity. Each region can contain multiple birds, and if the region is considered far enough away and contains a large number of birds, only the midpoint of the region is used as a proxy for all birds within that region.
The basic features of the program are:
1. Initialization: The program initializes the initial state of the birds, i.e. their positions and speeds, and the quadtree structure.
2. Computation of behavior: Each step of the simulation, the program applies separation, tracking and coherence rules to each bird. The rules are applied taking into account only birds that are close to the current bird, which is optimized by using a quadtree structure.
3. Update of positions: Based on the calculated speed changes, the program updates the positions of the birds.
4. Drawing: The program uses a graphical interface to display the simulation. Birds are shown as simple shapes (eg circles) that move on the screen.




