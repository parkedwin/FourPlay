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
from agents import ReflexAgent
import agents
import copy
from matplotlib.widgets import Button


class ConnectFour():

	def __init__(self, players, dimension = 3, x = 4, y = 4, z = 4, conn_num = 4, display = True):
		self.dimension = dimension
		if self.dimension == 2: y = 1
		self.board = [[[] for j in range(y)] for i in range(x)]
		self.players = ['None']
		self.players.extend(players)

		self.height = z
		self.rownum = x
		self.colnum = y
		self.conn_num = conn_num
		self.isOver = False
		self.display = display

	def getPlayerIndex(self,player):
		if player in self.players:
			return self.players.index(player)
		raise AssertionError("Invalid player")

	def getPlayerID(self,index):
		if index <= len(self.players) and index > 0:
			return self.players[index]
		raise AssertionError("invalid index")

	def addBlock(self, player, action):
		x = action[0]
		y = action[1]
		if y < self.colnum and x < self.rownum and x >= 0 and y >= 0:
			column = self.board[x][y]
			if len(column) < self.height:
				column.append(self.getPlayerIndex(player))
				return
		raise AssertionError("Cannot add to this column "+ str(action) + " with " + str(player))

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

	def checkRowWin(self,allRows):
		for row in allRows:
			if row.count(row[0]) == len(row) and row[0] > 0:
				return row[0]
		return None

	def rowsPatterns(self,allRows, patterns,counts):
		for num,row in enumerate(allRows):
			if(row in patterns):
				#print "row", num
				pattern_index = patterns.index(row)
				#print "pattern", row
				counts[pattern_index] += 1

	def getAllCounts(self, patterns, patternsize, offset):
		counts = [0] * len(patterns)
		for k in range(self.height):
			for i in range(self.rownum):
				for j in range(self.colnum):
					player = self.getBlock(i, j, k)
					if player > 0:
						#print "\n player", player
						#print "block", i,j,k
						allRows = []
						#go down column to check for win
						allRows.append([self.getBlock(i+num-offset,j,k) for num in range(0, patternsize)])
						allRows.append([self.getBlock(i-num+offset,j,k) for num in range(0, patternsize)])
						#go down row to check for win
						allRows.append([self.getBlock(i,j+num-offset,k) for num in  range(0, patternsize)])
						allRows.append([self.getBlock(i,j-num+offset,k) for num in  range(0, patternsize)])
						#go down z_col to check for win
						allRows.append([self.getBlock(i,j,k+num-offset) for num in range(0, patternsize)])
						allRows.append([self.getBlock(i,j,k-num+offset) for num in range(0, patternsize)])
						#go down diagonals
						allRows.append([self.getBlock(i+num-offset,j+num-offset,k) for num in range(0, patternsize)])
						allRows.append([self.getBlock(i+num-offset,j,k+num-offset) for num in range(0, patternsize)])
						allRows.append([self.getBlock(i,j+num-offset,k+num-offset) for num in range(0, patternsize)])
						allRows.append([self.getBlock(i+num-offset,j+num-offset,k+num-offset) for num in range(0, patternsize)])

						allRows.append([self.getBlock(i-num+offset,j-num+offset,k) for num in range(0, patternsize)])
						allRows.append([self.getBlock(i-num+offset,j,k-num+offset) for num in range(0, patternsize)])
						allRows.append([self.getBlock(i,j-num+offset,k-num+offset) for num in range(0, patternsize)])
						allRows.append([self.getBlock(i-num+offset,j-num+offset,k-num+offset) for num in range(0, patternsize)])

						#other diagonals T_T
						allRows.append([self.getBlock(i+num-offset,j-num+offset,k) for num in range(0, patternsize)])
						allRows.append([self.getBlock(i+num-offset,j,k-num+offset) for num in range(0, patternsize)])
						allRows.append([self.getBlock(i,j+num-offset,k-num+offset) for num in range(0, patternsize)])

						allRows.append([self.getBlock(i-num+offset,j+num-offset,k) for num in range(0, patternsize)])
						allRows.append([self.getBlock(i-num+offset,j,k+num-offset) for num in range(0, patternsize)])
						allRows.append([self.getBlock(i,j-num+offset,k+num-offset) for num in range(0, patternsize)])

						allRows.append([self.getBlock(i-num+offset,j+num-offset,k+num-offset) for num in range(0, patternsize)])
						allRows.append([self.getBlock(i+num-offset,j-num+offset,k+num-offset) for num in range(0, patternsize)])
						allRows.append([self.getBlock(i+num-offset,j+num-offset,k-num+offset) for num in range(0, patternsize)])

						allRows.append([self.getBlock(i+num-offset,j-num+offset,k-num+offset) for num in range(0, patternsize)])
						allRows.append([self.getBlock(i-num+offset,j+num-offset,k-num+offset) for num in range(0, patternsize)])
						allRows.append([self.getBlock(i-num+offset,j-num+offset,k+num-offset) for num in range(0, patternsize)])

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
		if(result == self.players[1]):
			return float('inf')
		if(result == self.players[2]):
			return float('-inf')
		return 0

'''
OUTSIDE THE CLASS
'''

def simulate(game, agent_list, simulation=False):
	moves = []
	numMoves = 0
	while not game.isOver:
		for agent in agent_list:
			if not game.getLegalActions():
				print "DRAW"
				game.displayBoard()
				return (moves, "Draw")
			action = None
			action = agent.getAction(game)
			numMoves += 1
			# print ("Action: ", action)
			game.addBlock(agent.id, action)
			# print "Eval", agents.betterEvaluationFunction(game)
			moves.append((agent.id, action, agents.betterEvaluationFunction(game), numMoves))
			if game.display:
				game.displayBoard()
			winner = game.returnWinner()
			if winner is not None:
				print "Player %s won!" % winner
				game.isOver = True
				if not simulation: game.displayBoard()
				return (moves, winner)


if __name__ == "__main__":
	player1 = "O"
	player2 = "X"
	players = [player1,player2]

	human1 = Human(player1)
	human2 = Human(player2)
	random1 = RandomAgent(player1)
	random2 = RandomAgent(player2)
	reflex1 = ReflexAgent(player1, player2)
	reflex2 = ReflexAgent(player2, player1)

	alpha1 = AlphaBetaAgent(player1,player2, depth = 1, \
							maximize = 1, \
							evalFn = agents.betterEvaluationFunction)

	alpha2 = AlphaBetaAgent(player2, player1, depth = 1, \
							maximize = -1, \
							evalFn = agents.betterEvaluationFunction)
	agent_list = [random1, random2]
	#agent_list = [human1, alpha2]
	agent_list = [reflex1, alpha2]
	# winner, allMoves = simulate(game, agent_list)
	# print("Number of Total Moves: " + str(len(allMoves)))
	# print("Final Evaluation: " + str(abs(allMoves[-1][3])))

	numSimulations = 15
	winners = []
	for i in range(numSimulations):
		print "iteration %d" % i
		game = ConnectFour(players, dimension=3, x=4, y=4, z = 4, display=False)
		# simulate(game, agent_list, simulation=True)
		allMoves, winner = simulate(game, agent_list, simulation=True)
		print("Number of Total Moves: " + str(len(allMoves)))
		print("Final Evaluation: " + str(allMoves[-1][2]))
		winners.append(winner)
	print winners



