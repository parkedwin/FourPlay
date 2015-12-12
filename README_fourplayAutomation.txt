# fourplayWebAutomation README 


#######################################  File Description  #######################################

agents.py
	~ 	Defines the getAction(), evaluationFunction(), and scoreEvaluationFunction() for ReflexAgent
	~ 	Defines the minimax logic with alpha beta pruning for AlphaBetaAgent class 
	~ 	Defines betterEvaluationFunction() where we can apply domain specific knowledge and weights
		obtained by TD Learning to improve minimax performance


batchGameScript.sh
	~	For each simulation we want to automate between our AI and the online oracle, there are three
		commands to create the folder to store all the .png images of the game's history, create the
		transcript for all the move information for further analysis as .txt files, and delete
		all the images for memory savings. 
		>> mkdir <game_identification>
		>> python fourplayWebAutomate.py <game_identification> <game_mode> <player_name>
		>> rm -rf <game_identification>


batchGameScriptGenerator.py
	~	Creates the batchGameScript.sh
	~ 	User specifies a low index and high index (eg python batchGameScriptGenerator.py 1 10)
		would generate a command for game 1 to game 10 

fourplay.html
	~	HTML backbone for extracting the graphical interface from mathisfun.com to the webbrowser 


fourplayWebAutomate.py
	~	Script containing all the logic behind the automation of the gameplay between our AI
	and online oracle. Takes care of the computer vision to detect oracle's moves, mouse event
	handling to input our AI's moves, and integration of other classes to make the gameplay end 
	to end.


human.py
	~	Defines the human class, which would involve manual input of a human player's moves


imageSubtract.py
	~	Tool developed part of the computer vision to detect the areas of change between two
	iterations of the game. Pixel subtraction would lead to black ([0,0,0] for rgb) in areas
	where no change occurred. We can find blue regions to associate with the oracle's new game 
	piece.


mouseClick.py
	~ 	Script to take care of performing a mouse click at the coordinates specified 


random_agent.py
	~ 	Defines the RandomAgent class, which would just choose moves randomly 


simulation.py
	~ 	Script containing all the logic behind our own graphic interface to display gameplay 
	between two players. Each player could be an instance of the Human, RandomAgent, ReflexAgent,
	or AlphaBetaAgent class. 


TDLearn.py
	~	Takes in a list of game transcripts, parses each move, and learn weights for our
		evaluation function to improve performance. 


test_simulation.py
	~	Test cases for robustness of our simulation.py script


trackOpponentMove.py
	~	Perform image subtraction of previous and current iteration, and identify the pixel
		as well as the corresponding grid on the game board where the oracle placed its piece. 


######################## Automation Playing our AI Against Online Oracle ######################## 

After developing our fourplay AI agent with minimax + alpha beta pruning, we would like to 
test it's performance against the best state of the art oracle available online. The oracle
we will use will be based on the "hard" level of Connect3D from mathisfun.com we extracted
the game board graphics into fourplay.html by screenshot and then utilized computer vision 
to track the oracle's moves (blue tiles), feed their move into our AI, generate our move, 
and place a red tile on the corresponding tile through a mouse event. 

To recognize the oracle's move per iteration, we performed an image subtraction of the 
screen shot of the board between the current iteration and previous iteration. We
empircally determined the pixel coordinates that correspond to where a tile would be 
placed on the board. We also determined the change in pixel coordinate given tile stacking.
Finally, we constantly keep track of the stack height of each of the 16 cells, so it is
possible to determine exactly the 16 pixel coordinates to check. For each pixel coordinate
as long as the corresponding pixel in the subtracted image is sufficiently blue, which 
is determined by checking across a red, green, and blue threshold (ie make sure the pixel
is low in value for the red and green channel but high in the blue channel), we can
conclude that the position of the newly placed tile is at the corresponding grid position. 
The tile detection accuracy was verified over hundreds of games with 100 % accuracy. 

Our AI agent calculates the appropriate move, and we use CGQuartz package to make a mouseClick
event to the corresponding position on the mathisfun graphics display. The following is a 
description of how to set up the game environment and run many iterations of the game on 
different settings. 

0.) Use MacBook Pro (13-inch Mid 2012) model 
1.) Load fourplay.html on google chrome web browser
2.) Drag left side of the browser window all the way left to have it flush against left 
	boundary of screen
3.) Drag the board angle to 0, and have setting with Red as Human (our AI) and blue as 
	computer (the oracle).
