import random 

class Human:
	def __init__(self, index):
		self.index = index
	
	def getAction(self, game):
		if game.dimension == 2: #2D case
			return self.get2DAction(game, game.players[self.index])
		elif game.dimension == 3: #3D case
			return self.get3DAction(game, game.players[self.index])
		else:
			raise AssertionError("Invalid Dimension")

	def get2DAction(self, game, playerIndex):
		user_input = raw_input("Select Column for Player " + str(playerIndex) + " : ")
		action = game.rownum - 1 - int(user_input)
		return (action, 0)

	def get3DAction(self, game, playerIndex):
		user_input = raw_input("Select x,y coordinate for Player " + str(playerIndex) + " : ")
		processed_input = user_input.split(",")
		action = (int(processed_input[0]), int(processed_input[1]))
		return action	


