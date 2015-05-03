from itertools import product

class Node:
	def __init__(self):
		self.name = None
		self.col_header = None
		self.up = self
		self.down = self
		self.left = self
		self.right = self

class ColHeader:

	def __init__(self):
		self.name = None
		self.up = self
		self.down = self
		self.left = self
		self.right = self
		self.size = 0

class H:
	def __init__(self):
		self.name = None
		self.up = self
		self.down = self
		self.left = self
		self.right = self

def add_col_with_name(h, name):
	curr = ColHeader()
	curr.name = name
	curr.left = h.left
	curr.right = h
	h.left.right = curr
	h.left = curr

def init_col_headers(h,N):
	for row,col in product(range(N),range(N)):
		add_col_with_name(h, ("cell", row, col))
	for row,n in product(range(N),range(1,N+1)):
		add_col_with_name(h,("row", row, n))
	for col,n in product(range(N),range(1,N+1)):
		add_col_with_name(h,("col", col, n))
	for block,n in product(range(N),range(1,N+1)):
		add_col_with_name(h,("block", block, n))

def select(col):
	# print "selecting col", col.name
	col.right.left = col.left
	col.left.right = col.right

	row = col.down
	while row!=col:
		right = row.right
		while right!=row:
			right.col_header.size -= 1
			right.up.down = right.down
			right.down.up = right.up
			right = right.right
		row = row.down

	# print "done selecting col", col.name

def deselect(col):
	# print "deselecting col", col.name
	row = col.up
	while row!=col:
		left = row.left
		while left!=row:
			left.up.down = left
			left.down.up = left
			left.col_header.size += 1
			left = left.left
		row = row.up

	col.right.left = col
	col.left.right = col
	# print "done deselecting col", col.name

def find_col(h, i, j):
	col = h.right
	while col!= h:
		if col.name == ("cell",i,j):
			return col
		col = col.right

def build_graph(size, grid):
	N = size*size
	h = H()
	init_col_headers(h,N)
	for r, c, n in product(range(N), range(N), range(1, N + 1)):
		b = (r / size) * size + (c / size) # Box number
		col = h.right
		row = None
		# print "on row",r,c,n
		while col != h:
			if (col.name == ("cell", r, c) or
				col.name == ("row", r, n) or
				col.name == ("col", c, n) or
				col.name == ("block", b, n)):
				new_node = Node()
				row = row or new_node
				new_node.col_header = col

				new_node.name = (r,c,n)
				new_node.up = col.up
				new_node.down = col
				new_node.right = row
				new_node.left = row.left

				row.left.right = new_node
				row.left = new_node

				col.up.down = new_node
				col.up = new_node

				col.size += 1
			col = col.right
	for i,row in enumerate(grid):
		for j,num in enumerate(row):
			if num:
				# print "removing constraints for",i,j,num
				col = find_col(h, i, j)
				select(col)
	return h

def choose_next_col(h):
	return h.left

def search(h, sol, depth):
	# print "at depth", depth
	if h.right == h:
		print "found solution"
		yield sol
		return
	col = choose_next_col(h)
	select(col)
	# print "removing col ", col.name

	row = col.down
	row_count = 0
	while row != col:
		row_count += 1
		row = row.down
	row = row.down
	# print "depth", depth, "chosen col has", row_count,"row"
	row_count = 1
	while row != col:
		# print "depth",depth,"checking row",row_count
		row_count += 1
		sol.append(row.name)
		# print "removing row ", row.name

		right = row.right
		while right != row:
			select(row.col_header)
			right = right.right

		for result in search(h, sol, depth+1):
			yield result

		left = row.left
		while left != row:
			deselect(left.col_header)
			left = left.left
		sol.pop()
		row = row.down
	deselect(col)

def solve_sudoku(size, grid):
	h = build_graph(size, grid)
	sols = 0
	for sol in search(h, [], 0):
		sols += 1
	print sols







