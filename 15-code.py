#!/usr/bin/env python
# coding: utf-8

import numpy as np
from heapq import *


START = np.array([11, 9, 4, 15, 1, 3, 0, 12, 7, 5, 8, 6, 13, 2, 10, 14])
END = np.array(list(range(1, 16)) + [0])


class Board:
    m = np.zeros(16)

    def __init__(self, m):
        self.m = m
        if not self.is_valid():
            raise Exception("NotValidBoard")

    def is_valid(self):
        return set(self.m.flatten()) == set(np.array(range(16)))

    def has_found(self):
        return np.all(self.m.flatten() == END)
    
    def __hash__(self) -> int:
        s = 0
        for i in self.m:
            s = (s * 29 + i) % 10000019
        return int(s)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return np.all(self.m == other.m)
        else:
            return False
        
    def __repr__(self):
        return self.m.reshape(4, 4).__repr__()
    
    def get_neighbors(self):
        index = int(np.argwhere(self.m == 0))
        neighbors = []
        if index > 3: 
            neighbors.append(copy_and_swap(self.m, index, index - 4))
        if index < 12: 
            neighbors.append(copy_and_swap(self.m, index, index + 4))
        if not index % 4 == 0: 
            neighbors.append(copy_and_swap(self.m, index, index - 1))
        if not (index + 1) % 4 == 0: 
            neighbors.append(copy_and_swap(self.m, index, index + 1))
        return neighbors


def copy_and_swap(original, a: int, b: int):
    m = original.copy()
    if 0 <= a < 16 and 0 <= b < 16:
        tmp = m[a]
        m[a] = m[b]
        m[b] = tmp
    return Board(m)


class Node:
    def __init__(self, a_board: Board, father=0):
        self.board = a_board
        self.father = father
        self.d = 0
        if father != 0 and isinstance(father, self.__class__):
            self.d = father.d + 1
        self._f = -1
        self._f = self.get_f()
        
    def get_f(self) -> int:
        if self._f == -1:
            self._f = self.d + self.h()
        return self._f
    
    def h(self) -> int:
        m_now = self.board.m.reshape(4, 4)
        target = END.reshape(4, 4)
        s = 0
        for i in range(16):
            s += np.sum(np.abs(np.argwhere(target == i) - np.argwhere(m_now == i)))
        return s
    
    def __lt__(self, other) -> bool:
        return self.get_f() < other.get_f()
    
    def __repr__(self):
        return self.board.__repr__()

# 堆优化


start = Node(Board(START), 0)
open_heap = []  # set of nodes to be developed
heappush(open_heap, start)
closed = set()  # set of visited boards
route = []
while len(open_heap) > 0:
    now = heappop(open_heap)
    if len(closed) % 10000 == 0:
        print(f'Step: {len(closed)}, Depth:{now.d}, Eval Func:{now.get_f()}, Closed len:{len(closed)}, '
              f'Opened len:{len(open_heap)}')
        print(now.board)
    closed.add(now.board)
    for neighbor in now.board.get_neighbors():
        if neighbor in closed:
            continue
        if neighbor.has_found():
            print("Excited!")
            print(f'Step: {len(closed)}, Depth:{now.d + 1}, Closed len:{len(closed)}, Opened len:{len(open_heap)}')
            route = [neighbor]
            output = now
            while now != 0:
                route = [now.board] + route
                now = now.father
            for board in route:
                print(board)
            break
        heappush(open_heap, (Node(neighbor, now)))
    if len(route) > 0:
        break
