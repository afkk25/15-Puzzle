# search.py

# ---------
# Licensing Information: You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.

# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).
"""
In search.py, we implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
        state: Search state
        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
        state: Search state
        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
        actions: A list of actions to take
        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()

def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze. For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """Search the deepest nodes in the search tree first."""

    # define start node
    frontier = [(problem.getStartState(), [])]
    explored = set() # Using a set for better accessibility
    repeated_states = set()  # To detect repeated states
    expanded_nodes_count = 0  # Initialize the expanded nodes count

    while frontier:
        state, actions = frontier.pop()

        if problem.isGoalState(state):
            return actions, expanded_nodes_count

        if state not in explored:
            expanded_nodes_count += 1  # Increment the expanded nodes count
            explored.add(state)
            successors = problem.getSuccessors(state)

            for next_state, action, _ in successors:
                if next_state not in repeated_states:  # Check for repeated states
                    frontier.append((next_state, actions + [action]))
                else:
                    #===== Start Change Task 4 =====*/
                    return None, expanded_nodes_count  # No solution found due to infinite loop
                    #===== End Change Task 4 =====*/
                repeated_states.add(next_state)
                
    #===== Start Change Task 4 =====*/
    return [], expanded_nodes_count  # No solution found
    #===== End Change Task 4 =====*/


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    #to be explored (FIFO)
    frontier = util.Queue()
    #previously expanded states (for cycle checking), holds states
    exploredNodes = []

    startState = problem.getStartState()
    startNode = (startState, [], 0) #(state, action, cost)
    frontier.push(startNode)

    while not frontier.isEmpty():
        #begin exploring first (earliest-pushed) node on frontier
        currentState, actions, currentCost = frontier.pop()

        if currentState not in exploredNodes:
            #put popped node state into explored list
            exploredNodes.append(currentState)

            if problem.isGoalState(currentState):
                return actions
            else:
                #list of (successor, action, stepCost)
                successors = problem.getSuccessors(currentState)

                for succState, succAction, succCost in successors:
                    newAction = actions + [succAction]
                    newCost = currentCost + succCost
                    newNode = (succState, newAction, newCost)
                    frontier.push(newNode)
    return actions

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    #to be explored (FIFO): holds (item, cost)
    frontier = util.PriorityQueue()
    #previously expanded states (for cycle checking), holds state:cost
    exploredNodes = {}

    startState = problem.getStartState()
    startNode = (startState, [], 0) #(state, action, cost)
    frontier.push(startNode, 0)

    while not frontier.isEmpty():
        #begin exploring first (lowest-cost) node on frontier
        currentState, actions, currentCost = frontier.pop()

        if (currentState not in exploredNodes) or (currentCost < exploredNodes[currentState]):
            #put popped node's state into explored list
            exploredNodes[currentState] = currentCost

            if problem.isGoalState(currentState):
                return actions
            else:
                #list of (successor, action, stepCost)
                successors = problem.getSuccessors(currentState)

                for succState, succAction, succCost in successors:
                    newAction = actions + [succAction]
                    newCost = currentCost + succCost
                    newNode = (succState, newAction, newCost)
                    frontier.update(newNode, newCost)
    return actions

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    #to be explored (FIFO): takes in item, cost+heuristic
    frontier = util.PriorityQueue()
    exploredNodes = [] #holds (state, cost)

    startState = problem.getStartState()
    startNode = (startState, [], 0) #(state, action, cost)
    frontier.push(startNode, 0)

    while not frontier.isEmpty():
        #begin exploring first (lowest-combined (cost+heuristic) ) node on frontier
        currentState, actions, currentCost = frontier.pop()

        #put popped node into explored list
        currentNode = (currentState, currentCost)
        exploredNodes.append((currentState, currentCost))

        if problem.isGoalState(currentState):
            return actions

        else:
            #list of (successor, action, stepCost)
            successors = problem.getSuccessors(currentState)

            #examine each successor
            for succState, succAction, succCost in successors:
                newAction = actions + [succAction]
                newCost = problem.getCostOfActions(newAction)
                newNode = (succState, newAction, newCost)

                #check if this successor has been explored
                already_explored = False
                for explored in exploredNodes:
                    #examine each explored node tuple
                    exploredState, exploredCost = explored
                    if (succState == exploredState) and (newCost >= exploredCost):
                        already_explored = True

                #if this successor not explored, put on frontier and explored list
                if not already_explored:
                    #start task
                    frontier.push(newNode, newCost + heuristic(succState))
                    #end task
                    exploredNodes.append((succState, newCost))
    return actions

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch