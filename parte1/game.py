from search import *
from copy import deepcopy

# TAI color
# no color = 0
# has color > 0
def get_no_color():
	return 0
def no_color(c):
	return c == 0
def color(c):
	return c > 0

# TAI pos
def make_pos(l, c):
	return (l, c)
def pos_l(pos):
	return pos[0]
def pos_c(pos):
	return pos[1]

#	Return:  List with all the groups of pieces in this board O(MN)
# Made with a stack in order to prevent non optimized python recursion overflows
def board_find_groups(board):
	res = []
	m = deepcopy(board)
	def floodfill(x, y, oC, nC):
		stack = [make_pos(x,y)]
		resF = []
		while len(stack) > 0:
			x, y = stack.pop()
			if m[x][y] != oC:
				continue
			resF = resF + [make_pos(x,y)]
			m[x][y] = nC
			if(y < len(m[0]) - 1):
				stack.append(make_pos(x,y+1))  # baixo
			if(x > 0):
				stack.append(make_pos(x-1,y))  # esquerda
			if(y > 0):
				stack.append(make_pos(x,y-1))  # cima
			if(x < len(m) - 1):
				stack.append(make_pos(x+1,y))  # direita
		return resF
	return [floodfill(l,c,m[l][c],-1) for l in range(0,len(m)) for c in range(0,len(m[0])) if(color(m[l][c]))]

#	Removes given group from board and "compresses" the board accordingly
#	Return: Modified board
def board_remove_group(searchBoard, searchGroup):
	newBoard = deepcopy(searchBoard)
	#Minimum and maximum column index to update
	min_col = -1
	max_col = -1

	#Set all the coordinates in the group to 0 and the interval of modified columns
	for coord in searchGroup:
		newBoard[pos_l(coord)][pos_c(coord)] = get_no_color()
		if (min_col == -1 or pos_c(coord) < min_col):
			min_col = pos_c(coord)

		if (max_col == -1 or pos_c(coord) > max_col):
			max_col = pos_c(coord)

	#Stores the indexes of empty columns
	emptyColumns = []
	#Update only modified columns
	for c in range(min_col, max_col+1, 1):
		lastLine = -1
		#Update each column from bottom to top
		for l in range(len(newBoard)-1, -1, -1):
			#If there is no color and lastLine is invalid, validate it
			if (no_color(newBoard[l][c]) and lastLine == -1):
				lastLine = l
			#If a color is found and lastLine is valid, move it to bottom of board
			if (color(newBoard[l][c]) and lastLine != -1):
				newBoard[lastLine][c] = newBoard[l][c]
				newBoard[l][c] = get_no_color()
				lastLine -= 1

		#If column is empty, add column index to emptyColumns
		if (lastLine == len(newBoard) - 1):
			emptyColumns.append(c)

	#Shift the board left once for every emptyColumn index
	for emptyIndex in range(0, len(emptyColumns)):
		for c in range(emptyColumns[emptyIndex] - emptyIndex, len(newBoard[0])-1, 1):
			for l in range(len(newBoard)):
				newBoard[l][c] = newBoard[l][c+1]
				newBoard[l][c+1] = get_no_color()
	return newBoard

class sg_state:
	"""
	Holds the state of a board
	"""
	def __init__(self, newBoard):
		self.board = deepcopy(newBoard)
		self.groups = board_find_groups(newBoard)
	def __lt__(self, other_state):
		thisStateCount = sum(color(self.board[l][c]) for l in range(len(self.board)) for c in range(len(self.board[0])))
		otherStateCount = sum(color(self.board[l][c]) for l in range(len(self.board)) for c in range(len(self.board[0])))
		return thisStateCount < otherStateCount

class same_game(Problem):
	"""
	Models a Same Game problem as a satisfaction problem.
	A solution cannot have pieces left on the board.
	"""
	def __init__(self, newBoard):
		self.board = deepcopy(newBoard)
		self.initial = sg_state(newBoard)

	def actions(self, state):
		return [state.groups[i] for i in range(len(state.groups)) if len(state.groups[i]) >= 2]

	def result(self, state, action):
		return sg_state(board_remove_group(state.board, action))

	def goal_test(self, state):
		# ha grupos?
		#super.goal_test(state)
		return state.groups == []

	def path_cost(self, c, state1, action, state2):
		#Cost of going from state1 to state2
		#Como avaliar o custo?
		return c + 1

	def h(self, node):
		return len(node.state.groups) # Heuristica possivel (mas pode haver melhores)