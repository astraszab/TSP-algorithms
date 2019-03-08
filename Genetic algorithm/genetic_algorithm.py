# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 14:43:01 2019

@author: astar
"""

import random 
import math
import matplotlib.pyplot as plt
from time import clock


def generate_random_nodes(size):
    return [(random.uniform(0, size), random.uniform(0, size)) for i in range(size)]


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


def crossover(p1, p2):
    child = []
    i = random.randrange(len(p1) + 1)
    j = random.randrange(len(p1) + 1)
    if i > j:
        i, j = j, i
    cut = p1[i:j]
    k = 0
    while len(child) < i:
        if p2[k] not in cut:
            child.append(p2[k])
        k += 1
    child += cut
    while len(child) < len(p1):
        if p2[k] not in child:
            child.append(p2[k])
        k += 1
    return child 

def mutate(path, mutation_rate):
    while random.random() < mutation_rate:
        i = random.randrange(len(path))
        j = random.randrange(len(path))
        if i > j:
            i, j = j, i
        new_path = path[:i] + path[i:j][::-1] + path[j:]
        return new_path
    return path



if __name__ == '__main__':
    SIZE = 10
    GENERATION_SIZE = 20
    NUMBER_OF_GENERATIONS = 20
    MUTATION_RATE = 0.2
    
    start = clock()
    
#    random.seed(1)
#    path = generate_random_nodes(SIZE)
#    random.seed()
    path = read_map(f'{SIZE}.txt')
    
    history = []
    
    generation = [random.sample(path, k=len(path)) for i in range(GENERATION_SIZE)]
    history.append(distance(min(generation, key=distance)))
    
    for i in range(NUMBER_OF_GENERATIONS):
        weights = [1 / distance(path) for path in generation]
        p1 = min(generation, key=distance)
        generation.remove(p1)
        p2 = min(generation, key=distance)
        offspring = [mutate(crossover(p1, p2), MUTATION_RATE) for j in range(GENERATION_SIZE)]
        generation = offspring
        history.append(distance(min(generation, key=distance)))
        
    end = clock()
    
    path = min(generation, key=distance)
    
    path.append(path[0])
    X = [path[i][0] for i in range(len(path))]
    Y = [path[i][1] for i in range(len(path))]
    
    plt.figure(1, figsize=(6, 10))
    plt.subplot(211)
    plt.title('Learning curve\n'
              f'Generation size: {GENERATION_SIZE}\n'
              f'Number of generations: {NUMBER_OF_GENERATIONS}\n'
              f'Mutation rate: {MUTATION_RATE}\n'
              f'Found solution: {history[-1]}\n'
              f'Working time: {end - start}')
    plt.xlabel('generations')
    plt.ylabel('optimal path length')
    plt.plot(history)
    plt.subplot(212)
    plt.title('Optimal path')
    plt.plot(X, Y)
    