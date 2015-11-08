import simulation

###Basic Tests for simulation
def testSimulation(players,moves):
	sim = simulation.Connect4Simulation(players)
	for move in moves:
		player = move[0]
		action = move[1]
		sim.addBlock(player, action)
		result = sim.returnWinner()
		if(result):
			return (result,action)
	return None

result = testSimulation(['X','O'],[('X',(0,0)), ('X',(0,1)), ('X',(0,2)),('X',(0,3)), ('X',(0,4))])
if result != ('X',(0,3)):
	print "Test 1 failed: Expected:", ('X',(0,3)), " got:", result

result = testSimulation(['X','O'],[('X',(0,0)), ('O',(0,1)), ('X',(0,2)),('O',(0,3)), ('X',(0,4))])
if result != None:
	print "Test 2 failed: Expected:", "None", " got:", result

result = testSimulation(['X','O'],[('X',(3,0)), ('X',(2,0)), ('X',(1,0)), ('X',(0,0))])
if result != ('X',(0,0)):
	print "Test 2 failed: Expected:", ('X',(0,0)), " got:", result

result = testSimulation(['X','O'],[('X',(3,0)), ('X',(2,0)), ('X',(1,0)), ('X',(0,0))])
if result != ('X',(0,0)):
	print "Test 2 failed: Expected:", ('X',(0,0)), " got:", result