4.) Have terminal and all other applications to the right of the web browser. Must not have
	any thing overlapping the game board at any point. 
5.) Default settings for xgap and ygap in the fourplayWebAutomation.py are set to fit the 
	screen size to find the top left corner of the gameboard. Adjust these parameters if 
	running software on computers of different screen dimensions. 
6.) >> python batchGameScriptGenerator.py <begin_index> <end_index> 
	This command generates the batchGameScript.sh file that contains commands to make 
	directory to store the game's frame by frame moves as .png, run the entire game, and 
	write to .txt file the game transcript which contains each move of the session. Delete 
	the frame by frame images after transcript is created to save memory. 

7.) >> bash batchGameScript.sh
	This commands begins execution of game session beg_index, to end_index
8.) Watch the many sessions of games run automatically
9.) Retrieve game transcripts stored in game_transcript directory to perform further analysis. 


####################################  fourplayWebAutomate.py  ####################################

This program performs all the machinery behind the automation for playing our AI against
the online oracle. To run the program for one iteration of the game type the following command

>> python fourplayWebAutomate.py <game_id> <game_mode> <player_name> <exploration_param>

It takes it three required parameters: game_id specifies the name of the .txt file for the game 
transcript, game_mode specifies whether we are playing "beginner", "easy", "medium", or "hard" 
(oracle), and player_name can be specified as "alpha", "reflex", or "random" to specify which 
form of the AI we are using. There is an optional fourth parameter expoloration_param that could 
be either True or False, depending on whether user would like to user an exploration policy. By 
default, the exploration probability is set to 0.2. 

At the beginning of this file, there are also some important global variables. depth is specific 
to the minimax search algorithm, and can be toggled between 1 or 2. xgap, and ygap are set to 6 
and 124 as default configuration for the location of the top left corner of the gameplay screen. 
These settings are specific to using google chrome browser on a standard 13 inch macbook pro. 
Adjustments to these parameters are needed when running the automation on different environments. window_len, and window_height are also the default dimensions of the board given google chrome 
browser set to 100 % zoom. 

Output: 

When running fourplayWebAutomate.py user should be able to see the game play on the fourplay.html
window on their browser. Each of the moves are stored in an array called game_transcript, and 
details for every move will be written out to the game transcript folder as a .txt file. User has 
the option of modifying the directory path of the filewriter to specify where they would like to 
write the transcripts to. 


#########################################  simulation.py  #########################################

We developed our own graphical interface, so user has the option to play against another human
(2 player mode), against our random agent, reflex agent, and our minimax agent. In this file we
defined a ConnectFour class, which initializes the board dimensions, has methods for setting
player index, adding blocks, checking whether a cell has any more space, check if there is a win,
find row patterns, are calculate all counts. 

The simulate() method takes in an agent list of two players, and specification of whether or not
to turn on the graphical display. A player could be an instance of following classes: Human,
RandomAgent, ReflexAgent, AlphaBetaAgent. 

To use this program, type following command in the terminal window

>> python simulation.py <player_1_type> <player_2_type> <num_simulations>

There are two required arguments, each specifying the type of player. They can be the following
input: "human", "random", "reflex", "alpha". The third optional argument num_simulations would
specify the number of games we want the program to run. Default for this parameter is 15 if
value is not specified. 

Output: 
Transcript of all the moves, number of moves for the game to come to completion, identity of
the winner, and evaluation metric. If graphical display is on, then user can see the game
visually as well. 



####################################### Data set generation #######################################

We ran our fourplayAutomation.python module on the following conditions and obtained
the corresponding results. 


Depth 1 Minimax w/ Alpha Beta Pruning vs Oracle
	- Ran 100 iterations 
	- 75 wins
	- 75 % win rate

Depth 1 Minimax w/ Alpha Beta Pruning + TD Learning Weights vs Oracle
	- Ran 50 iterations
	- 41 wins
	- 82 % win rate 
	- 7% improvement with TD Learning

Depth 2 Minimax w/ Alpha Beta Pruning + TD Learning Weights Vs Oracle
	- Ran 10 iterations
	- 9 wins
	- 90 % win rate 

Random vs Oracle
	- Ran 50 iterations
	- 0 wins
	- 0 % win rate

Reflex Agent vs Oracle (Hard)
	- Ran 50 iterations
	- 2 wins
	- 4 % win rate 

Reflex Agent vs Oracle (Medium)
	- Ran 50 iterations
	- 20 wins
	- 40 % win rate


