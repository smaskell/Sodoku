# Authod: Samuel Maskell <samuelmaskell@gmail.com> 
# Based on work by: Ali Assaf <ali.assaf.mail@gmail.com>
# Copyright: (C) 2014 Samuel Maskell
# License: GNU General Public License <http://www.gnu.org/licenses/>

from itertools import product
from random import shuffle

def solve_sudoku(size, grid, shuffle_rows=False):
    X, Y = gen_initial_contraints(size)  
    # convert problem to desired format
    A = exact_cover(X, Y)
    # For each cell in the existing puzzle, remove all contraints that
    # are already satisfied
    for i, row in enumerate(grid):
        for j, n in enumerate(row):
            if n != 0:
                select(A, Y, (i, j, n))
    for solution in solve(A, Y, [], shuffle_rows):
        for (row, col, num) in solution:
            grid[row][col] = num
        yield grid

def gen_initial_contraints(size):
    N = size*size
    # Generate list of all constraints
    X = []
    for row, col in product(range(N),range(N)):
        X.append(("cell_constraint", (row, col)))
    for iden, num in product(range(N), range(1, N + 1)):
        X.append(("row_constraint",(iden, num)))
        X.append(("column_constraint", (iden, num)))
        X.append(("block_constraint", (iden, num)))
    Y = {}
    # for each row, add an item for the constraints it satisfies
    for row, col, num in product(range(N), range(N), range(1, N + 1)):
        block = (row / size) * size + (col / size) # Box number
        Y[(row, col, num)] = [
            ("cell_constraint", (row, col)),
            ("row_constraint", (row, num)),
            ("column_constraint", (col, num)),
            ("block_constraint", (block, num))]
    return X, Y

def exact_cover(X, Y):
    X = {j: set() for j in X}
    for i, row in Y.items():
        for j in row:
            X[j].add(i)
    return X

def solve(X, Y, solution, shuffle_rows):
    if not X:
        yield list(solution)
    else:
        c = min(X, key=lambda c: len(X[c]))
        rows = list(X[c])
        if shuffle_rows:
            shuffle(rows)
        for r in rows:
            solution.append(r)
            cols = select(X, Y, r)
            for s in solve(X, Y, solution, shuffle_rows):
                yield s
            deselect(X, Y, r, cols)
            solution.pop()

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