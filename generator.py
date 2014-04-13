# Author: Samuel Maskell <samuelmaskell@gmail.com> 
# Based on work by: Ali Assaf <ali.assaf.mail@gmail.com>
# Copyright: (C) 2014 Samuel Maskell
# License: GNU General Public License <http://www.gnu.org/licenses/>

from itertools import product
from random import shuffle

from solver import solve_sudoku

def print_grid(grid):
    for row in grid:
        print row

def gen_rand_start_grid(size):
    N = size*size
    first_block = range(1,N+1)
    first_row = range(1,N+1)
    first_col = range(1,N+1)
    shuffle(first_block)
    grid = [[0 for __ in xrange(N)] for __ in xrange(N)]
    for i in range(size):
        for j in range(size):
            curr = first_block.pop()
            grid[i][j] = curr
            if i == 0:
                first_row.remove(curr)
            if j == 0:
                first_col.remove(curr)
    shuffle(first_col)
    shuffle(first_row)
    for i in range(size,N):
        grid[0][i] = first_row.pop()
        grid[i][0] = first_col.pop()
    return grid

def remove_clues(size, grid):
    N = size*size
    entries = list(product(range(N), range(N)))
    shuffle(entries)
    for row,col in entries:
        entry = grid[row][col]
        grid[row][col] = 0
        solutions = solve_sudoku(size, grid)
        zero_sols = True
        try:
            next(solutions)
            zero_sols = False
            next(solutions)
            grid[row][col] = entry
        except StopIteration:
            if zero_sols:
                grid[row][col] = entry
    return grid

def gen_rand_grid(size):
    return remove_clues(size, next(solve_sudoku(size, gen_rand_start_grid(size), shuffle_rows=True)))

if __name__ == "__main__":
    for i in xrange(1):
        x = gen_rand_grid(3)
        print_grid(x)

