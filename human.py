import random 

class Human:
	def __init__(self, rownum, colnum, index = 1):
		self.rownum = rownum
		self.colnum = colnum
		self.index = index
	
	def getHumanChosenAction(self, playerIndex):
		user_input = raw_input("Select Column for Player " + str(playerIndex) + " : ")
		action = self.rownum - 1 - int(user_input)
		return action
		

