# Display 2D Fourplay Board 

import matplotlib.pyplot as plt
import numpy as np
import random
import copy



def displayBoardSingleFrame(grid):
	dim_x, dim_y = grid.shape
	column_labels = range(dim_x)
	row_labels = range(dim_y)
	fig, ax = plt.subplots()
	print(plt.cm.Blues)
	heatmap = ax.pcolor(grid, cmap = 'YlGnBu')
	ax.set_xticks(np.arange(grid.shape[0]), minor = False)
	ax.set_yticks(np.arange(grid.shape[1]), minor = False)
	ax.invert_yaxis()
	plt.grid()
	plt.show()


def rowWin(row):
	if (0 not in row):
		tempDict = {}
		for elem in row:
			tempDict[elem] = 1
		if(len(tempDict) == 1):
			return True
	return False

def gameOver(grid):
	numRow, numCol = grid.shape
	if(np.count_nonzero(grid) == numRow*numCol):
		return True
	gridTranspose = grid.T
	print(grid, gridTranspose)
	for row in grid:
		if(rowWin(row)):
			return True
	for row in gridTranspose:
		if(rowWin(row)):
			return True
	return False

def randomAvailableIndex(grid):
	numRow, numCol = grid.shape
	while(True):
		i, j = random.choice(range(numRow)), random.choice(range(numCol))
		if(grid[i][j] == 0):
			return i, j


def simulateGame():
	grid = np.zeros((4,4))
	displayBoardSingleFrame(grid)
	playerTurn = 1
	while(gameOver(grid) == False):
		i, j = randomAvailableIndex(grid)
		grid[i][j] = playerTurn
		if(playerTurn == 1): 
			playerTurn = 2
		else: 
			playerTurn = 1
		displayBoardSingleFrame(grid)


simulateGame()