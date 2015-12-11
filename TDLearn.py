import os
from simulation import ConnectFour
def parseFile(filename):
	result = {}
	f = open(filename, 'r')
	game = f.readline().split()[-1]
	winner = f.readline().split()[-1]
	time = f.readline().split()[-1]
	moves = []
	for line in f:
		tokens = line.split(',')
		player = tokens[0]
		index1 = int(tokens[1])
		index2 = int(tokens[2])
		moves.append((player, (index1, index2)))
	result['game'] = game
	result['winner'] = winner
	result['time'] = time
	result['moves'] = moves
	return result

def parseDirectory(directory):
	games = []
	print directory
	for fn in os.listdir(directory):
		pathname = os.path.join(directory, fn)
		if os.path.isfile(pathname):
			games.append(parseFile(pathname))
	return games
def getFnApproxScore(currentGameState, weight_2, weight_3):
	pattern_score = []
	pattern_score.append(([1,1,0,0], weight_2))
	pattern_score.append(([1,1,1,0], weight_3))
	pattern_score.append(([2,2,0,0], -1 * weight_2))
	pattern_score.append(([2,2,2,0], -1 * weight_3))
	patterns = [thing[0] for thing in pattern_score]

	offset_patterns_score = []
	offset_patterns_score.append(([0,1,1,0], weight_2))
	offset_patterns_score.append(([0,2,2,0], -1 * weight_2))
	off_patterns = [thing[0] for thing in offset_patterns_score]


	score = 0
	counts = currentGameState.getAllCounts(patterns,4,0)
	for index,count in enumerate(counts):
		score += count*pattern_score[index][1]

	off_counts = currentGameState.getAllCounts(off_patterns,4,1)
	for index,count in enumerate(off_counts):
		score += count*int(offset_patterns_score[index][1]) / 2 

	return score, (counts, off_counts)

def learnWeights(game):
	weight_2 = 2
	weight_3 = 2

	weights_2 = [weight_2]
	weights_3 = [weight_3]

	wins = 0
	eta = 0.02
	disc = 0.9
	for game_i, game in enumerate(games):
		if game['winner'] == 'Us':
			wins += 1
		players = ['oracle','fourplay AI']
		connfour = ConnectFour(players, dimension=3, x=4, y=4, z = 4, display=False)
		currscore = 0

		eta = 0.01 / (game_i + 1)
		for i,move in enumerate(game['moves']):
			if(i == len(game['moves'])-1):
				if game['winner'] == 'Us':
					reward = -100000
				else:
					reward = 100000
			else:
				reward = 0
			new_connfour = connfour.generateSuccessor(move[0],move[1])
			newscore, counts = getFnApproxScore(new_connfour,weight_2,weight_3)
			not_off_counts ,off_counts = counts

			#parameter sharing between these counts. When different player, direction of update should be reversed.
			weight_2 -= eta*(currscore - (reward + newscore*disc)) * not_off_counts[0]
			weight_2 += eta*(currscore - (reward + newscore*disc)) * not_off_counts[2]
			weight_2 -= eta*(currscore - (reward + newscore*disc)) * off_counts[0]
			weight_2 += eta*(currscore - (reward + newscore*disc)) * off_counts[1]

			weight_3 -= eta*(currscore - (reward + newscore*disc)) * not_off_counts[1]
			weight_3 += eta*(currscore - (reward + newscore*disc)) * not_off_counts[3]
			weights_2.append(weight_2)
			weights_3.append(weight_3)
			connfour = new_connfour
			currscore = newscore
	#write weights to file
	f2= open('weights2.txt','w')
	for num in weights_2:
		f2.write(str('%.02f'%num)+'\n')

	f3= open('weights3.txt','w')
	for num in weights_3:
		f3.write(str('%.02f'%num)+'\n')
  	print wins

#games = parseDirectory('game_transcripts')
games = parseDirectory('no_TD_game_transcripts')
learnWeights(games)