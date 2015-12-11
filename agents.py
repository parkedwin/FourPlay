
import random

class Agent:
  def __init__(name, index=0):
    self.id = name

  def getAction(self, state):
    raiseNotDefined()

class ReflexAgent(Agent):
  """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.
  """
  def __init__(self, name, opp_name, maximize = True):
    self.dc = None
    self.max = maximize
    self.id = name
    self.opp = opp_name


  def getAction(self, gameState):
    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions()

    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    # print scores
    if(self.max):
      bestScore = max(scores)
    else:
      bestScore = min(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best

    return legalMoves[chosenIndex]

  def evaluationFunction(self, currentGameState, action):
    successorGameState = currentGameState.generateSuccessor(self.id, action)
    scores = []
    for action in successorGameState.getLegalActions():
      successorGameState2 = successorGameState.generateSuccessor(self.opp, action)
      scores.append(successorGameState2.getScore())
    if(self.max):
      return min(scores)
    else:
      return max(scores)

def scoreEvaluationFunction(currentGameState):
  return currentGameState.getScore()

class AlphaBetaAgent(Agent):
  """
    Your minimax agent with alpha-beta pruning (problem 2)
  """
  def __init__(self, name, opp_name, maximize = 1, depth = 1, evalFn = scoreEvaluationFunction):
    self.dc = None
    self.max = maximize
    self.id = name
    self.opponent = opp_name
    self.evaluationFunction = evalFn
    self.depth = depth
    
  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    def getCurrentPlayer(turn):
      if(turn * self.max > 0):
        return self.id
      return self.opponent 

    def recurse(gameState, current_d, turn, threshold):
        LegalActions = gameState.getLegalActions()
        if(gameState.returnWinner() is not None or len(LegalActions) == 0):
          return ['',gameState.getScore()]
        if(current_d == 0):
          return ['',self.evaluationFunction(gameState)]
        new_turn = -1*turn
        newDepth = current_d
        if new_turn == self.max:
          newDepth = current_d - 1

        bestactions = []
        player = getCurrentPlayer(turn)
        #likes to maximize
        if turn > 0:
          bestscore = float("-inf")
          for action in LegalActions:
            newState = gameState.generateSuccessor(player, action)
            result = recurse(newState,newDepth,new_turn,bestscore)
            if result[1] == bestscore:
              bestactions.append(action)
            if result[1] > bestscore:
              bestscore = result[1]
              bestactions = [action]
            if result[1] > threshold:
              return[random.choice(bestactions), bestscore]
        else: #minimizer
          bestscore = float("inf")
          for action in LegalActions:
            newState = gameState.generateSuccessor(player, action)
            result = recurse(newState,newDepth,new_turn,bestscore)
            if result[1] == bestscore:
              bestactions.append(action)
            if result[1] < bestscore:
              bestscore = result[1]
              bestactions = [action]
            if(result[1] < threshold):
              return [random.choice(bestactions),bestscore]
        return [random.choice(bestactions), bestscore]

    if(self.max > 0 and self.id != gameState.players[1]):
      raise AssertionError("Alpha Beta instance set up backwards")
    if(self.max < 0 and self.id != gameState.players[2]):
      raise AssertionError("Alpha Beta instance set up backwards")

    if(self.max > 0):
      threshold = float("inf")
    else:
      threshold = float("-inf") 
    result = recurse(gameState, self.depth, self.max, threshold)
    return result[0]


def betterEvaluationFunction(currentGameState):
  score = currentGameState.getScore()
  pattern_score = []
  weight2 = 4554.46
  weight3 = 6986.67
  pattern_score.append(([1,1,0,0], weight2))
  pattern_score.append(([1,1,1,0], weight3))
  pattern_score.append(([2,2,0,0], -weight2))
  pattern_score.append(([2,2,2,0], -weight3))
  patterns = [thing[0] for thing in pattern_score]
  counts = currentGameState.getAllCounts(patterns,4,0)

  for index,count in enumerate(counts):
    score += count*pattern_score[index][1]

  offset_patterns_score = []
  offset_patterns_score.append(([0,1,1,0], weight2))
  offset_patterns_score.append(([0,2,2,0], -weight2))
  off_patterns = [thing[0] for thing in offset_patterns_score]
  off_counts = currentGameState.getAllCounts(off_patterns,4,1)
  for index,count in enumerate(off_counts):
    score += count*int(offset_patterns_score[index][1]) / 2 

  return score
better = betterEvaluationFunction


