# Author: Samuel Maskell <samuelmaskell@gmail.com> 
# Copyright: (C) 2014 Samuel Maskell
# License: GNU General Public License <http://www.gnu.org/licenses/>

from itertools import product
from random import shuffle
import subprocess
import time
from sat_encoder import sudoku_to_sat

from solver import solve_sudoku, sudoku_to_cover, print_cover
from dlx import solve_sudoku as dlx_solver

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

def check_grid_valid(size, grid):
    rows = [set() for __ in xrange(size*size)]
    cols = [set() for __ in xrange(size*size)]
    blocks = [set() for __ in xrange(size*size)]
    for r,row in enumerate(grid):
        for c,col in enumerate(row):
            block = (r / size) * size + (c / size)
            rows[r].add(col)
            cols[c].add(col)
            blocks[block].add(col)
    for row in rows:
        if len(row) != size*size:
            return False
    for col in cols:
        if len(col) != size*size:
            return False
    for block in blocks:
        if len(block) != size*size:
            return False
    return True

def print_grid_with_rows(cover_rows, covered_rows, grid):
    changed = {}
    for row in covered_rows:
        r,c,n = cover_rows[row]
        changed[(r,c)] = grid[r][c]
        grid[r][c] = n
    print_grid(grid)
    print
    # if not check_grid_valid(3,grid):
    #     print "bad"
    # else:
    #     print "good"
    # print
    for row in covered_rows:
        r,c,n = cover_rows[row]
        grid[r][c] = changed[(r,c)]

def run_process(X,Y, grid):
    rows_used = set()
    for val in X.itervalues():
        for row in val:
            rows_used.add(row)

    rows = []
    popen = subprocess.Popen(["./a.out"], shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    popen.stdin.write("%d %d\n"%(len(rows_used),len(X)))
    for row, cols in Y.items():
        if row not in rows_used:
            continue
        rows.append(row)
        for col in X:
            if col in cols:
                popen.stdin.write("1 ")
            else:
                popen.stdin.write("0 ")
        popen.stdin.write("\n")
    for line in popen.stdout.readlines():
        yield rows, [int(i) for i in line.strip().split(" ")]
        # print_grid_with_rows(rows, [int(i) for i in line.strip().split(" ")], grid)


if __name__ == "__main__":
    # grids = []
    # for i in xrange(100):
    #     grids.append(gen_rand_grid(3))
    # start_time = time.time()
    # for grid in grids:
    #     for sol in solve_sudoku(3, grid):
    #         pass
    # print "python time:",time.time() - start_time, "seconds"
    # start_time = time.time()
    # for grid in grids:
    #     X,Y, sol = sudoku_to_cover(3, grid)
    #     for sol in run_process(X,Y,grid):
    #         pass
    # print "c++ time:",time.time() - start_time, "seconds"

    # print_grid(x)
    # dlx_solver(2,x)
    x = gen_rand_grid(3)
    # X,Y,sol = sudoku_to_cover(3, x)
    # print_cover(X,Y)
    clauses = sudoku_to_sat(x,False)
    for clause in clauses:
        print " ".join(clause)
    # run_process(X,Y,x)
    # for sol in solve_sudoku(2, x):
    #     print_grid(sol)

