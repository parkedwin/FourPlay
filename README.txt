# fourplayWebAutomation README 

Automation with Web 
After developing our fourplay AI agent with minimax + alpha beta pruning, we would like to 
test it's performance against the best state of the art oracle available online. The oracle
we will use will be based on the "hard" level of Connect3D from mathisfun.com we extracted
the game board graphics into fourplay.html by screenshot and then utilized computer vision to track the
oracle's moves (blue tiles), feed their move into our AI, generate our move, and place 
a red tile on the corresponding tile through a mouse event. 

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
description of how to set up the game environment and run many iterations of the game on different
settings. 

0.) Use MacBook Pro (13-inch Mid 2012) model 
1.) Load fourplay.html on google chrome web browser
2.) Drag left side of the browser window all the way left to have it flush against left boundary
of screen
3.) Have terminal and all other applications to the right of the web browser. Must not have
any thing overlapping the game board at any point. 
4.) Default settings for xgap and ygap in the fourplayWebAutomation.py are set to fit the screen
size to find the top left corner of the gameboard. Adjust these parameters if running software
on computers of different screen dimensions. 
5.) >> python batchGameScriptGenerator.py <begin_index> <end_index> 
This command generates the batchGameScript.sh file that contains commands to make directory to 
store the game's frame by frame moves as .png, run the entire game, and write to .txt file the
game transcript which contains each move of the session. Delete the frame by frame images after
transcript is created to save memory. 
6.) >> bash batchGameScript.sh
This commands begins execution of game session beg_index, to end_index
7.) Watch the many sessions of games run automatically
8.) Retrieve game transcripts stored in game_transcript directory to perform further analysis. 

 TD Learning
1. 