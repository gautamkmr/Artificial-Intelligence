# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
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
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"
        #print legalMoves[chosenIndex]

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
        newPos = successorGameState.getPacmanPosition()          #new position of the packman in (x,y) form
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        food_list=newFood.asList()
        #initially it is assumed that the food is too far away
        near_food_dist=9999
        #In the below for loop we calculate the distance of nearest food particle to the pacman
        for i in food_list:
            if near_food_dist > (abs(i[0]-newPos[0])+abs(i[1]-newPos[1])):
               near_food_dist=(abs(i[0]-newPos[0])+abs(i[1]-newPos[1]))
        #print near_food_dist
        #next we consider the distance of the ghosts from the pacman.
        ghost_dist=1
        for i in range(0,len(newGhostStates)):
          #print str(newGhostStates[i]),j
          temp1=str(newGhostStates[i]).split(")=(")
          temp1=temp1[1].split(", ")
          x_val=float(temp1[0])
          temp1=temp1[1].split(")")
          y_val=float(temp1[0])
          ghost_dist=ghost_dist*abs(x_val-newPos[0])+abs(y_val-newPos[1])
        #If it is the scared time, the distance of ghost can be assumed to be large, thus gets a boost factor of 10.
        if newScaredTimes > 0:
          ghost_dist=10*ghost_dist
        #the score is inversely propotional to the distance from the nearest food item, as near food item is good for the pacman. Similarly, the score is directly propotional to the ghost distance, as near ghost is not good for the pacman.
        total_score=(ghost_dist)+(1/(10*float(near_food_dist)))
        print ghost_dist, near_food_dist, total_score
        return total_score
        #return successorGameState.getScore()

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
      Your minimax agent (question 2)
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
        """
        "*** YOUR CODE HERE ***"
        #num_of agents is the number of agent in the game. of course there will be pacman, with entry 0. But there can be more than one adversery player, as here we have more than one ghosts.
        num_of_agents=gameState.getNumAgents()
        #thus the real depth is the depth corresponding to each one move by each player. Thus one move by pacman and one ghost is depth one. but representing it over the model we have to treat it as a new depth.
        Actual_depth=self.depth*num_of_agents
        Legal_Actions=gameState.getLegalActions(0)
        #print Legal_Actions
        if Directions.STOP in Legal_Actions:
          Legal_Actions.remove(Directions.STOP)
        new_state=[]
        #corresponding to the pacman we generate it`s valid move
        for i in Legal_Actions:
          new_state.append(gameState.generateSuccessor(0,i))
        #print new_state
        minmax_value=[]
        # and corresponding to each valid move we call the minmax algo, which expands the node for the possible ghosts move, and the correspondingly the pacman`s move, and so on.
        for state in new_state:
          minmax_value.append(self.MinMax(num_of_agents,1,state,Actual_depth-1))
        minmax_index=0
	#once we are with all the pacman`s move with it`s corresponding score, we select the one with highest score. Thus ensuring that pacman plays optimally.
        for minmax_index in range(0,len(minmax_value)):
          if minmax_value[minmax_index]==max(minmax_value):
            break
        #and corresponding to this optimal score, we return the move of pacman.
        return Legal_Actions[minmax_index]
        #util.raiseNotDefined()

    def MinMax(self,no_of_agents,agent_index,gameState,depth):
	#if the present state is the win, or loose, or the max depth to explore, the corresponding evaluation value is returned.
        if (gameState.isLose() or gameState.isWin() or depth==0):
          return self.evaluationFunction(gameState)
	#all legal actions are evaluated
        legal_actions=gameState.getLegalActions(agent_index)
        new_state=[]
	#and correspondingly the legal successors are generated.
        for j in legal_actions:
	  new_state.append(gameState.generateSuccessor(agent_index,j))
        max_value=[]
        min_value=[]
	#now for each state, the minmax algorithm is applied to it`s successor recursively, so that each get to it`s alloted deptha and the score is assigned to it. Or in case of win state or loose, the evaluation value is returned. 
        for state in new_state:
          if agent_index==0:
            max_value.append(self.MinMax(no_of_agents,(agent_index+1)%no_of_agents,state,depth-1))
          else:
            min_value.append(self.MinMax(no_of_agents,(agent_index+1)%no_of_agents,state,depth-1))
	#now each player plays optimally. The ghosts make a move to make the pacman choose the least value, thus most unfavourable, and the pacman make corresponding move, by choosing the best among the available option.
        if agent_index==0:
          return max(max_value)
        else:
          return min(min_value)

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
	#get the number of agent involved in the game
        num_of_agents=gameState.getNumAgents()
	#as earlier gets the actual depth, as the number of agent may be greater than two, one pacman and a ghost.
        Actual_depth=self.depth*num_of_agents
	#corresponding to the pacman, we get the legal move possible.
        Legal_Actions=gameState.getLegalActions(0)
        #print Legal_Actions
        if Directions.STOP in Legal_Actions:
          Legal_Actions.remove(Directions.STOP)
        new_state=[]
	#and corresponding to each legal move, we get the new successor of the pacman position.
        for i in Legal_Actions:
          new_state.append(gameState.generateSuccessor(0,i))
        #print new_state
	#now we will be applying alpha beta prunning, which is similar to the minmax, except that
        alphabeta_value=[]
        for state in new_state:
          alphabeta_value.append(self.Alpha_Beta(num_of_agents,1,state,Actual_depth-1,-1e209,1e209))
        alphabeta_index=0
        #and corresponding to all the values from it`s(pacman) possible move, the one with maximum evaluation value is selected.
        for alphabeta_index in range(0,len(alphabeta_value)):
          if alphabeta_value[alphabeta_index]==max(alphabeta_value):
            break
	#and the corresponding action is returned.
        return Legal_Actions[alphabeta_index]
        #util.raiseNotDefined()

    def Alpha_Beta(self, num_of_agents, agent_index, gameState, depth, alpha, beta):
	#If the state is the win or lose or the set depth state, the evaluation function returns the corresponding value.
        if (gameState.isLose() or gameState.isWin() or depth==0):
          return self.evaluationFunction(gameState)
	#all possible legal actions are computed.
	legal_actions=gameState.getLegalActions(agent_index)
        if ((Directions.STOP in legal_actions) and (agent_index==0)):
          legal_actions.remove(Directions.STOP)
        new_state=[]
	#and corresponding to each legal action the corresponding successor is generated.
        for action in legal_actions:
          new_state.append(gameState.generateSuccessor(agent_index,action))
	#now in case of pacman, the pacman picks the maximum-value. This step also calls the alphabeta prunning algo recursively, to get down to stipulated deapth, or win state, or lose state, and based on these the prunning is done. As if for a subtree, a value is obtained, the for others it can be prunned out based on it`s alpha-beta value.
	if agent_index==0:
          alpha_value=-1e203
          for state in new_state:
            alpha_value=max(self.Alpha_Beta(num_of_agents, (agent_index+1)%num_of_agents, state, depth-1, alpha, beta), alpha_value)
            if alpha_value >= beta:
              return alpha_value
            alpha=max(alpha,alpha_value)
          return alpha_value
	#similarly for the ghosts the prunning is done here.
        else:
          beta_value=1e203
          for state in new_state:
            beta_value=min(self.Alpha_Beta(num_of_agents, (agent_index+1)%num_of_agents, state, depth-1, alpha, beta), beta_value)
            if beta_value <= alpha:
              return beta_value
            beta=min(beta,beta_value)
          return beta_value



class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
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
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
    """
      Your agent for the mini-contest
    """

    def getAction(self, gameState):
        """
          Returns an action.  You can use any method you want and search to any depth you want.
          Just remember that the mini-contest is timed, so you have to trade off speed and computation.

          Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
          just make a beeline straight towards Pacman (or away from him if they're scared!)
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

