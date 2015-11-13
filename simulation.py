### Simple Simulation for Connect Four
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from itertools import product, combinations
import numpy as np
import random
import agents
from human import Human
from random_agent import RandomAgent
from agents import AlphaBetaAgent
import copy
from matplotlib.widgets import Button


class Connect4Simulation():

	def __init__(self, players, dimension = 3, x = 4, y = 4, z = 4, conn_num = 4, display = True):
		self.dimension = dimension
		if self.dimension == 2: y = 1
		self.board = [[[] for j in range(y)] for i in range(x)]
		self.players = players
		self.height = z
		self.rownum = x
		self.colnum = y
		self.conn_num = conn_num
		self.isOver = False
		self.display = display

	def getPlayerIndex(self,player):
		if player in self.players:
			return self.players.index(player) + 1
		raise AssertionError("Invalid player")
	#indexed starting at 1
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
		  if k >= 0 and k < self.height:
		  	return 0
		return -1

	def getBlock_PlayerID(self, i,j, k):
		if j < self.colnum and i < self.rownum and j >= 0 and i >= 0:
		  if k < len(self.board[i][j]) and k >= 0:
			return self.getPlayerID(self.board[i][j][k])
		  if k >= 0 and k < self.height:
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

	def displayBoard(self):
		if self.dimension == 2:
			self.display2DBoard()
		elif self.dimension == 3:
			self.display3DBoard()

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
		terminalGrid = copy.deepcopy(grid)
		print terminalGrid.transpose()
		self.display2DBoardSingleFrame(grid.transpose())


	# AM 11/11/15 Added function for display3DBoard
	def display3DBoard(self):
		grid = np.zeros((self.rownum, self.colnum, self.height))
		for i in range(len(self.board)):
			for j in range(len(self.board[i])):
				for k in range(len(self.board[i][j])):
					grid[i][j][k] = self.getBlock(i, j, k)
		self.display3DBoardSingleFrame(grid)

	def exiting(self,blah):
		exit()

	def closeplt(self,blah):
		plt.close()

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
		axstop = plt.axes([0.9, 0.0, 0.1, 0.075])
		axnext = plt.axes([0.1, 0.0, 0.1, 0.075])
		button_stop = Button(axstop, 'Stop')
		button_next = Button(axnext, 'Next')
		button_stop.on_clicked(self.exiting)
		button_next.on_clicked(self.closeplt)
		plt.show()

		#AM Added 11/11/15 
	def display3DBoardSingleFrame(self, grid):
		def drawGamePrism(ax):
			cube_corner = [[0, 0, 0], [self.rownum, 0, 0], [self.rownum, self.colnum, 0], [0, self.colnum, 0],
			[0, 0, self.height], [self.rownum, 0, self.height], [self.rownum, self.colnum, self.height], [0, self.colnum, self.height]]
			ax.plot3D(*zip(cube_corner[0], cube_corner[1]), color = "m")
			ax.plot3D(*zip(cube_corner[1], cube_corner[5]), color = "m")
			ax.plot3D(*zip(cube_corner[5], cube_corner[4]), color = "m")
			ax.plot3D(*zip(cube_corner[4], cube_corner[0]), color = "m")
			ax.plot3D(*zip(cube_corner[3], cube_corner[2]), color = "m")
			ax.plot3D(*zip(cube_corner[2], cube_corner[6]), color = "m")
			ax.plot3D(*zip(cube_corner[6], cube_corner[7]), color = "m")
			ax.plot3D(*zip(cube_corner[7], cube_corner[3]), color = "m")
			ax.plot3D(*zip(cube_corner[0], cube_corner[3]), color = "m")
			ax.plot3D(*zip(cube_corner[1], cube_corner[2]), color = "m")
			ax.plot3D(*zip(cube_corner[5], cube_corner[6]), color = "m")
			ax.plot3D(*zip(cube_corner[4], cube_corner[7]), color = "m")

		def drawThreadPoles(ax):
			for x in range(self.rownum):
				for y in range(self.colnum):
					minz, maxz = 0, self.height
					ax.plot3D(*zip([x,y,minz], [x,y,maxz]), color = "g")

		fig = plt.figure()
		ax = fig.add_subplot(111, projection = '3d')
		ax.set_xticks(np.arange(grid.shape[0]), minor = False)
		ax.set_yticks(np.arange(grid.shape[1]), minor = False)
		ax.set_zticks(np.arange(grid.shape[2]), minor = False)
		drawGamePrism(ax)
		drawThreadPoles(ax)
		
		for x in range(len(grid)):
			for y in range(len(grid[0])):
				for z in range(len(grid[0][0])):
					if(grid[x][y][z] == 0):
						continue
					elif(grid[x][y][z] == 1):
						color = 'b'
					elif(grid[x][y][z] == 2):
						color = 'r'
					ax.scatter([x], [y], [z], c = color, s = 80)
		ax.set_xlabel('X Label')
		ax.set_ylabel('Y Label')
		ax.set_zlabel('Z Label')
		axstop = plt.axes([0.9, 0.0, 0.1, 0.075])
		axnext = plt.axes([0.1, 0.0, 0.1, 0.075])
		button_stop = Button(axstop, 'Stop')
		button_next = Button(axnext, 'Next')
		button_stop.on_clicked(self.exiting)
		button_next.on_clicked(self.closeplt)
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

	#indexed starting at 0
	def getPlayer(self,index):
		return self.players[index]

