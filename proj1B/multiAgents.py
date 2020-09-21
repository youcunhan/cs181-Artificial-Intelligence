# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


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


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
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

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 1)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        maxVal = float('-inf')
        bestAction = None
        for action in gameState.getLegalActions(0):
            value = self.getMin(gameState.generateSuccessor(0, action),0,1)
            if value > maxVal:
                maxVal = value
                bestAction = action
        return bestAction

        
    def getMax(self, gameState, depth, agentIndex):
        if depth == self.depth:
            return self.evaluationFunction(gameState)
        if len(gameState.getLegalActions(agentIndex)) == 0:
            return self.evaluationFunction(gameState)
        maxVal = float('-inf')
        for action in gameState.getLegalActions(agentIndex):
            value = self.getMin(gameState.generateSuccessor(agentIndex, action), depth, agentIndex + 1)
            if value > maxVal:
                maxVal = value
        return maxVal            


    def getMin(self, gameState, depth, agentIndex):
        if depth == self.depth:
            return self.evaluationFunction(gameState)
        if len(gameState.getLegalActions(agentIndex)) == 0:
            return self.evaluationFunction(gameState)
        minVal = float('inf')
        for action in gameState.getLegalActions(agentIndex):
            if agentIndex == gameState.getNumAgents()-1:
                value = self.getMax(gameState.generateSuccessor(agentIndex, action), depth + 1, 0)
            else:
                value = self.getMin(gameState.generateSuccessor(agentIndex, action), depth,agentIndex + 1)
            if value < minVal:
                minVal = value
        return minVal

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return self.getMax(gameState, 0, 0, float('-inf'), float('inf'))[1]

    # getMax主要是计算吃豆人选择最佳的动作
    def getMax(self, gameState, depth,agentIndex, alpha, beta):
        # 如果达到搜索深度，则将当前状态的评价值返回
        if depth == self.depth:
            return self.evaluationFunction(gameState),None
        # 如果接下来没有可行的行动，也要终止迭代
        if len(gameState.getLegalActions(agentIndex)) == 0:
            return self.evaluationFunction(gameState),None
        # 获得吃豆人的所有可行操作，并进行遍历
        maxVal = -float('inf')
        bestAction = None
        for action in gameState.getLegalActions(agentIndex):
            # 参数中最后的“1”，表示接下来的动作是计算鬼怪的行动影响
            value = self.getMin(gameState.generateSuccessor(agentIndex, action),depth,agentIndex+1,alpha,beta)[0]
            if value>maxVal:
                maxVal = value
                bestAction = action
            # 如果v>beta,
            if value>beta:
                return value,action
            alpha = value if value>alpha else alpha
        return maxVal,bestAction

    # getMin主要是计算鬼怪选择造成最坏影响的动作
    def getMin(self,gameState,depth=0,agentIndex=1,alpha=-float('inf'),beta=float('inf')):
        # 如果达到搜索深度，则将当前状态的评价值返回
        if depth == self.depth:
            return self.evaluationFunction(gameState),None
        # 如果接下来没有可行的行动，也要终止迭代
        if len(gameState.getLegalActions(agentIndex)) == 0:
            return self.evaluationFunction(gameState),None
        # 获得当前鬼怪的所有可行操作，并进行遍历
        minVal = float('inf')
        bestAction = None
        for action in gameState.getLegalActions(agentIndex):
            # 如果你是最后一个鬼怪的agent，那么接下来就要去计算吃豆人的行动，否则就去计算下一个鬼怪的行动
            if agentIndex == gameState.getNumAgents()-1:
                # 参数中最后的“0”，表示接下来的动作是计算吃豆人的行动影响
                value = self.getMax(gameState.generateSuccessor(agentIndex, action),depth+1,0,alpha,beta)[0]
            else:
                # 参数中最后的agentIndex(大于1)，表示接下来的动作是计算鬼怪的行动影响
                value = self.getMin(gameState.generateSuccessor(agentIndex, action),depth,agentIndex+1,alpha,beta)[0]
            if value<minVal:
                minVal = value
                bestAction = action
            if value<alpha:
                return value,action
            beta = value if value<beta else beta # 这个条件选择语句和C语言中"exp1?exp2:exp3"一样
        return minVal,bestAction

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 4).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
