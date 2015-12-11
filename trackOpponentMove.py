# Use image subtraction of two consecutive game iterations to determine 
# what was the oracle's most recent move 

import numpy as np
from scipy.misc import imread, imsave
import pylab as plt

RED_THRESHOLD = 40
GREEN_THRESHOLD = 40
BLUE_THRESHOLD = 75

def detectionPointDict():
	detectPoints = {}
	initXCoord = 150
	initYCoord = [293, 257, 221, 185]
	for x_board_index in range(4):
		xc = initXCoord + 90*x_board_index
		for y_board_index in range(4):
			yc = initYCoord[y_board_index]
			detectPoints[(x_board_index, y_board_index)] = (xc, yc)
	return detectPoints 


# def identifyMove(detectPoints, img_sub, prevHeights):
# 	possibleMoves = []
# 	for boardPos in detectPoints.keys():
# 		pixelPair = detectPoints[boardPos]
# 		stackHeight = prevHeights[boardPos[1]][boardPos[0]]
# 		x = int(pixelPair[0])
# 		y = int(pixelPair[1] - stackHeight*15)
# 		if(img_sub[y][x][0] <RED_THRESHOLD and img_sub[y][x][1] < GREEN_THRESHOLD and img_sub[y][x][2] > BLUE_THRESHOLD):
# 			possibleMoves.append(boardPos)

# 	if(len(possibleMoves) != 1):
# 		print("Number of possible moves is not equal 1")
# 	return possibleMoves

# return tuple (column, row)
# def calcOracleMoveByImageSubtract(gameFolder, iteration, prevHeights):
# 	detectPoints = detectionPointDict()
# 	print("Performing Image Subtraction")
# 	image_prev = imread(gameFolder + "/full_snap__" + str(iteration - 1) + ".png").astype(np.float32)
# 	image_curr = imread(gameFolder + "/full_snap__" + str(iteration) + ".png").astype(np.float32)
# 	img_sub = image_prev - image_curr
# 	for y_b in range(len(img_sub)):
# 		for x_b in range(len(img_sub[0])):
# 			if(not (np.absolute(img_sub[y_b][x_b]) == np.array([0,0,0])).all()):
# 				img_sub[y_b][x_b] = image_curr[y_b][x_b]
# 			else:
# 				img_sub[y_b][x_b] = np.array([0,0,0])

# 			if(img_sub[y_b][x_b][2] != max(img_sub[y_b][x_b])):
# 				img_sub[y_b][x_b] = np.array([0,0,0])
# 	oracle_move = identifyMove(detectPoints, img_sub, prevHeights)
# 	return oracle_move[0]


def calcOracleMoveByImageSubtract(gameFolder, iteration, prevHeights):
	detectPoints = detectionPointDict()
	print("Performing Image Subtraction")
	image_prev = imread(gameFolder + "/full_snap__" + str(iteration - 1) + ".png").astype(np.float32)
	image_curr = imread(gameFolder + "/full_snap__" + str(iteration) + ".png").astype(np.float32)

	possibleMoves = []
	for boardPos in detectPoints.keys():
		pixelPair = detectPoints[boardPos]
		stackHeight = prevHeights[boardPos[1]][boardPos[0]]
		x = int(pixelPair[0])
		y = int(pixelPair[1] - stackHeight*15)
		pixel_sub = image_prev[y][x] - image_curr[y][x]
		if(not(np.absolute(pixel_sub) == np.array([0,0,0])).all()):
			pixel_sub = image_curr[y][x]
		else:
			pixel_sub = np.array([0,0,0])
		if(pixel_sub[2] != max(pixel_sub)):
			pixel_sub = np.array([0,0,0])
		if(pixel_sub[0] < RED_THRESHOLD and pixel_sub[1] < GREEN_THRESHOLD and pixel_sub[2] > BLUE_THRESHOLD):
			possibleMoves.append(boardPos)
	if(len(possibleMoves) != 1):
		print("Number of possible moves is not equal 1")
	return possibleMoves


