# Create the shell script for many games

import sys

def main():
	lowIndex = sys.argv[1]
	highIndex = sys.argv[2]
	f = open("batchGameScript.sh", 'w')
	for i in range(int(lowIndex), int(highIndex) +1):
		ident = "game" + str(i)
		f.write("mkdir " + ident + "\n")
		f.write("python fourplayWebAutomate.py " + ident + " HARD " + "\n")
		f.write("rm -rf " + ident + "\n\n")

main()