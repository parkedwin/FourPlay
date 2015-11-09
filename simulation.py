### Simple Simulation for Connect Four
import matplotlib.pyplot as plt
import numpy as np
import random

class Connect4Simulation():

	def __init__(self, players, x = 5, y = 5, z = 7, conn_num = 4):
		self.board = [[[] for j in range(y)] for i in range(x)]
		self.players = players
		self.height = z
		self.rownum = x
		self.colnum = y
		self.conn_num = conn_num

	def addBlock(self, player, action):
		x = action[0]
		y = action[1]
		if y < self.colnum and x < self.rownum and x >= 0 and y >= 0:
			column = self.board[x][y] # is column set by reference or value?
			if len(column) < self.height:
				column.append(player)
				return
		raise AssertionError("Cannot add to this column")

	def hasSpace(self, x, y):
		if y < self.colnum and x < self.rownum and x >= 0 and y >= 0:
		  if len(self.board[x][y]) < self.height:
		  	return True
		return False

	def getBlock(self, i, j, k):
		if j < self.colnum and i < self.rownum and j >= 0 and i >= 0:
		  if k < len(self.board[i][j]) and k >= 0:
			return self.board[i][j][k]
		return None

	def checkRowWin(self,allRows):
		for row in allRows:
			if row.count(row[0]) == len(row):
				return row[0]
		return None

	#Think about better time complexity ...
	def returnWinner(self):
		conn_num = self.conn_num
		for k in range(self.height):
			for i in range(self.rownum):
				for j in range(self.colnum):
					player = self.getBlock(i, j, k)
					if player is not None:
						allRows = []
						#go down column to check for win
						allRows.append([self.getBlock(i+num,j,k) for num in range(0, conn_num)])
						#go down row to check for win
						allRows.append([self.getBlock(i,j+num,k) for num in  range(0, conn_num)])
						#go down z_col to check for win
						allRows.append([self.getBlock(i,j,k+num) for num in range(0, conn_num)])
						#go down diagonals
						allRows.append([self.getBlock(i+num,j+num,k) for num in range(0, conn_num)])
						allRows.append([self.getBlock(i+num,j,k+num) for num in range(0, conn_num)])
						allRows.append([self.getBlock(i,j+num,k+num) for num in range(0, conn_num)])
						allRows.append([self.getBlock(i+num,j+num,k+num) for num in range(0, conn_num)])

						#other diagonals T_T
						allRows.append([self.getBlock(i+num,j-num,k) for num in range(0, conn_num)])
						allRows.append([self.getBlock(i+num,j,k-num) for num in range(0, conn_num)])
						allRows.append([self.getBlock(i,j+num,k-num) for num in range(0, conn_num)])

						allRows.append([self.getBlock(i-num,j+num,k+num) for num in range(0, conn_num)])
						allRows.append([self.getBlock(i+num,j-num,k+num) for num in range(0, conn_num)])
						allRows.append([self.getBlock(i+num,j+num,k-num) for num in range(0, conn_num)])

						result = self.checkRowWin(allRows)
						if result is not None:
							return result
		return None

	# action defined as (row, col) pair to add to a column
	def getLegalActions(self):
		actions = []
		for i in range(self.rownum):
			for j in range(self.colnum):
				if self.hasSpace(i,j):
					actions.append((i, j))
		return actions

	def generateSuccessor(self, player, action):
		newState = copy.deepcopy(self)
		if player in newState.players and action in newState.getLegalActions():
			newState.addBlock(player, action)
		else:
			raise AssertionError("Invalid Player/action")
		return newState

	# Temporary function for checking if our algorithm works in 2D connect four.
	def display2DBoard(self):
		# grid = np.zeros((self.rownum, self.height))
		# for i in range(len(self.board)):
		# 	for k in range(len(self.board[i][0])):
		# 		grid[i][k] = self.board[i][0][k] + 1 # because 0 is empty, 1 is player 1, 2 is player 2
		grid = np.zeros((self.rownum, self.height))
		for i in range(len(self.board)):
			for k in range(len(self.board[i][0])):
				grid[self.rownum - i - 1][self.height - k - 1] = self.board[i][0][k] + 1
		print grid.transpose()
		self.display2DBoardSingleFrame(grid.transpose())

	def display2DBoardSingleFrame(self, grid):
		dim_x, dim_y = grid.shape
		column_labels = range(dim_x)
		row_labels = range(dim_y)
		fig, ax = plt.subplots()
		print(plt.cm.Blues)
		heatmap = ax.pcolor(grid, cmap = 'YlGnBu')
		print grid.shape
		ax.set_xticks(np.arange(grid.shape[0] - 1), minor = False)
		ax.set_yticks(np.arange(grid.shape[1]), minor = False)
		ax.invert_yaxis()
		plt.grid()
		plt.show()



'''
OUTSIDE THE CLASS
'''
def simulate2D():
	game = Connect4Simulation(['O', 'X'], y = 1)
	turns = 20
	gameIsOver = False
	for i in range(turns):
		if gameIsOver:
			break
		for player in range(2):
			action = random.choice(game.getLegalActions())
			game.addBlock(player, action)
			print action
			game.display2DBoard()
			winner = game.returnWinner()
			if winner is not None:
				print "Player %s won!" % game.players[winner]
				gameIsOver = True
				break

