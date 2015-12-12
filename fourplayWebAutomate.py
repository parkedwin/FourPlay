# To automate the game play between our AI for 3D connect 4 and the mathisfun.com
# oracle, we use a series of automated screen shots, and image subtraction to 
# determine the move made by their computer (blue tiles). We would then feed
# their move into our side of the AI to generate a response which we would pass
# as a coordinate and create a mouse event to generate a click onto the mathisfun
# window to complete a full turn. Repeat these turns until game is over, and we would
# have generated a series of images for the entire game movie. 




from PIL import ImageGrab
import random
import os
import sys
import time
import numpy as np 
import mouseClick
from random import randint
from trackOpponentMove import calcOracleMoveByImageSubtract

#Simulation packages
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from itertools import product, combinations
import random
from simulation import ConnectFour
import agents
from human import Human
from random_agent import RandomAgent
from agents import AlphaBetaAgent
from agents import ReflexAgent
import agents
import copy
from matplotlib.widgets import Button

gameFolder = sys.argv[1]
gameMode = sys.argv[2]
player_name = sys.argv[3]
if len(sys.argv) > 4:
	explore = True
else:
	explore = False
exploreProb = 0.2
depth = 2


xgap = 6
ygap = 124
window_len = 619
window_height = 420

def screenGrab(iteration):
	box = (xgap, ygap, xgap + window_len, ygap + window_height)
	im = ImageGrab.grab(box)
	im.save(os.getcwd() + "/" + gameFolder + '/full_snap__' + str(iteration) + '.png', 'PNG')

def main():
	print("STARTING GAME: " + gameFolder)
	game_transcript = [] #keep track of all moves
	iteration = 0
	prevHeights = np.zeros((4,4)) # prevHeight[y][x] gives height of stack for xth column and y row counting upwards

	screenGrab(iteration) #to get the empty board
	newgamecordx = 180
	newgamecordy = 153
	mouseClick.mouseclick(newgamecordx,newgamecordy)

	xcoords = [182,272,365,455]
	ycoords = [405,320,286,259]

	#NUM_GAME_ITERATIONS = 25
	win = False


	web_player = "O"
	our_player = "X"
	players = [web_player,our_player]

	alpha_player = AlphaBetaAgent(our_player, web_player, depth = depth, \
							maximize = -1, \
							evalFn = agents.betterEvaluationFunction)

	reflex_player = ReflexAgent(our_player,web_player,maximize=False)

	random_player = RandomAgent(our_player)

	if(player_name == "random"):
		play_inst = random_player
	elif(player_name == "reflex"):
		play_inst = reflex_player
	elif(player_name == "alpha"):
		play_inst = alpha_player

	game = ConnectFour(players, dimension=3, x=4, y=4, z = 4, display=False)
	tic = time.clock()
	timesfailed = 0
	while(not win):
		time.sleep(3)
		iteration += 1

		print "ITERATION:", iteration

		while(True):
			screenGrab(iteration)
		# get the move they put by image subtraction 
			oracleMove = calcOracleMoveByImageSubtract(gameFolder, iteration, prevHeights)
			if(len(oracleMove) == 1):
				oracleMove = oracleMove[0]
				break
			if(iteration == 1):
				screenGrab(0)
				print "Clicked New Game Again"
				mouseClick.mouseclick(newgamecordx,newgamecordy)
				screenGrab(0)
				timesfailed = 0
				time.sleep(3)
			else:
				timesfailed += 1
			if(timesfailed > 3): #restart whole game since faulty
				print "Failed more than 3 times. Trying to restart game"
				iteration = 1
				game = ConnectFour(players, dimension=3, x=4, y=4, z = 4, display=False)
				game_transcript = []
				exit(0)

		prevHeights[oracleMove[1]][oracleMove[0]] += 1
		print("oracle move", oracleMove)
		game_transcript.append(("oracle", oracleMove[0], oracleMove[1], iteration))

		game.addBlock(web_player, oracleMove)

		if(game.returnWinner() == web_player):
			result = "Web"
			print "Web Won"
			win = True
			break
		if(len(game.getLegalActions()) == 0):
			result = "Draw"
			print "Draw"
			win = True
			break

		if(explore):
			rand_num = random.random()
			if(rand_num > exploreProb):
				(mymove_x, mymove_y) = play_inst.getAction(game)
			else:
				actions = game.getLegalActions()
				(mymove_x, mymove_y) = random.choice(actions)
		else:
			(mymove_x, mymove_y) = play_inst.getAction(game)
		game.addBlock(our_player, (mymove_x,mymove_y))

		prevHeights[mymove_y][mymove_x] += 1
		print("our move", (mymove_x,mymove_y))
		game_transcript.append(("fourplay AI", mymove_x, mymove_y, iteration))
		xpixel, ypixel = xcoords[mymove_x],ycoords[mymove_y]
		mouseClick.mouseclick(xpixel, ypixel)
		time.sleep(0.25)
		mouseClick.mouseclick(xpixel, ypixel)
		time.sleep(0.25)
		mouseClick.mouseclick(279, 600)

		if(game.returnWinner() == our_player):
			result = "Us"
			print "We Won!"
			win = True
			break
		if(len(game.getLegalActions()) == 0):
			result = "Draw"
			print "Draw"
			win = True
			break

	toc = time.clock()
	gameTime = toc - tic 
	print("GAME OVER. PLAY TIME = " + str(gameTime))
	print("GAME TRANSCRIPT:")
	f = open('TD_depth2_game_transcripts/' + gameFolder + ".txt", 'w')
	f.write("GAME TRANSCRIPT LEVEL " + gameMode + " FOR: " + gameFolder + "\n")
	f.write("WINNER: " + result + "\n")
	f.write("PLAY TIME = " + str(gameTime) + "\n")
	for move in game_transcript:
		print(move)
		f.write(str(move[0]) + ", " + str(move[1]) +  ", " + str(move[2]) + "\n")


if __name__ == '__main__':
    main()