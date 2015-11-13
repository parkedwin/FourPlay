import random

class RandomAgent:
	def __init__(self, index):
		self.index = index
	
	def getAction(self, game):
		if game.getLegalActions():
			return random.choice(game.getLegalActions())
		else:
			return None
