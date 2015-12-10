# To automate the game play between our AI for 3D connect 4 and the mathisfun.com
# oracle, we use a series of automated screen shots, and image subtraction to 
# determine the move made by their computer (blue tiles). We would then feed
# their move into our side of the AI to generate a response which we would pass
# as a coordinate and create a mouse event to generate a click onto the mathisfun
# window to complete a full turn. Repeat these turns until game is over, and we would
# have generated a series of images for the entire game movie. 




from PIL import ImageGrab
import os
import time
import numpy as np 
import mouseClick
from random import randint
from trackOpponentMove import calcOracleMoveByImageSubtract

gameFolder = 'game5'

xgap = 6
ygap = 124
window_len = 619
window_height = 420

def screenGrab(iteration):
	box = (xgap, ygap, xgap + window_len, ygap + window_height)
	im = ImageGrab.grab(box)
	im.save(os.getcwd() + "/" + gameFolder + '/full_snap__' + str(iteration) + '.png', 'PNG')


def main():
	time.sleep(3)
	iteration = 0
	prevHeights = np.zeros((4,4)) # prevHeight[y][x] gives height of stack for xth column and y row counting upwards

	screenGrab(iteration) #to get the empty board
	newgamecordx = 180
	newgamecordy = 153
	mouseClick.mouseclick(newgamecordx,newgamecordy)
	mouseClick.mouseclick(newgamecordx,newgamecordy)

	xcoords = [182,272,365,455]
	ycoords = [405,320,286,259]

	NUM_GAME_ITERATIONS = 25

	while(iteration < NUM_GAME_ITERATIONS):
		time.sleep(2)
		iteration += 1
		screenGrab(iteration)

		# get the move they put by image subtraction 
		oracleMove = calcOracleMoveByImageSubtract(gameFolder, iteration, prevHeights)
		prevHeights[oracleMove[1]][oracleMove[0]] += 1
		print("prevHeight after oracle move", prevHeights)

		moves = [(0,1),(0,1),(1,1),(0,1),(1,1),(0,1),(0,2)]
		# make a call to our AI to find x, y to place the red tile
		# x, y = randint(0,3), randint(0,3)

		x, y = randint(0,3), randint(0,3)
		prevHeights[y][x] += 1
		print("prevHeight after human move", prevHeights)
		xpixel, ypixel = xcoords[x],ycoords[y]
		mouseClick.mouseclick(xpixel, ypixel)
		time.sleep(0.25)
		mouseClick.mouseclick(xpixel, ypixel)
		time.sleep(0.25)
		print "ITERATION", iteration, "Human clicked board coord: ", x,y, "at pixels: ", xpixel, ypixel
		mouseClick.mouseclick(279, 600)
		print 'clicked out'


if __name__ == '__main__':
    main()