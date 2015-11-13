import random 

class Human:
	def __init__(self, name):
		self.id = name
	
	def getAction(self, game):
		if game.dimension == 2: #2D case
			return self.get2DAction(game, self.id)
		elif game.dimension == 3: #3D case
			return self.get3DAction(game, self.id)
		else:
			raise AssertionError("Invalid Dimension")
	
	def checkAction(self, game,action):
		return game.hasSpace(action[0],action[1])
	
	def RepresentsInt(self,s):
		try: 
			int(s)
			return True
		except ValueError:
			return False

	def get2DAction(self, game, playerIndex):
		Exit = False
		while(not Exit):
			user_input = raw_input("Select Column for Player " + str(playerIndex) + " : ")
			if self.RepresentsInt(user_input):
				action = game.rownum - 1 - int(user_input)
				action = (action, 0)
				if(self.checkAction(game,action)):
					Exit = True
					break
			print "Invalid Input. Try Again."
		return action

	def get3DAction(self, game, playerIndex):
		Exit = False
		while(not Exit):
			user_input = raw_input("Select x,y coordinate for Player " + str(playerIndex) + " : ")
			processed_input = user_input.split(",")

			if len(processed_input) == 2:
				if self.RepresentsInt(processed_input[0]) and self.RepresentsInt(processed_input[1]):
					action = (int(processed_input[0]), int(processed_input[1]))
					self.checkAction(game,action)
					if(self.checkAction(game,action)):
						Exit = True
						break
			print "Invalid Input. Try Again."
		return action	


