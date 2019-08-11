from copy import deepcopy

# reads the input file 'board.txt' and populates the board
# as well as pruning the constraint lists for the already
# given spaces
def readInput(board,constraints):
	row = -1
	col = -1
	with open('board.txt') as inFile:
		for line in inFile:
			row = row + 1
			col = -1
			for char in line.strip():
				col = col + 1
				board[row][col] = int(char)
				if int(char) > 0:
					constraints[row][col] = {int(char)}

# check if a given value at a given (row,col) on the board
# is a valid move, returning True if it is, False if not
def checkValidity(value,row,col):
	cRow = row
	cCol = col
	for x in range(9):
		if x != col:
			if board[cRow][x] == value:
				return False
		if x != row:
			if board[x][cCol] == value:
				return False
	rOffset = int((row / 3)) * 3
	cOffset = int((col / 3)) * 3
	for x in range(3):
		for y in range(3):
			if (x + rOffset != row) and (y + cOffset != col):
				if board[x + rOffset][y + cOffset] == value:
					return False
	return True

# prune the constraint lists consistent with forward checking
# based on the value at (row,col)
# Returns False if any constraint list becomes empty as a result
# of pruning, returns True otherwise
def prune(constraints,value,row,col):
	cRow = row
	cCol = col
	for x in range(9):
		if x != col and (value in constraints[cRow][x]):
			constraints[cRow][x].remove(value)
			if len(constraints[cRow][x]) == 0:
				return False
		if x != row and (value in constraints[x][cCol]):
			constraints[x][cCol].remove(value)
			if len(constraints[x][cCol]) == 0:
				return False
	rOffset = int((row / 3)) * 3
	cOffset = int((col / 3)) * 3
	for x in range(3):
		for y in range(3):
			if (x + rOffset != row) and (y + cOffset != col) and (value in constraints[x + rOffset][y + cOffset]):
				constraints[x + rOffset][y + cOffset].remove(value)
				if len(constraints[x + rOffset][y + cOffset]) == 0:
					return False
	return True

# chooses the next position to fill based on the MRV algorithm
def chooseNext(constraints,visited,first):
	minLength = 10
	minRow = 0
	minCol = 0
	if first == True:
		for row in range(9):
			for col in range(9): 
				if len(constraints[row][col]) > 1:
					visited.append((row,col))
					return (row,col)
	for row in range(9):
		for col in range(9):
			curLen = len(constraints[row][col])
			if curLen < minLength and (row,col) not in visited:
				minLength = curLen
				minRow = row
				minCol = col
	visited.append((minRow,minCol))
	return (minRow,minCol)

# recursive algorithm to solve the given sudoku board
def backTrack(board,constraints,visited,first):
	recursionEnder = True
	for row in board:
		for col in row:
			if col == 0:
				recursionEnder = False
	if recursionEnder:
		return True
	result = False
	row,col = chooseNext(constraints,visited,first)
	for value in constraints[row][col]:
		if checkValidity(value,row,col):
			multiverse = deepcopy(constraints)
			if prune(multiverse, value, row, col):
				board[row][col] = value
				if col == 8:
					result = backTrack(board,multiverse,visited,False)
				else:
					result = backTrack(board,multiverse,visited,False)
			if result == True:
				return True
	board[row][col] = 0
	visited.remove((row,col))
	return False

def solver(board,constraints):
	return backTrack(board,deepcopy(constraints),[],True)

def drawDivide(solid,outWrite):
	for x in range(3):
		for y in range(3):
			if not solid:
				outWrite.write(' ')
			outWrite.write('-')
			if y < 2:
				if solid:
					outWrite.write('----',)
				else:
					outWrite.write('  ')
		if solid:
			outWrite.write('|')
		else:
			outWrite.write(' |')
	outWrite.write('\n')

def drawBoard(board,outWrite):
	row = -1
	for line in board:
		row = row + 1
		if row % 3 == 0:
			drawDivide(True,outWrite)
		else:
			drawDivide(False,outWrite)
		for char in line:
			if char == 0:
				outWrite.write('   |')
			else:
				outWrite.write(' ' + str(char) + ' |')
		outWrite.write('\n')

