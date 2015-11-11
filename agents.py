
import random

class Agent:
  def __init__(self, index=0):
    self.index = index

  def getAction(self, state):
    raiseNotDefined()

class ReflexAgent(Agent):
  """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.
  """
  def __init__(self, maximize = True):
    self.lastPositions = []
    self.dc = None
    self.max = maximize


  def getAction(self, gameState):

    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions()

    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    if(self.max):
      bestScore = max(scores)
    else:
      bestScore = min(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best

    return legalMoves[chosenIndex]

  def evaluationFunction(self, currentGameState, action):
    successorGameState = gameState.generateSuccessor(agentIndex, action)
    return successorGameState.getScore()


def scoreEvaluationFunction(currentGameState):
  return currentGameState.getScore()

class AgentSearchAgent(Agent):

  def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2', max_dir=0):
    self.evaluationFunction = scoreEvaluationFunction
    self.depth = int(depth)
    self.index = max_dir 
    #max_dir = 0 means try to maximize score, max_dir otherwise means agent
    #wants to minimize score

######################################################################################
# Problem 1b: implementing minimax

class MinimaxAgent(AgentSearchAgent):
  def getAction(self, gameState):
    def recurse(gameState, current_d, agentIndex):
        LegalActions = gameState.getLegalActions()
        if agentIndex == 0:
          LegalActions = [x for x in LegalActions if x != Directions.STOP]
        if(gameState.returnWinner() is not None or len(LegalActions) == 0):
          return ['',gameState.getScore()]
        if(current_d == 0 and agentIndex == self.index):
          return ['',self.evaluationFunction(gameState)]
        newIndex = agentIndex + 1
        newDepth = current_d
        if newIndex == gameState.getNumAgents():
          newIndex = 0
          newDepth = current_d - 1
        if agentIndex == 0: #this agent wants to maximize
          player = gameState.getPlayer(agentIndex)
          bestactions = []
          bestscore = float("-inf")
          for action in LegalActions:
            newState = gameState.generateSuccessor(player, action)
            result = recurse(newState,newDepth,newIndex)
            if result[1] > bestscore:
              bestscore = result[1]
              bestactions = [action]
            if result[1] == bestscore:
              bestactions.append(action)
        else: #this agent wants to minimize
          player = gameState.getPlayer(agentIndex)
          bestactions = []
          bestscore = float("inf")
          for action in LegalActions:
            newState = gameState.generateSuccessor(player, action)
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

class AlphaBetaAgent(AgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (problem 2)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    def recurse(gameState, current_d, agentIndex, threshold):
        LegalActions = gameState.getLegalActions()
        if(gameState.returnWinner() is not None or len(LegalActions) == 0):
          return ['',gameState.getScore()]
        if(current_d == 0 and agentIndex == self.index):
          return ['',self.evaluationFunction(gameState)]
        newIndex = agentIndex + 1
        newDepth = current_d
        if newIndex == gameState.getNumAgents():
          newIndex = 0
          newDepth = current_d - 1
        if agentIndex == 0:
          bestactions = []
          bestscore = float("-inf")
          player = gameState.getPlayer(agentIndex)
          for action in LegalActions:
            newState = gameState.generateSuccessor(player, action)
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
          player = gameState.getPlayer(agentIndex)
          for action in LegalActions:
            newState = gameState.generateSuccessor(player, action)
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

    if(self.index == 0):
      threshold = float("inf")
    else:
      threshold = float("-inf") 
    result = recurse(gameState, self.depth, self.index, float("inf"))
    return result[0]

######################################################################################
# Problem 3b: implementing expectimax

class ExpectimaxAgent(AgentSearchAgent):
  """
    Your expectimax agent (problem 3)
  """

  def getAction(self, gameState):
    # BEGIN_YOUR_CODE (around 25 lines of code expected)
    def recurse(gameState, current_d, agentIndex):
        LegalActions = gameState.getLegalActions()
        if(gameState.returnWinner() is not None or len(LegalActions) == 0):
          return ['',gameState.getScore()]
        if(current_d == 0 and agentIndex == self.index):
          return ['',self.evaluationFunction(gameState)]
        newIndex = agentIndex + 1
        newDepth = current_d
        if newIndex == gameState.getNumAgents():
          newIndex = 0
          newDepth = current_d - 1
        if agentIndex == self.index:
          bestactions = []
          if(agentIndex == 0):
            bestscore = float("-inf")
            player = gameState.getPlayer(agentIndex)
            for action in LegalActions:
              newState = gameState.generateSuccessor(player, action)
              result = recurse(newState,newDepth,newIndex)
              if result[1] == bestscore:
                bestactions.append(action)
              elif result[1] > bestscore:
                bestscore = result[1]
                bestactions = [action]
            return [random.choice(bestactions), bestscore]
          if(agentIndex == 1):
            bestscore = float("inf")
            player = gameState.getPlayer(agentIndex)
            for action in LegalActions:
              newState = gameState.generateSuccessor(player, action)
              result = recurse(newState,newDepth,newIndex)
              if result[1] == bestscore:
                bestactions.append(action)
              elif result[1] < bestscore:
                bestscore = result[1]
                bestactions = [action]
            return [random.choice(bestactions), bestscore]

        else:
          score_list = list()
          player = gameState.getPlayer(agentIndex)
          for action in LegalActions:
            newState = gameState.generateSuccessor(player, action)
            result = recurse(newState,newDepth,newIndex)
            score_list.append(result[1])
          bestscore = sum(score_list)/len(score_list)
          return ['', bestscore]

    result = recurse(gameState, self.depth, self.index)
    return result[0]

    # END_YOUR_CODE

######################################################################################
# Problem 4a (extra credit): creating a better evaluation function

def betterEvaluationFunction(currentGameState):
  """
    Your extreme, unstoppable evaluation function (problem 4).

    DESCRIPTION: This function uses manhattan distance as the main measure of length.
    The evaluation function gives a higher score as pacman gets closer to a food, capsule, or scared ghosts.
    The evaluation function gives a higher score as pacman gets further away from a normal ghost but only
    up until 3 steps away, where it is considered as a safe distance from a ghost. The evaluation function
    gives a lower score with more capsules, food particles, and scared ghosts.
  """
  score = 0
  return score
better = betterEvaluationFunction


