import random

class RandomAgent:
	def __init__(self, name):
		self.id = name
	
	def getAction(self, game):
		if game.getLegalActions():
			return random.choice(game.getLegalActions())
		else:
			return None