constraints = [[{1,2,3,4,5,6,7,8,9},{1,2,3,4,5,6,7,8,9},{1,2,3,4,5,6,7,8,9},
{1,2,3,4,5,6,7,8,9},{1,2,3,4,5,6,7,8,9},{1,2,3,4,5,6,7,8,9},
{1,2,3,4,5,6,7,8,9},{1,2,3,4,5,6,7,8,9},{1,2,3,4,5,6,7,8,9}],
[{1,2,3,4,5,6,7,8,9},{1,2,3,4,5,6,7,8,9},{1,2,3,4,5,6,7,8,9},
{1,2,3,4,5,6,7,8,9},{1,2,3,4,5,6,7,8,9},{1,2,3,4,5,6,7,8,9},
{1,2,3,4,5,6,7,8,9},{1,2,3,4,5,6,7,8,9},{1,2,3,4,5,6,7,8,9}],
[{1,2,3,4,5,6,7,8,9},{1,2,3,4,5,6,7,8,9},{1,2,3,4,5,6,7,8,9},
{1,2,3,4,5,6,7,8,9},{1,2,3,4,5,6,7,8,9},{1,2,3,4,5,6,7,8,9},
{1,2,3,4,5,6,7,8,9},{1,2,3,4,5,6,7,8,9},{1,2,3,4,5,6,7,8,9}],
[{1,2,3,4,5,6,7,8,9},{1,2,3,4,5,6,7,8,9},{1,2,3,4,5,6,7,8,9},
{1,2,3,4,5,6,7,8,9},{1,2,3,4,5,6,7,8,9},{1,2,3,4,5,6,7,8,9},
{1,2,3,4,5,6,7,8,9},{1,2,3,4,5,6,7,8,9},{1,2,3,4,5,6,7,8,9}],
[{1,2,3,4,5,6,7,8,9},{1,2,3,4,5,6,7,8,9},{1,2,3,4,5,6,7,8,9},
{1,2,3,4,5,6,7,8,9},{1,2,3,4,5,6,7,8,9},{1,2,3,4,5,6,7,8,9},
{1,2,3,4,5,6,7,8,9},{1,2,3,4,5,6,7,8,9},{1,2,3,4,5,6,7,8,9}],
[{1,2,3,4,5,6,7,8,9},{1,2,3,4,5,6,7,8,9},{1,2,3,4,5,6,7,8,9},
{1,2,3,4,5,6,7,8,9},{1,2,3,4,5,6,7,8,9},{1,2,3,4,5,6,7,8,9},
{1,2,3,4,5,6,7,8,9},{1,2,3,4,5,6,7,8,9},{1,2,3,4,5,6,7,8,9}],
[{1,2,3,4,5,6,7,8,9},{1,2,3,4,5,6,7,8,9},{1,2,3,4,5,6,7,8,9},
{1,2,3,4,5,6,7,8,9},{1,2,3,4,5,6,7,8,9},{1,2,3,4,5,6,7,8,9},
{1,2,3,4,5,6,7,8,9},{1,2,3,4,5,6,7,8,9},{1,2,3,4,5,6,7,8,9}],
[{1,2,3,4,5,6,7,8,9},{1,2,3,4,5,6,7,8,9},{1,2,3,4,5,6,7,8,9},
{1,2,3,4,5,6,7,8,9},{1,2,3,4,5,6,7,8,9},{1,2,3,4,5,6,7,8,9},
{1,2,3,4,5,6,7,8,9},{1,2,3,4,5,6,7,8,9},{1,2,3,4,5,6,7,8,9}],
[{1,2,3,4,5,6,7,8,9},{1,2,3,4,5,6,7,8,9},{1,2,3,4,5,6,7,8,9},
{1,2,3,4,5,6,7,8,9},{1,2,3,4,5,6,7,8,9},{1,2,3,4,5,6,7,8,9},
{1,2,3,4,5,6,7,8,9},{1,2,3,4,5,6,7,8,9},{1,2,3,4,5,6,7,8,9}],]


board = [[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]]
readInput(board,constraints)
outWrite = open('output.txt','w')
outWrite.write("Starting board: \n")
drawBoard(board,outWrite)
results = solver(board,constraints)
if results:
	outWrite.write("\nEnding Board: \n")
	drawBoard(board,outWrite)
else:
	outWrite.write("\nNo solution could be found")