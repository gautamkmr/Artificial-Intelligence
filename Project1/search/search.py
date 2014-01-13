# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
"""

import util
import searchAgents
from game import Directions

class SearchProblem:
  """
  This class outlines the structure of a search problem, but doesn't implement
  any of the methods (in object-oriented terminology: an abstract class).
  
  You do not need to change anything in this class, ever.
  """
  
  def getStartState(self):
     """
     Returns the start state for the search problem 
     """
     util.raiseNotDefined()
    
  def isGoalState(self, state):
     """
       state: Search state
    
     Returns True if and only if the state is a valid goal state
     """
     util.raiseNotDefined()

  def getSuccessors(self, state):
     """
       state: Search state
     
     For a given state, this should return a list of triples, 
     (successor, action, stepCost), where 'successor' is a 
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental 
     cost of expanding to that successor
     """
     util.raiseNotDefined()

  def getCostOfActions(self, actions):
     """
      actions: A list of actions to take
 
     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
     """
     util.raiseNotDefined()
           

def tinyMazeSearch(problem):
  """
  Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence of moves will be incorrect, so only use this for tinyMaze
  """
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first [p 85].
  
  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm [Fig. 3.7].
  
  To get started, you might want to try some of these simple commands to
  understand the search problem that is being passed in:
  
  print "Start:", problem.getStartState()
  print "Is the start a goal?", problem.isGoalState(problem.getStartState())
  print "Start's successors:", problem.getSuccessors(problem.getStartState())
  """
  "*** YOUR CODE HERE ***"
  unexplored_node=util.Stack()     #the nodes that have been found but not explored, i..e their successor`s have not been discovered.
  search_direction=util.Stack()
  explored_node=[] #all nodes that have been found.It ensures that a visited node isn`t selected again.No pop operation,to store all found values.
  unexplored_node.__init__()
  search_direction.__init__()
  unexplored_node.push(problem.getStartState())
  search_direction.push([])
  explored_node.append(problem.getStartState())
  print "Start:", problem.getStartState()
  while(unexplored_node.isEmpty()==False):
        testing_node=unexplored_node.pop()
        lead_direction=search_direction.pop()
        if problem.isGoalState(testing_node)==False:
               successor_node=problem.getSuccessors(testing_node)
               i=0                           #each successor node has three part,(successor node, direction, length of path)
               while(i<len(successor_node)):
                     if successor_node[i][0] not in explored_node:
                          unexplored_node.push(successor_node[i][0])
                          explored_node.append(successor_node[i][0])
                          push_direction=lead_direction[:]
                          push_direction.append(successor_node[i][1])
                          search_direction.push(push_direction)
                     i=i+1
        else:
               print "Got the solution", testing_node
               print lead_direction
               break
  return lead_direction
#  util.raiseNotDefined()

def breadthFirstSearch(problem):
  "Search the shallowest nodes in the search tree first. [p 81]"
  "*** YOUR CODE HERE ***"
  unexplored_node=util.Queue()
  search_direction=util.Queue()
  explored_node=[]
  unexplored_node.__init__()
  search_direction.__init__()
  unexplored_node.push(problem.getStartState())
  search_direction.push([])
  explored_node.append(problem.getStartState())
  print "Start:", problem.getStartState()
  while(unexplored_node.isEmpty()==False):
        testing_node=unexplored_node.pop()
        lead_direction=search_direction.pop()
        if problem.isGoalState(testing_node)==False:
               successor_node=problem.getSuccessors(testing_node)
               i=0
               while(i<len(successor_node)):
                     if successor_node[i][0] not in explored_node:
                          unexplored_node.push(successor_node[i][0])
                          explored_node.append(successor_node[i][0])
                          push_direction=lead_direction[:]
                          push_direction.append(successor_node[i][1])
                          search_direction.push(push_direction)
                     i=i+1
        else:
               print "Got the solution", testing_node
               print lead_direction
               break
  return lead_direction
#  util.raiseNotDefined()
      
def uniformCostSearch(problem):
  "Search the node of least total cost first. "
  "*** YOUR CODE HERE ***"
  unexplored_node=util.PriorityQueue()
  found_node=[]   #nodes that have been found, to avoid adding same node in P-queue multiple times.
  unexplored_node.__init__()
  unexplored_node.push(problem.getStartState(),[],0) # 3 parameters, (state, direction, priority) to be passed.
  found_node.append(problem.getStartState())
  unexplored_node.display()
  print "Start:", problem.getStartState()
  while(unexplored_node.isEmpty()==False):
        testing_node=unexplored_node.pop()
        if problem.isGoalState(testing_node[0])==False:
               successor_node=problem.getSuccessors(testing_node[0]) # successor node=(node, direction, path length)
               i=0
               while(i<len(successor_node)):
                     if successor_node[i][0] not in found_node:
                          push_direction=testing_node[1][:]
			  push_direction.append(successor_node[i][1])
                          unexplored_node.push(successor_node[i][0],push_direction,successor_node[i][2]+testing_node[2])
                          found_node.append(successor_node[i][0])
                     i=i+1
        else:
               print "Got the solution", testing_node
               break
  return testing_node[1]
#  util.raiseNotDefined()

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."
  "*** YOUR CODE HERE ***"
  #same as the uniform cost function but has also got h-value along with path length to decide the priority. 
  unexplored_node=util.PriorityQueue()
  found_node=[]
  unexplored_node.__init__()
  unexplored_node.push(problem.getStartState(),[],0+heuristic(problem.getStartState(),problem))
  found_node.append(problem.getStartState())
  unexplored_node.display()
  print "Start:", problem.getStartState()
  while(unexplored_node.isEmpty()==False):
        testing_node=unexplored_node.pop()
        if problem.isGoalState(testing_node[0])==False:
               successor_node=problem.getSuccessors(testing_node[0])
               i=0
               while(i<len(successor_node)):
                     if successor_node[i][0] not in found_node:
                          push_direction=testing_node[1][:]
			  push_direction.append(successor_node[i][1])
                          unexplored_node.push(successor_node[i][0],push_direction,successor_node[i][2]+testing_node[2]+heuristic(successor_node[i][0],problem))
#			  print heuristic(successor_node[i][0],problem)
                          found_node.append(successor_node[i][0])
                     i=i+1
        else:
               print "Got the solution", testing_node
               break
  return testing_node[1]
#  util.raiseNotDefined()
    
  
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
