# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 20:03:31 2019

@author: astar
"""

import random
import math
import matplotlib.pyplot as plt
from time import clock


def generate_random_nodes(size):
    return [(random.uniform(0, size), random.uniform(0, size)) for i in range(size)]


def mutate(path):
    i = random.randrange(len(path))
    j = random.randrange(len(path))
    if i > j:
        i, j = j, i
    new_path = path[:i] + path[i:j][::-1] + path[j:]
    return new_path


def run_annealing(initial_path, trials, initial_temperature, cooling_rate):
    history = [distance(initial_path)]
    path = initial_path[:]
    temperature = initial_temperature
    for trial in range(trials):
        new_path = mutate(path)
        delta = (distance(new_path) - distance(path)) / distance(path)
        try:
            if math.exp(-delta / temperature) > random.random():
                path = new_path
        except:
            pass
        temperature *= cooling_rate
        history.append(distance(path))
    return path, history


def read_map(source):
    with open(source, 'r') as file:
        lines = file.readlines()
        path = [(float(line.split()[0]), float(line.split()[1])) for line in lines]
        return path
        
        
def distance(path):
    dist = 0
    for i in range(len(path) - 1):
        dist += math.sqrt(math.pow(path[i][0] - path[i + 1][0], 2) + math.pow(path[i][1] - path[i + 1][1], 2))
    dist += math.sqrt(math.pow(path[0][0] - path[-1][0], 2) + math.pow(path[0][1] - path[-1][1], 2))
    return dist



if __name__ == "__main__":
    INITIAL_TEMPERATURE = 0.05
    SIZE = 50
    COOLING_CONSTANT = 0.99997
    NUMBER_OF_ITERATIONS = 100000
    
    start = clock()
    
#    random.seed(1)
#    path = generate_random_nodes(SIZE)
#    random.seed()
    path = read_map(f'{SIZE}.txt')
    
    path, history = run_annealing(path, NUMBER_OF_ITERATIONS, INITIAL_TEMPERATURE, COOLING_CONSTANT)
    
    end = clock()
    
    path.append(path[0])
    X = [path[i][0] for i in range(len(path))]
    Y = [path[i][1] for i in range(len(path))]
    
    plt.figure(1, figsize=(6, 10))
    plt.subplot(211)
    plt.title('Learning curve\n'
              f'Initial temperature: {INITIAL_TEMPERATURE}\n'
              f'Number of trials: {NUMBER_OF_ITERATIONS}\n'
              f'Cooling rate: {COOLING_CONSTANT}\n'
              f'Found solution: {history[-1]}\n'
              f'Working time: {end - start}')
    plt.xlabel('trials')
    plt.ylabel('optimal path length')
    plt.plot(history)
    plt.subplot(212)
    plt.title('Optimal path')
    plt.plot(X, Y)