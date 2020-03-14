"""
Name: <Jinho Lee>
Uni: <jl5027>
"""

# The function signatures are named for the questions they represent, for
# instance p1 is problem 1. Please do not modify any of the function signatures
# as they will be used for grading purposes
from typing import List, Any

import numpy as np


def p1(k: int) -> str:
    facString = ""
    while k >= 1:
        j = k
        for i in range(1, k):
            j = j*i
        facString += str(j)
        if (k!=1):
            facString += str(",")
        k -= 1

    return facString
    #the function signature indicates that p1 takes in an int k and returns a string
    pass


def p2_a(x: list, y: list) -> list:
    y.sort(reverse=True)
    y.pop()
    return y
    pass


def p2_b(x: list, y: list) -> list:
    x.reverse()
    return x
    pass


def p2_c(x: list, y: list) -> list:
    comb = list(set(x+y))
    comb.sort()
    return comb
    pass


def p2_d(x: list, y: list) -> list:
    l1 = [x, y]
    return l1
    pass


def p3_a(x: set, y: set, z: set) -> set:
    union = set(x | y | z)
    return union
    pass


def p3_b(x: set, y: set, z: set) -> set:
    intersec = set(x&y&z)
    return intersec
    pass

def p3_c(x: set, y: set, z: set) -> set:
    union = set(x | y | z)
    intersec = set((x & y) | (x & z) | (y & z))
    sortedSet = set(union - intersec)
    return sortedSet
    pass


def p4_a() -> np.array:
    positions = [[1,1,1,1,1], [1,0,0,0,1], [1,0,2,0,1], [1,0,0,0,1], [1,1,1,1,1]]
    board = np.array(positions)
    return board
    pass


def p4_b(x: np.array) -> list:
    """knightMove = [(-2,-1),(-2,1),(2,1),(2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]"""
    coordinates = []
    size = len(x) - 1
    for i in range(0, len(x)):
        for j in range(0,len(x)):
            if x[i][j] == 1:
                if (0 <= i - 2 <= size) and (0 <= j - 1 <= size):
                    if x[i-2][j-1] == 2:
                        coordinates.append((i,j))
                if (0 <= i - 2 <= size) and (0 <= j + 1 <= size):
                    if x[i-2][j+1] == 2:
                        coordinates.append((i,j))
                if (0 <= i + 2 <= size) and (0 <= j + 1 <= size):
                    if x[i+2][j+1] == 2:
                        coordinates.append((i,j))
                if (0 <= i + 2 <= size) and (0 <= j - 1 <= size):
                    if x[i+2][j-1] == 2:
                        coordinates.append((i,j))
                if (0 <= i + 1 <= size) and (0 <= j + 2 <= size):
                    if x[i+1][j+2] == 2:
                        coordinates.append((i,j))
                if (0 <= i + 1 <= size) and (0 <= j - 2 <= size):
                    if x[i+1][j-2] == 2:
                        coordinates.append((i,j))
                if (0 <= i - 1 <= size) and (0 <= j + 2 <= size):
                    if x[i-1][j+2] == 2:
                        coordinates.append((i,j))
                if (0 <= i - 1 <= size) and (0 <= j - 2 <= size):
                    if x[i-1][j-2] == 2:
                        coordinates.append((i,j))
    return coordinates
    pass


def p5_a(x: dict) -> int:
    isolated = []
    for i in x:
        if not x[i] :
            isolated += i

    return len(isolated)
    pass


def p5_b(x: dict) -> int:
    accessible = []
    for i in x:
        if x[i] :
            accessible += i
    return len(accessible)
    pass


def p5_c(x: dict) -> list:
    paths = []
    for i in x:
        for neighbor in x[i]:
            paths.append((i, neighbor))
    output = []
    for a,b in paths:
        output.append((a,b))
    for a,b in output:
        output.remove((b,a))
    return output
    pass


def p5_d(x: dict) -> np.array:
    keys = sorted(x.keys())
    size = len(x)
    matrix = np.zeros([size,size], dtype=int)
    for a, b in [(keys.index(a), keys.index(b)) for a, row in x.items() for b in row]:
        matrix[a][b] = 2 if (a == b) else 1
    return matrix
    pass

#Question 6
class PriorityQueue(object):
    def __init__(self):
        self.menu = {
            'apple': [5],
            'banana': [4.5],
            'carrot': [3.3],
            'kiwi': [7.4],
            'orange': [5],
            'mango': [9.1],
            'pineapple': [9.1]
        }
        self.pq = []
        pass

    def push(self, x):
        self.pq.append(x)
        pass

    def pop(self):
        highest = 0
        if not self.is_empty():
            for i in range(0, len(self.pq)):
                for j in range(0,len(self.pq)):
                    if self.menu[self.pq[i]] < self.menu[self.pq[j]]:
                        highest = j
            return self.pq.pop(highest)
        else:
            return "There's nothing to dequeue in the priority queue"
        pass

    def is_empty(self):
        return len(self.pq) == 0
        pass


if __name__ == '__main__':
    print(p1(8))
    print('-----------------------------')
    print(p2_a(x=[], y=[1, 3, 5]))
    print(p2_b(x=[2, 4, 6], y=[]))
    print(p2_c(x=[1, 3, 5, 7], y=[1, 2, 5, 6]))
    print(p2_d(x=[1, 3, 5, 7], y=[1, 2, 5, 6]))
    print('------------------------------')
    print(p3_a(x={1, 3, 5, 7}, y={1, 2, 5, 6}, z={7, 8, 9, 1}))
    print(p3_b(x={1, 3, 5, 7}, y={1, 2, 5, 6}, z={7, 8, 9, 1}))
    print(p3_c(x={1, 3, 5, 7}, y={1, 2, 5, 6}, z={7, 8, 9, 1}))
    print('------------------------------')
    print(p4_a())
    print(p4_b(p4_a()))
    print('------------------------------')
    graph = {
        'A': ['D', 'E'],
        'B': ['E', 'F'],
        'C': ['E'],
        'D': ['A', 'E'],
        'E': ['A', 'B', 'C', 'D'],
        'F': ['B'],
        'G': []
    }
    print(p5_a(graph))
    print(p5_b(graph))
    print(p5_c(graph))
    print(p5_d(graph))
    print('------------------------------')
    pq = PriorityQueue()
    pq.push('apple')
    pq.push('kiwi')
    pq.push('orange')
    while not pq.is_empty():
        print(pq.pop())
