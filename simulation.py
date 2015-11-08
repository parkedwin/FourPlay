### Simple Simulation for Connect Four

class Connect4Simulation():

	def __init__(self, x = 5, y = 5, z = 7, conn_num = 4):
		self.board = [[[] for j in range(y)] for i in range(x)]
		self.players = ['red', 'yellow']
		self.height = z
		self.rownum = x
		self.colnum = y
		self.conn_num = conn_num

	def addBlock(self, player, action):
		x = action[0]
		y = action[1]
		if y < self.colnum and x < self.rownum:
			column = self.board[x][y] # is column set by reference or value?
			if len(column) < self.height:
				column.append(player)
				return
		raise AssertionError("Cannot add to this column")

	def hasSpace(self, x, y):
		if y < self.colnum and x < self.rownum:
		  if len(self.board[x][y]) < self.height:
		  	return True
		return False

	def getBlock(self, i, j, k):
		if j < self.colnum and i < self.rownum:
		  if k < len(self.board[i][j]):
			return self.board[i][j][k]
		return None

	def checkRowWin(allRows):
		for row in allRows:
			if row.count(row[0]) == len(row):
				return row[0]
		return None

	#Think about better time complexity ...
	def returnWinner(self):
		conn_num = self.conn_num
		for k in range(self.height):
			for i in range(self.rownum - self.conn_num):
				for j in range(self.colnum - self.conn_num):
					player = getBlock(i, j, k)
					if player is not None:
						allRows = []
						#go down column to check for win
						allRows.append([getBlock(i+num,j,k) for num in range(0, conn_num)])
						#go down row to check for win
						allRows.append([getBlock(i,j+num,k) for num in  range(0, conn_num)])
						#go down z_col to check for win
						allRows.append([getBlock(i,j,k+num) for num in range(0, conn_num)])
						#go down diagonals
						allRows.append([getBlock(i+num,j+num,k) for num in range(0, conn_num)])
						allRows.append([getBlock(i+num,j,k+num) for num in range(0, conn_num)])
						allRows.append([getBlock(i,j+num,k+num) for num in range(0, conn_num)])
						allRows.append([getBlock(i+num,j+num,k+num) for num in range(0, conn_num)])

						#other diagonals T_T
						allRows.append([getBlock(i+num,j-num,k) for num in range(0, conn_num)])
						allRows.append([getBlock(i+num,j,k-num) for num in range(0, conn_num)])
						allRows.append([getBlock(i,j+num,k-num) for num in range(0, conn_num)])

						allRows.append([getBlock(i-num,j+num,k+num) for num in range(0, conn_num)])
						allRows.append([getBlock(i+num,j-num,k+num) for num in range(0, conn_num)])
						allRows.append([getBlock(i+num,j+num,k-num) for num in range(0, conn_num)])

						result = checkRowWin(allRows)
						if result:
							return result
		return None

	# action defined as (row, col) pair to add to a column
	def GetLegalActions(self):
		actions = []
		for i in range(self.rownum):
			for j in range(self.colnum):
				if hasSpace(i,j):
					actions.append((i, j))
		return actions

	def generateSuccessor(self, player, action):
		newState = copy.deepcopy(self)
		if player in newState.players and action in newState.GetLegalActions():
			newState.addBlock(player, action)
		else:
			raise AssertionError("Invalid Player/action")
		return newState