'''
OUTSIDE THE CLASS
'''

def simulate(game, players):
	while not game.isOver:
		for player_index in range(1,3):
			if not game.getLegalActions():
				print "DRAW"
				game.displayBoard()
				return
			player_id = game.getPlayerID(player_index)
			curr_player = players[player_index]
			action = None
			action = curr_player.getAction(game)
			print ("Action: ", action)
			game.addBlock(player_id, action)
			if game.display:
				game.displayBoard()
			winner = game.returnWinner()
			if winner is not None:
				print "Player %s won!" % winner
				game.isOver = True
				game.displayBoard()
				return

game = Connect4Simulation(['O', 'X'], dimension=3, display=True)
human1 = Human(index = 0)
human2 = Human(index = 1)
random1 = RandomAgent(index = 0)
random2 = RandomAgent(index = 1)
alpha1 = AlphaBetaAgent(depth = 1, \
						max_dir = 0, \
						evalFn = agents.betterEvaluationFunction)
alpha2 = AlphaBetaAgent(depth = 1, \
						max_dir = 1, \
						evalFn = agents.betterEvaluationFunction)
players = ['None', human1, alpha2]
simulate(game, players)

def simulateRandom(dimension):
	game, turns = None, 0
	if(dimension == 2):
		game = Connect4Simulation(['O', 'X'], y = 1)
		turns = 20
	elif(dimension == 3):
		game = Connect4Simulation(['O', 'X'])
		turns = 90
	gameIsOver = False
	for i in range(turns):
		if gameIsOver:
			break
		for player_index in range(1,3):
			action = random.choice(game.getLegalActions())
			player_id = game.getPlayerID(player_index)
			game.addBlock(player_id, action)
			print action
			if(dimension == 2):
				game.display2DBoard()
			elif(dimension == 3):
				game.display3DBoard()
			winner = game.returnWinner()
			if winner is not None:
				print "Player %s won!" % winner
				gameIsOver = True
				break


