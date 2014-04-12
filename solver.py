# Author: Samuel Maskell <samuelmaskell@gmail.com> 
# Based on work by: Ali Assaf <ali.assaf.mail@gmail.com>
# Copyright: (C) 2014 Samuel Maskell
# License: GNU General Public License <http://www.gnu.org/licenses/>

from itertools import product
from random import shuffle
from collections import defaultdict

def solve_sudoku(size, grid, shuffle_rows=False):
    X,Y,solution = sudoku_to_cover(size, grid)
    for solution in solve(X, Y, solution, shuffle_rows):
        yield cover_to_sudoku(size, solution)

def sudoku_to_cover(size, grid):
    X, Y = gen_initial_contraints(size)  
    # For each cell in the existing puzzle, remove all contraints that
    # are already satisfied
    solution = []
    for i, row in enumerate(grid):
        for j, n in enumerate(row):
            if n != 0:
                solution.append((i,j,n))
                select(X, Y, (i, j, n))
    return X,Y,solution


def cover_to_sudoku(size, cover):
    N = size*size
    grid = [[0 for __ in xrange(N)] for __ in xrange(N)]
    for row,col,num in cover:
        grid[row][col] = num
    return grid


def gen_initial_contraints(size):
    N = size*size
    Y = {}
    # for each row, add an item for the constraints it satisfies
    for row, col, num in product(range(N), range(N), range(1, N + 1)):
        block = (row / size) * size + (col / size) # Box number
        Y[(row, col, num)] = [
            ("cell_constraint", (row, col)),
            ("row_constraint", (row, num)),
            ("column_constraint", (col, num)),
            ("block_constraint", (block, num))]

    # inverse of Y
    X = defaultdict(set)
    for i, row in Y.items():
        for j in row:
            X[j].add(i)

    return X, Y

def solve(X, Y, solution_rows, shuffle_rows):
    if not X:
        yield list(solution_rows)
    else:
        col = min(X, key=lambda c: len(X[c]))
        rows = list(X[col])
        if shuffle_rows:
            shuffle(rows)
        for row in rows:
            solution_rows.append(row)
            cols = select(X, Y, row)
            for solution in solve(X, Y, solution_rows, shuffle_rows):
                yield solution
            deselect(X, Y, row, cols)
            solution_rows.pop()

def select(X, Y, r):
    cols = []
    for j in Y[r]:
        for i in X[j]:
            for k in Y[i]:
                if k != j:
                    X[k].remove(i)
        cols.append(X.pop(j))
    return cols

def deselect(X, Y, r, cols):
    for j in reversed(Y[r]):
        X[j] = cols.pop()
        for i in X[j]:
            for k in Y[i]:
                if k != j:
                    X[k].add(i)