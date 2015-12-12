# Script to generate the statistics for game transcript

def averageNumMoves():
	folderName = sys.argv[1]
	numGames = sys.argv[2]
	for i in range(1, numGames + 1):
		filename = folderName + "/" + "game" + str(i) + ".txt"
		f = open(filename, 'r')
		count = -3

averageNumMoves()