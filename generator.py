# Author: Samuel Maskell <samuelmaskell@gmail.com> 
# Copyright: (C) 2014 Samuel Maskell
# License: GNU General Public License <http://www.gnu.org/licenses/>

from itertools import product
from random import shuffle
import subprocess
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
    for row in covered_rows:
        r,c,n = cover_rows[row]
        grid[r][c] = changed[(r,c)]

def run__dlx_process(X,Y, grid):
    rows_used = set()
    for val in X.itervalues():
        for row in val:
            rows_used.add(row)

    rows = []
    popen = subprocess.Popen(["./dlx"], shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
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
        print_grid_with_rows(rows, [int(i) for i in line.strip().split(" ")], grid)


if __name__ == "__main__":
    grids = []
    for i in xrange(500):
        grids.append(gen_rand_grid(3))
    for i, grid in enumerate(grids):
        m = open("sat/minimal/sat%03d.cnf"%(i+1),"w")
        clauses = sudoku_to_sat(grid,False)
        for clause in clauses:
            m.write(" ".join(clause))
            m.write("\n")
        m.close()

        e = open("sat/extended/sat%03d.cnf"%(i+1),"w")
        clauses = sudoku_to_sat(grid,True)
        for clause in clauses:
            e.write(" ".join(clause))
            e.write("\n")
        e.close()

        c = open("cover/sat%03d.txt"%(i+1),"w")
        X,Y, sol = sudoku_to_cover(3, grid)
        print_cover(X,Y,c)
        c.close()

