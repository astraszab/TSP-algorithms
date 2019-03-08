# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 07:06:58 2019

@author: astar
"""

import random
import math
import matplotlib.pyplot as plt
from time import clock



class Ant:
    
    def __init__(self, map_):
        self.map = map_
        self.path = []
        self.path_length = math.inf
        
        
    def run(self):
        self.path = []
        pheromone_map = [self.map.pheromones[row][:] for row in range(len(self.map.pheromones))]
        current_node = random.choice(range(len(self.map.nodes)))
        self.path.append(current_node)
        for row in range(len(pheromone_map)):
            pheromone_map[row][current_node] = 0
        for i in range(len(self.map.nodes) - 1):
            current_node = random.choices(range(len(self.map.nodes)), weights = pheromone_map[self.path[-1]])[0]
            self.path.append(current_node)
            for row in range(len(pheromone_map)):
                pheromone_map[row][current_node] = 0
        self.path_length = distance([self.map.nodes[i] for i in self.path])
        
            
    def get_path_length(self):
        return self.path_length
    
    
    def get_path(self):
        return self.path



class TSPMap:
    
    def __init__(self, num_of_ants = 1, size = 10, auto_generate = True, source = "", evaporating_rate = 0):
        self.ants = [Ant(self) for i in range(num_of_ants)]
        if auto_generate:
            self.nodes = TSPMap.generate_nodes(size)
        else:
            self.nodes = self.read_nodes(source)
        self.pheromones = [[1 for i in range(len(self.nodes))] for j in range(len(self.nodes))]
        for i in range(len(self.pheromones)):
            self.pheromones[i][i] = 0
        self.evaporating_rate = evaporating_rate
        self.optimal_path = []
        self.optimal_length = math.inf
        self.optimal_history = []
        
        
    def generate_nodes(size):
        nodes = [(random.uniform(0, size), random.uniform(0, size)) for i in range(size)]
        return nodes
    
    
    def read_nodes(self, source):
        with open(source, 'r') as file:
            lines = file.readlines()
            path = [(float(line.split()[0]), float(line.split()[1])) for line in lines]
            return path
    
    
    def run(self, trials):
        for trial in range(trials):
            for ant in self.ants:
                ant.run()
            optimal_ant = min(self.ants, key = Ant.get_path_length)
            self.update_pheromones(optimal_ant)
            self.optimal_path = optimal_ant.get_path()
            self.optimal_length = optimal_ant.get_path_length()
            self.optimal_history.append(self.optimal_length)    
            
             
    def update_pheromones(self, optimal_ant):
        self.pheromones = [[self.pheromones[i][j] * (1 - self.evaporating_rate) 
                            for j in range(len(self.pheromones))] for i in range(len(self.pheromones))]
        path = optimal_ant.get_path()
        for i in range(len(path) - 1):
            self.pheromones[path[i]][path[i + 1]] += 1 / optimal_ant.get_path_length()
            self.pheromones[path[i + 1]][path[i]] += 1 / optimal_ant.get_path_length()
        if len(path) > 0 and path[0] != path[-1]:
            self.pheromones[path[0]][path[-1]] += 1 / optimal_ant.get_path_length()
            self.pheromones[path[-1]][path[0]] += 1 / optimal_ant.get_path_length()
                
                
    def get_optimal_history(self):
        return self.optimal_history
    
    
    def get_optimal_path(self):
        return [self.nodes[i] for i in self.optimal_path]
    
    
    def get_optimal_distance(self):
        return self.optimal_distance
        
        
       
def distance(path):
    dist = 0
    for i in range(len(path) - 1):
        dist += math.sqrt(math.pow(path[i][0] - path[i + 1][0], 2) + math.pow(path[i][1] - path[i + 1][1], 2))
    dist += math.sqrt(math.pow(path[0][0] - path[-1][0], 2) + math.pow(path[0][1] - path[-1][1], 2))
    return dist



if __name__ == "__main__":
    NUM_OF_ANTS = 20
    SIZE = 10
    NUM_OF_TRIALS = 200
    EVAPORATING_RATE = 0.1
    SOURCE = f'{SIZE}.txt'
    start = clock()
#    map_ = TSPMap(num_of_ants=NUM_OF_ANTS, size=SIZE, evaporating_rate=EVAPORATING_RATE)
    map_ = TSPMap(num_of_ants=NUM_OF_ANTS, evaporating_rate=EVAPORATING_RATE, auto_generate=False, source=SOURCE)
    map_.run(NUM_OF_TRIALS)
    end = clock()
    history = map_.get_optimal_history()
    path = map_.get_optimal_path()
    path.append(path[0])
    X = [path[i][0] for i in range(len(path))]
    Y = [path[i][1] for i in range(len(path))]
    
    plt.figure(1, figsize=(6, 10))
    plt.subplot(211)
    plt.title('Learning curve\n'
              f'Number of ants: {NUM_OF_ANTS}\n'
              f'Number of trials: {NUM_OF_TRIALS}\n'
              f'Evaporating rate: {EVAPORATING_RATE}\n'
              f'Found solution: {history[-1]}\n'
              f'Working time: {end - start}')
    plt.xlabel('trials')
    plt.ylabel('optimal path length')
    plt.plot(history)
    plt.subplot(212)
    plt.title('Optimal path')
    plt.plot(X, Y)

    