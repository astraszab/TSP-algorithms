**Ant colony optimization** is a probabilistic technique for solving computational problems which can be reduced to finding good paths through graphs. 
[Read on Wikipedia](https://en.wikipedia.org/wiki/Ant_colony_optimization_algorithms)

In this version of ACO I update a pheromone map based on the best result in iteration only. The version that updates it based on each result  according to its length didn't work as well as this. 

In the tests folder you can see the best results I got for different graph sizes with visual representations of learning curves and paths themselves.

Since the algorithm is pretty slow for graphs with 100+ nodes, I'm looking for a way to parallelize calculations. All ants from a single iteration run independently from each other, so they can be processed separately. If you know how to parallelize class methods in python and want to contribute and explain, please contact me.
