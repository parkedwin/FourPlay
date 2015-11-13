import simulation

def Debugging(tests):
	players = ['X','O']
	for num, test in enumerate(tests):
		sim = simulation.Connect4Simulation(players, x=5, y=5, z=4)
		moves = test
		for move in moves:
			player = move[0]
			action = move[1]
			sim.addBlock(player, action)
		print sim.getBlock(0,0,4)
	#do stuff

tests = []
tests.append([('X',(0,0)), ('X',(0,0)), ('X',(0,0))])
Debugging(tests)