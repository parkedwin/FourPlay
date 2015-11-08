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

def runTests(tests):
	for num, test in enumerate(tests):
		expected = test[1]
		result = testSimulation(['X','O'], test[0])
		if result != expected:
			print "BasicTest", str(num)," failed: Expected:", expected, " got:", result

tests = []
tests.append(([('X',(0,0)), ('X',(0,1)), ('X',(0,2)),('X',(0,3)), ('X',(0,4))], ('X',(0,3))))
tests.append(([('X',(0,0)), ('O',(0,1)), ('X',(0,2)),('O',(0,3)), ('X',(0,4))], None))
tests.append(([('X',(3,0)), ('X',(2,0)), ('X',(1,0)), ('X',(0,0))], ('X',(0,0))))
tests.append(([('X',(0,0)), ('X',(1,1)), ('X',(2,2)), ('X',(3,3))],('X',(3,3))))
tests.append(([('X',(0,0)), ('X',(1,0)), ('X',(1,0)), ('X',(2,0)), ('X',(2,0)), ('X',(2,0)),('X',(3,0)),('X',(3,0)),('X',(3,0)),('X',(3,0))],('X',(3,0))))
tests.append(([('X',(0,0)), ('O',(1,0)), ('X',(1,0)), ('X',(2,0)), ('X',(2,0)), ('X',(2,0)),('X',(3,0)),('X',(3,0)),('X',(3,0)),('X',(3,0))],('X',(3,0))))
tests.append(([('X',(0,0)), ('X',(1,0)), ('O',(1,0)), ('O',(2,0)), ('X',(2,0)), ('X',(2,0)),('X',(3,0)),('O',(3,0)),('X',(3,0)),('X',(3,0))],None))
runTests(tests)

### Tests on a 2D board: still requires y position to add
def test2DSimulation(players,moves):
	sim = simulation.Connect4Simulation(players, y=1)
	for move in moves:
		player = move[0]
		action = move[1]
		sim.addBlock(player, action)
		result = sim.returnWinner()
		if(result):
			return (result,action)
	return None

def run2DTests(tests):
	for num, test in enumerate(tests):
		expected = test[1]
		result = testSimulation(['X','O'], test[0])
		if result != expected:
			print "Test2D", str(num)," failed: Expected:", expected, " got:", result

tests = []
tests.append(([('X',(3,0)), ('X',(2,0)), ('X',(1,0)), ('X',(0,0))], ('X',(0,0))))
tests.append(([('X',(0,0)), ('X',(1,0)), ('X',(1,0)), ('X',(2,0)), ('X',(2,0)), ('X',(2,0)),('X',(3,0)),('X',(3,0)),('X',(3,0)),('X',(3,0))],('X',(3,0))))
run2DTests(tests)