def simulateHumanVsHuman(dimension, graphics = False):
	game, turns = None, 0
	if(dimension == 2):
		game = Connect4Simulation(['O', 'X'], y = 1)
		turns = 20
	elif(dimension == 3):
		game = Connect4Simulation(['O', 'X'])
		turns = 90
	gameIsOver = False
	player_human1 = human.Human(game.rownum, game.colnum, 0)
	player_human2 = human.Human(game.rownum, game.colnum, 1)
	players = ['None', player_human1, player_human2]
	for i in range(turns):
		if gameIsOver:
			break
		for player_index in range(1,3):
			player_id = game.getPlayerID(player_index)
			human_player = players[player_index]
			action = None
			if(dimension == 2):
				action = (human_player.get2DAction(game.players[player_index -1]), 0)
				game.addBlock(player_id, action)
				if graphics: game.display2DBoard()
			elif(dimension == 3):
				action = human_player.get3DAction(game.players[player_index -1])
				game.addBlock(player_id, action)
				if graphics: game.display3DBoard()
			winner = game.returnWinner()
			if winner is not None:
				print "Player %s won!" % winner
				gameIsOver = True
				break 


def simulateMinimaxVsHuman(dimension):
	game, turns = None, 0
	if(dimension == 2):
		game = Connect4Simulation(['O', 'X'], y = 1)
		turns = 20
	elif(dimension == 3):
		game = Connect4Simulation(['O', 'X'])
		turns = 90
	gameIsOver = False
	player_human = human.Human(game.rownum, game.colnum)
	player_min = agents.AlphaBetaAgent(depth= 2, max_dir = 1, evalFn= agents.betterEvaluationFunction) #player 1 on game
	players = ['None', player_human, player_min]
	for i in range(turns):
		if gameIsOver:
			break
		for player_index in range(1,3):
			player_id = game.getPlayerID(player_index)
			if(player_index == 1):
				human_player = players[player_index]
				action = None
				if(dimension == 2):
					action = (human_player.get2DAction(game.players[player_index - 1]), 0)
				elif(dimension == 3):
					action = human_player.get3DAction(game.players[player_index - 1])
				game.addBlock(player_id, action)
			elif(player_index == 2):
				AlphaBetaAgent_player = players[player_index]
				action = AlphaBetaAgent_player.getAction(game)
				game.addBlock(player_id, action)
			print "player ",player_id, "places at", action
			print "Evaluation :",agents.betterEvaluationFunction(game)
			if(dimension == 2):
				game.display2DBoard()
			elif(dimension == 3):
				game.display3DBoard()
			winner = game.returnWinner()
			if winner is not None:
				print "Player %s won!" % winner
				gameIsOver = True
				break

def simulateMinimaxAgents(dimension):
	game, turns = None, 0
	if(dimension == 2):
		game = Connect4Simulation(['O', 'X'], y = 1)
		turns = 20
	elif(dimension == 3):
		game = Connect4Simulation(['O', 'X'])
		turns = 90
	gameIsOver = False
	player_max = agents.AlphaBetaAgent(depth= 2, max_dir = 0, evalFn= agents.betterEvaluationFunction) #player 0 on game
	player_min = agents.AlphaBetaAgent(depth= 2, max_dir = 1, evalFn= agents.betterEvaluationFunction) #player 1 on game
	alphabeta_players = ['None', player_max, player_min]
	for i in range(turns):
		if gameIsOver:
			break
		for player_index in range(1,3):
			player_id = game.getPlayerID(player_index)
			AlphaBetaAgent_player = alphabeta_players[player_index]
			print("here")
			action = AlphaBetaAgent_player.getAction(game)
			game.addBlock(player_id, action)
			print "player ",player_id, "places at", action
			print "Evaluation :",agents.betterEvaluationFunction(game)
			if(dimension == 2):
				game.display2DBoard()
			elif(dimension == 3):
				game.display3DBoard()
			winner = game.returnWinner()
			if winner is not None:
				print "Player %s won!" % winner
				gameIsOver = True
				break

# simulateRandom(3)
# simulateHumanVsHuman(3)
# simulateMinimaxVsHuman(3)
# simulateMinimaxAgents(2)

# simulateRandom(2)
# simulateHumanVsHuman(2)
# simulateMinimaxVsHuman(3)
# simulateMinimaxAgents(2)

# simulateMinimaxAgents(2)


