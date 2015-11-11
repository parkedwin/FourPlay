### Simple Simulation for Connect Four
import matplotlib.pyplot as plt
import numpy as np
import random
import agents
import copy

class Connect4Simulation():

	def __init__(self, players, x = 5, y = 5, z = 7, conn_num = 4):
		self.board = [[[] for j in range(y)] for i in range(x)]
		self.players = players
		self.height = z
		self.rownum = x
		self.colnum = y
		self.conn_num = conn_num

	def getPlayerIndex(self,player):
		if player in self.players:
			return self.players.index(player) + 1
		raise AssertionError("Invalid player")

	def getPlayerID(self,index):
		if index <= len(self.players) and index > 0:
			return self.players[index - 1]
		raise AssertionError("invalid index")

	def addBlock(self, player, action):
		x = action[0]
		y = action[1]
		if y < self.colnum and x < self.rownum and x >= 0 and y >= 0:
			column = self.board[x][y]
			if len(column) < self.height:
				column.append(self.getPlayerIndex(player))
				return
		raise AssertionError("Cannot add to this column")

	def hasSpace(self, x, y):
		if y < self.colnum and x < self.rownum and x >= 0 and y >= 0:
		  if len(self.board[x][y]) < self.height:
		  	return True
		return False

	# -1 means place is no good. 0 means it is open. 1,2 mean player in tile
	def getBlock(self, i, j, k):
		if j < self.colnum and i < self.rownum and j >= 0 and i >= 0:
		  if k < len(self.board[i][j]) and k >= 0:
			return self.board[i][j][k]
		  if k >= 0:
		  	return 0
		return -1

	def getBlock_PlayerID(self, i,j, k):
		if j < self.colnum and i < self.rownum and j >= 0 and i >= 0:
		  if k < len(self.board[i][j]) and k >= 0:
			return self.getPlayerID(self.board[i][j][k])
		  if k >= 0:
		    return "open"
		return "Not Valid position"

	def checkRowWin(self,allRows):
		for row in allRows:
			if row.count(row[0]) == len(row) and row[0] > 0:
				return row[0]
		return None

	def rowsPatterns(self,allRows, patterns,counts):
		for row in allRows:
			if(row in patterns):
				pattern_index = patterns.index(row)
				counts[pattern_index] += 1

	def getAllCounts(self, patterns, patternsize):
		counts = [0] * len(patterns)
		for k in range(self.height):
			for i in range(self.rownum):
				for j in range(self.colnum):
					player = self.getBlock(i, j, k)
					if player > 0:
						allRows = []
						#go down column to check for win
						allRows.append([self.getBlock(i+num,j,k) for num in range(0, patternsize)])
						#go down row to check for win
						allRows.append([self.getBlock(i,j+num,k) for num in  range(0, patternsize)])
						#go down z_col to check for win
						allRows.append([self.getBlock(i,j,k+num) for num in range(0, patternsize)])
						#go down diagonals
						allRows.append([self.getBlock(i+num,j+num,k) for num in range(0, patternsize)])
						allRows.append([self.getBlock(i+num,j,k+num) for num in range(0, patternsize)])
						allRows.append([self.getBlock(i,j+num,k+num) for num in range(0, patternsize)])
						allRows.append([self.getBlock(i+num,j+num,k+num) for num in range(0, patternsize)])

						#other diagonals T_T
						allRows.append([self.getBlock(i+num,j-num,k) for num in range(0, patternsize)])
						allRows.append([self.getBlock(i+num,j,k-num) for num in range(0, patternsize)])
						allRows.append([self.getBlock(i,j+num,k-num) for num in range(0, patternsize)])

						allRows.append([self.getBlock(i-num,j+num,k+num) for num in range(0, patternsize)])
						allRows.append([self.getBlock(i+num,j-num,k+num) for num in range(0, patternsize)])
						allRows.append([self.getBlock(i+num,j+num,k-num) for num in range(0, patternsize)])
						self.rowsPatterns(allRows,patterns,counts)
		return counts

	#Think about better time complexity ...
	def returnWinner(self):
		conn_num = self.conn_num
		for k in range(self.height):
			for i in range(self.rownum):
				for j in range(self.colnum):
					player = self.getBlock(i, j, k)
					if player > 0:
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
							return self.getPlayerID(result)
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
				grid[self.rownum - i - 1][self.height - k - 1] = self.getBlock(i, 0, k)
		print grid.transpose()
		self.display2DBoardSingleFrame(grid.transpose())

	def display2DBoardSingleFrame(self, grid):
		dim_x, dim_y = grid.shape
		column_labels = range(dim_x)
		row_labels = range(dim_y)
		fig, ax = plt.subplots()
		#print(plt.cm.Blues)
		heatmap = ax.pcolor(grid, cmap = 'YlGnBu')
		#print grid.shape
		ax.set_xticks(np.arange(grid.shape[0] - 1), minor = False)
		ax.set_yticks(np.arange(grid.shape[1]), minor = False)
		ax.invert_yaxis()
		plt.grid()
		plt.show()

	def getScore(self):
		result = self.returnWinner()
		if(result == self.players[0]):
			return float('inf')
		if(result == self.players[1]):
			return float('-inf')
		return 0

	def getNumAgents(self):
		return len(self.players)

	def getPlayer(self,index):
		return self.players[index]
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
		for player_index in range(1,3):
			
			action = random.choice(game.getLegalActions())
			player_id = game.getPlayerID(player_index)
			game.addBlock(player_id, action)
			print action
			game.display2DBoard()
			winner = game.returnWinner()
			if winner is not None:
				print "Player %s won!" % winner
				gameIsOver = True
				break

def simulate2DMinimaxAgents():
	game = Connect4Simulation(['O', 'X'], y = 1)
	turns = 20
	gameIsOver = False
	player_max = agents.AlphaBetaAgent(depth= 2, max_dir = 0, evalFn= agents.betterEvaluationFunction) #player 0 on game
	player_min = agents.AlphaBetaAgent(depth= 2, max_dir = 1) #player 1 on game
	alphabeta_players = [player_max, player_min]
	for i in range(turns):
		if gameIsOver:
			break
		for player_index in range(0,2):
			player_id = game.getPlayer(player_index)
			AlphaBetaAgent_player = alphabeta_players[player_index]
			action = AlphaBetaAgent_player.getAction(game)
			game.addBlock(player_id, action)
			print "player ",player_id, "places at", action
			game.display2DBoard()
			winner = game.returnWinner()
			if winner is not None:
				print "Player %s won!" % winner
				gameIsOver = True
				break
simulate2DMinimaxAgents()