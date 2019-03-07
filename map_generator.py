# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 12:53:34 2019

@author: astar
"""

import random



if __name__ == '__main__':

    SIZE = 20
    WIDTH = 5000
    HEIGHT = 5000

    path = [f'{random.uniform(0, WIDTH)} {random.uniform(0, HEIGHT)}\n' for i in range(SIZE)]

    with open(f'{SIZE}.txt', 'w') as file:
        file.writelines(path)
