from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
  """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
  """
  def __init__(self):
    self.lastPositions = []
    self.dc = None


  def getAction(self, gameState):

    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions()

    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best

    return legalMoves[chosenIndex]

  def evaluationFunction(self, currentGameState, action):

    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    oldFood = currentGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]


    return successorGameState.getScore()


def scoreEvaluationFunction(currentGameState):
  """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
  """
  return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
  """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
  """

  def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
    self.index = 0 # Pacman is always agent index 0
    self.evaluationFunction = util.lookup(evalFn, globals())
    self.depth = int(depth)

######################################################################################
# Problem 1b: implementing minimax

class MinimaxAgent(MultiAgentSearchAgent):
  """
    Your minimax agent (problem 1)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction. Terminal states can be found by one of the following: 
      pacman won, pacman lost or there are no legal moves. 

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game

      gameState.getScore():
        Returns the score corresponding to the current state of the game
    
      gameState.isWin():
        Returns True if it's a winning state
    
      gameState.isLose():
        Returns True if it's a losing state

      self.depth:
        The depth to which search should continue

    """
    def recurse(gameState, current_d, agentIndex):
        LegalActions = gameState.getLegalActions(agentIndex)
        if agentIndex == self.index:
          LegalActions = [x for x in LegalActions if x != Directions.STOP]
        if(gameState.isWin() or gameState.isLose() or len(LegalActions) == 0):
          return ['',gameState.getScore()]
        if(current_d == 0):
          return ['',self.evaluationFunction(gameState)]
        newIndex = agentIndex + 1
        newDepth = current_d
        if newIndex == gameState.getNumAgents():
          newIndex = 0
          newDepth = current_d - 1
        if agentIndex == self.index:
          bestactions = []
          bestscore = float("-inf")
          for action in LegalActions:
            newState = gameState.generateSuccessor(agentIndex, action)
            result = recurse(newState,newDepth,newIndex)
            if result[1] > bestscore:
              bestscore = result[1]
              bestactions = [action]
            if result[1] == bestscore:
              bestactions.append(action)
        else:
          bestactions = []
          bestscore = float("inf")
          for action in LegalActions:
            newState = gameState.generateSuccessor(agentIndex, action)
            result = recurse(newState,newDepth,newIndex)
            if result[1] < bestscore:
              bestscore = result[1]
              bestactions = [action]
            if result[1] == bestscore:
              bestactions.append(action)
        return [random.choice(bestactions), bestscore]

    result = recurse(gameState, self.depth, self.index)
    return result[0]
    # BEGIN_YOUR_CODE (around 30 lines of code expected)
    # END_YOUR_CODE

######################################################################################
# Problem 2a: implementing alpha-beta

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (problem 2)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    def recurse(gameState, current_d, agentIndex, threshold):
        LegalActions = gameState.getLegalActions(agentIndex)
        if agentIndex == self.index:
          LegalActions = [x for x in LegalActions if x != Directions.STOP]
        if(gameState.isWin() or gameState.isLose() or len(LegalActions) == 0):
          return ['',gameState.getScore()]
        if(current_d == 0):
          return ['',self.evaluationFunction(gameState)]
        newIndex = agentIndex + 1
        newDepth = current_d
        if newIndex == gameState.getNumAgents():
          newIndex = 0
          newDepth = current_d - 1
        if agentIndex == self.index:
          bestactions = []
          bestscore = float("-inf")
          for action in LegalActions:
            newState = gameState.generateSuccessor(agentIndex, action)
            result = recurse(newState,newDepth,newIndex,bestscore)
            if result[1] == bestscore:
              bestactions.append(action)
            if result[1] > bestscore:
              bestscore = result[1]
              bestactions = [action]
            if result[1] > threshold:
              return[random.choice(bestactions), bestscore]
        else:
          bestactions = []
          bestscore = float("inf")
          for action in LegalActions:
            newState = gameState.generateSuccessor(agentIndex, action)
            if newIndex == 0:
              result = recurse(newState,newDepth,newIndex,bestscore)
            else:
              result = recurse(newState,newDepth,newIndex,threshold)
            if result[1] == bestscore:
              bestactions.append(action)
            if result[1] < bestscore:
              bestscore = result[1]
              bestactions = [action]
            if(result[1] < threshold):
              return [random.choice(bestactions),bestscore]
        return [random.choice(bestactions), bestscore]
        
    result = recurse(gameState, self.depth, self.index, float("inf"))

    return result[0]
    # BEGIN_YOUR_CODE (around 50 lines of code expected)
    # END_YOUR_CODE

