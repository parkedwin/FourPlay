import random 

class Human:
	def __init__(self, rownum, colnum, index = 1):
		self.rownum = rownum
		self.colnum = colnum
		self.index = index
	
	def get2DAction(self, playerIndex):
		user_input = raw_input("Select Column for Player " + str(playerIndex) + " : ")
		action = self.rownum - 1 - int(user_input)
		return action

	def get3DAction(self, playerIndex):
		user_input = raw_input("Select x,y coordinate for Player " + str(playerIndex) + " : ")
		processed_input = user_input.split(",")
		action = (int(processed_input[0]), int(processed_input[1]))
		return action
		

