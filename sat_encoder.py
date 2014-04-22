def encode(x,y,z, bar):
	# assert 0<x<10 and 0<y<10 and 0<z<10
	neg = "~" if bar else ""
	return neg + "r%dc%dn%d"%(x,y,z)

#There is at least one number in each entry
def entry_least(clauses):
	for x in range(1,10):
		for y in range(1,10):
			curr = []
			for z in range(1,10):
				curr.append(encode(x,y,z,False))
			clauses.append(curr)

#There is at most one number in each entry			
def entry_most(clauses):
	for x in range(1,10):
		for y in range(1,10):
			for z in range(1,9):
				for i in range(z+1,10):
					clauses.append([encode(x,y,z,True),encode(x,y,i,True)])

#Each number appears at most once in each row
def row_most(clauses):
	for y in range(1,10):
		for z in range(1,10):
			for x in range(1,9):
				for i in range(x+1,10):
					clauses.append([encode(x,y,z,True),encode(i,y,z,True)])

#Each number appears at least once in each row
def row_least(clauses):
	for y in range(1,10):
		for z in range(1,10):
			curr = []
			for x in range(1,10):
				curr.append(encode(x,y,z,False))
			clauses.append(curr)

#Each number appears at most once in each column
def column_most(clauses):
	for x in range(1,10):
		for z in range(1,10):
			for y in range(1,9):
				for i in range(y+1,10):
					clauses.append([encode(x,y,z,True),encode(x,i,z,True)])

#Each number appears at least once in each column
def column_least(clauses):
	for x in range(1,10):
		for z in range(1,10):
			curr = []
			for y in range(1,10):
				curr.append(encode(x,y,z,False))
			clauses.append(curr)

#Each number appears at most once in each 3x3 sub-grid
def sub_grid_most(clauses):
	for z in range(1,10):
		for i in range(0,3):
			for j in range(0,3):
				for x in range(1,4):
					for y in range(1,4):
						for k in range(y+1,4):
							clauses.append([encode(3*i+x,3*j+y,z,True),encode(3*i+x,3*j+k,z,True)])
						for k in range(x+1,4):
							for l in range(1,4):
								clauses.append([encode(3*i+x,3*j+y,z,True),encode(3*i+k,3*j+l,z,True)])

#Each number appears at least once in each 3x3 sub-grid
def sub_grid_least(clauses):
	for z in range(1,10): #for each number
		for i in range(0,3):
			for j in range(0,3): #for each sub-grid
				curr = []
				for x in range(1,4):
					for y in range(1,4):
						curr.append(encode(3*i+x,3*j+y,z,False)) #number is in at least one of the spots
				clauses.append(curr)
					

def minimal_encoding(clauses):
	entry_least(clauses)
	row_most(clauses)
	column_most(clauses)
	sub_grid_most(clauses)
	
def extended_encoding(clauses):
	minimal_encoding(clauses)
	entry_most(clauses)
	row_least(clauses)
	column_least(clauses)
	sub_grid_least(clauses)

def filled_in(clauses,puzzle):
	for i,row in enumerate(puzzle):
		for j,num in enumerate(row):
			if num:
				clauses.append([encode(i+1,j+1,num,False)])

def sudoku_to_sat(grid, extended=False):
	clauses = []
	if extended:
		extended_encoding(clauses)
	else:
		minimal_encoding(clauses)
	filled_in(clauses, grid)
	return clauses