######################################################################################
# Problem 3b: implementing expectimax

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (problem 3)
  """

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """

    # BEGIN_YOUR_CODE (around 25 lines of code expected)
    def recurse(gameState, current_d, agentIndex):
        LegalActions = gameState.getLegalActions(agentIndex)
        if agentIndex == self.index:
          LegalActions = [x for x in LegalActions if x != Directions.STOP]
        if(gameState.isWin() or gameState.isLose() or len(LegalActions) == 0):
          return ['',gameState.getScore()]
        if(current_d == 0):
          return ['',self.evaluationFunction(gameState)]
        newIndex = agentIndex + 1
        newDepth = current_d
        if newIndex == gameState.getNumAgents():
          newIndex = 0
          newDepth = current_d - 1
        if agentIndex == self.index:
          bestactions = []
          bestscore = float("-inf")
          for action in LegalActions:
            newState = gameState.generateSuccessor(agentIndex, action)
            result = recurse(newState,newDepth,newIndex)
            if result[1] == bestscore:
              bestactions.append(action)
            elif result[1] > bestscore:
              bestscore = result[1]
              bestactions = [action]
          return [random.choice(bestactions), bestscore]
        else:
          score_list = list()
          for action in LegalActions:
            newState = gameState.generateSuccessor(agentIndex, action)
            result = recurse(newState,newDepth,newIndex)
            score_list.append(result[1])
          bestscore = sum(score_list)/len(score_list)
          return ['', bestscore]

    result = recurse(gameState, self.depth, self.index)
    return result[0]

    # END_YOUR_CODE

######################################################################################
# Problem 4a (extra credit): creating a better evaluation function
def manhattanDistance(tuple1,tuple2):
  return abs(tuple1[1] - tuple2[1]) + abs(tuple1[0] - tuple2[0]) 

def betterEvaluationFunction(currentGameState):
  """
    Your extreme, unstoppable evaluation function (problem 4).

    DESCRIPTION: This function uses manhattan distance as the main measure of length.
    The evaluation function gives a higher score as pacman gets closer to a food, capsule, or scared ghosts.
    The evaluation function gives a higher score as pacman gets further away from a normal ghost but only
    up until 3 steps away, where it is considered as a safe distance from a ghost. The evaluation function
    gives a lower score with more capsules, food particles, and scared ghosts.
  """
  pacmanPlace = currentGameState.getPacmanPosition()
  oldFood = currentGameState.getFood()
  walls = currentGameState.getWalls()
  longestlength = walls.width + walls.height
  closestfooddist = float(longestlength)
  countfood = 0
  for i in range(oldFood.width):
    for j in range(oldFood.height):
      if oldFood[i][j]:
        dist = manhattanDistance((i,j), pacmanPlace)
        if closestfooddist > dist:
          closestfooddist += dist
        countfood += 1
  capsules = currentGameState.getCapsules()
  closestcapsule = float(longestlength)
  for capsule in capsules:
    dist = manhattanDistance(capsule, pacmanPlace)
    if dist < closestcapsule:
      closestcapsule = dist
  numberscared = 0
  closestScaredGhostdist = float(longestlength)
  closestNormalGhostdist = float(longestlength)
  for ghostindex in range(1,currentGameState.getNumAgents()):
    ghoststate = currentGameState.getGhostState(ghostindex)
    ghostposition = currentGameState.getGhostPosition(ghostindex)
    isScared = ghoststate.scaredTimer > 0
    dist =manhattanDistance(ghostposition, pacmanPlace)
    if isScared:
      numberscared += 1
      if dist < closestScaredGhostdist:
        closestScaredGhostdist = dist
    elif dist < closestNormalGhostdist:
      closestNormalGhostdist = dist

  if(countfood == 0):
    score += longestlength* 400

  score = currentGameState.getScore()
  score += 3*(1/closestfooddist)
  score += 3*(1/closestcapsule)
  score += 3*(1/closestScaredGhostdist)
  score += min(50*(closestNormalGhostdist), 100)
  score -= 20*numberscared
  if(numberscared == 0):
    score -= 70*(len(capsules))
    score -= 3*(countfood)

  else:
    score += 70*(len(capsules))
    score += 4*(countfood)
    score -= 20*numberscared

  return score
better = betterEvaluationFunction


