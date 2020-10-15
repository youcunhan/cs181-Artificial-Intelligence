# logicPlan.py
# ------------
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


"""
In logicPlan.py, you will implement logic planning methods which are called by
Pacman agents (in logicAgents.py).
"""

import util
import sys
import logic
import game


pacman_str = 'P'
ghost_pos_str = 'G'
ghost_east_str = 'GE'
pacman_alive_str = 'PA'

class PlanningProblem:
    """
    This class outlines the structure of a planning problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the planning problem.
        """
        util.raiseNotDefined()

    def getGhostStartStates(self):
        """
        Returns a list containing the start state for each ghost.
        Only used in problems that use ghosts (FoodGhostPlanningProblem)
        """
        util.raiseNotDefined()
        
    def getGoalState(self):
        """
        Returns goal state for problem. Note only defined for problems that have
        a unique goal state such as PositionPlanningProblem
        """
        util.raiseNotDefined()

def tinyMazePlan(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def sentence1():
    """Returns a logic.Expr instance that encodes that the following inits are all true.
    
    A or B
    (not A) if and only if ((not B) or C)
    (not A) or (not B) or C
    """
    "*** YOUR CODE HERE ***"
    A = logic.Expr('A')
    B = logic.Expr('B')
    C = logic.Expr('C')
    s1 = A | B
    s2 = (~A) % (~B | C)
    s3 = logic.disjoin([~A, ~B, C])
    return logic.conjoin([s1, s2, s3])

def sentence2():
    """Returns a logic.Expr instance that encodes that the following inits are all true.
    
    C if and only if (B or D)
    A implies ((not B) and (not D))
    (not (B and (not C))) implies A
    (not D) implies C
    """
    "*** YOUR CODE HERE ***"
    A = logic.Expr('A')
    B = logic.Expr('B')
    C = logic.Expr('C')
    D = logic.Expr('D')
    s1 = C % (B | D)
    s2 = A >> (~B & ~D)
    s3 = ~(B & ~C) >> A
    s4 = ~D >> C

    return logic.conjoin([s1, s2, s3, s4])

def sentence3():
    """Using the symbols WumpusAlive[1], WumpusAlive[0], WumpusBorn[0], and WumpusKilled[0],
    created using the logic.PropSymbolExpr constructor, return a logic.PropSymbolExpr
    instance that encodes the following English sentences (in this order):

    The Wumpus is alive at time 1 if and only if the Wumpus was alive at time 0 and it was
    not killed at time 0 or it was not alive and time 0 and it was born at time 0.

    The Wumpus cannot both be alive at time 0 and be born at time 0.

    The Wumpus is born at time 0.
    """
    "*** YOUR CODE HERE ***"
    alive1 = logic.PropSymbolExpr('WumpusAlive', 1)
    alive0 = logic.PropSymbolExpr('WumpusAlive', 0)
    born0 = logic.PropSymbolExpr('WumpusBorn', 0)
    killed0 = logic.PropSymbolExpr('WumpusKilled', 0)
    s1 = alive1 % (alive0 & ~killed0 | ~alive0 & born0)
    s2 = ~(alive0 & born0)
    s3 = born0

    return logic.conjoin([s1, s2, s3])


def findModel(sentence):
    """Given a propositional logic sentence (i.e. a logic.Expr instance), returns a satisfying
    model if one exists. Otherwise, returns False.
    """
    "*** YOUR CODE HERE ***"

    cnf = logic.to_cnf(sentence)
    sol = logic.pycoSAT(cnf)
    
    return sol

def atLeastOne(literals) :
    """
    Given a list of logic.Expr literals (i.e. in the form A or ~A), return a single 
    logic.Expr instance in CNF (conjunctive normal form) that represents the logic 
    that at least one of the literals in the list is true.
    >>> A = logic.PropSymbolExpr('A');
    >>> B = logic.PropSymbolExpr('B');
    >>> symbols = [A, B]
    >>> atleast1 = atLeastOne(symbols)
    >>> model1 = {A:False, B:False}
    >>> print logic.pl_true(atleast1,model1)
    False
    >>> model2 = {A:False, B:True}
    >>> print logic.pl_true(atleast1,model2)
    True
    >>> model3 = {A:True, B:True}
    >>> print logic.pl_true(atleast1,model2)
    True
    """
    "*** YOUR CODE HERE ***"
    return logic.disjoin(literals)


def atMostOne(literals) :
    """
    Given a list of logic.Expr literals, return a single logic.Expr instance in 
    CNF (conjunctive normal form) that represents the logic that at most one of 
    the inits in the list is true.
    """
    "*** YOUR CODE HERE ***"
    conjunctions = []
    for i in literals:
        for j in literals:
            if i != j:
                conjunctions.append(~i | ~j)

    return logic.conjoin(conjunctions)


def exactlyOne(literals) :
    """
    Given a list of logic.Expr literals, return a single logic.Expr instance in 
    CNF (conjunctive normal form)that represents the logic that exactly one of 
    the inits in the list is true.
    """
    "*** YOUR CODE HERE ***"
    conjunctions = []
    true_list = []
    for literal in literals:
        true_list.append(literal)

        reached = False
        for inner_literal in literals:
            if reached:
                not_inner_literal = ~inner_literal
                disjunction = logic.disjoin(~literal, not_inner_literal)
                conjunctions.append(disjunction)
            if literal == inner_literal:
                reached = True

    true_one = logic.disjoin(true_list)
    conjunctions.append(true_one)

    return logic.conjoin(conjunctions)


def extractActionSequence(model, actions):
    """
    Convert a model in to an ordered list of actions.
    model: Propositional logic model stored as a dictionary with keys being
    the symbol strings and values being Boolean: True or False
    Example:
    >>> model = {"North[3]":True, "P[3,4,1]":True, "P[3,3,1]":False, "West[1]":True, "GhostScary":True, "West[3]":False, "South[2]":True, "East[1]":False}
    >>> actions = ['North', 'South', 'East', 'West']
    >>> plan = extractActionSequence(model, actions)
    >>> print plan
    ['West', 'South', 'North']
    """
    "*** YOUR CODE HERE ***"
    models = []
    final = []
    for i in model.keys():
        if model[i]:
            a = logic.PropSymbolExpr.parseExpr(i)
            if a[0] in actions:
                models.append(a)
    models = sorted(models, key=lambda key: int(key[1]))
    for m in models:
        final.append(m[0])

    return final


def pacmanSuccessorStateAxioms(x, y, t, walls_grid):
    """
    Successor state axiom for state (x,y,t) (from t-1), given the board (as a 
    grid representing the wall locations).
    Current <==> (previous position at time t-1) & (took action to move to x, y)
    """
    "*** YOUR CODE HERE ***"
    currentposi = logic.PropSymbolExpr(pacman_str, x, y, t)

    allPossibleActions = []

    if not walls_grid[x-1][y]:
        prev_posi = logic.PropSymbolExpr(pacman_str, x-1, y, t-1)
        action = logic.PropSymbolExpr('East', t-1)
        state = logic.conjoin(prev_posi, action)
        allPossibleActions.append(state)

    if not walls_grid[x+1][y]:
        prev_posi = logic.PropSymbolExpr(pacman_str, x+1, y, t-1)
        action = logic.PropSymbolExpr('West', t-1)
        state = logic.conjoin(prev_posi, action)
        allPossibleActions.append(state)

    if not walls_grid[x][y-1]:
        prev_posi = logic.PropSymbolExpr(pacman_str, x, y-1, t-1)
        action = logic.PropSymbolExpr('North', t-1)
        state = logic.conjoin(prev_posi, action)
        allPossibleActions.append(state)

    if not walls_grid[x][y+1]:
        prev_posi = logic.PropSymbolExpr(pacman_str, x, y+1, t-1)
        action = logic.PropSymbolExpr('South', t-1)
        state = logic.conjoin(prev_posi, action)
        allPossibleActions.append(state)

    res = currentposi % logic.disjoin(allPossibleActions)
    return res


def positionLogicPlan(problem):
    """
    Given an instance of a PositionPlanningProblem, return a list of actions that lead to the goal.
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    walls = problem.walls
    width, height = problem.getWidth(), problem.getHeight()
    
    "*** YOUR CODE HERE ***"
    actions = ['North', 'East', 'South', 'West']
    init_state = problem.getStartState()
    goal_state = problem.getGoalState()
    init = None

    for x in range(1, width+1) :
        for y in range(1, height+1) :
            if (x, y) == init_state:
                if init != None:
                    init &= logic.PropSymbolExpr(pacman_str, x, y, 0)
                else:
                    init = logic.Expr(logic.PropSymbolExpr(pacman_str, x, y, 0))
            else:
                if init:
                    init &= ~logic.PropSymbolExpr(pacman_str, x, y, 0)
                else:
                    init = ~logic.PropSymbolExpr(pacman_str, x, y, 0)

    successors = []
    restriction = []
    t = 0
    while 1:
        tmp = []
        if t > 0:
            for x in range(1, width + 1):
                for y in range(1, height + 1):
                    if (x, y) not in walls.asList():
                        tmp.append(pacmanSuccessorStateAxioms(x, y, t, walls))
            successor = logic.conjoin(tmp)
            if successors:
                success = successor & logic.conjoin(successors)
            else:
                success = successor
            successors.append(successor)


            tmp = []
            for action in actions:
                tmp.append(logic.PropSymbolExpr(action, t-1))
            restrictionFort = exactlyOne(tmp)
            restriction.append(restrictionFort)
            restrictions = logic.conjoin(restriction)

            goal = logic.conjoin(logic.PropSymbolExpr(pacman_str, goal_state[0], goal_state[1], t+1), pacmanSuccessorStateAxioms(goal_state[0], goal_state[1], t+1, walls))
            sol = findModel(logic.conjoin(init, goal, restrictions, success))

        else:
            goal = logic.conjoin(logic.PropSymbolExpr(pacman_str, goal_state[0], goal_state[1], t+1), pacmanSuccessorStateAxioms(goal_state[0], goal_state[1], t+1, walls))
            sol = findModel(logic.conjoin(init, goal))
        if sol != False:
            return extractActionSequence(sol, actions)

        t += 1


def foodLogicPlan(problem):
    """
    Given an instance of a FoodPlanningProblem, return a list of actions that help Pacman
    eat all of the food.
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    walls = problem.walls
    width, height = problem.getWidth(), problem.getHeight()

    "*** YOUR CODE HERE ***"
    actions = ['North', 'East', 'South', 'West']
    init_state = problem.getStartState()
    pacman_init_location = init_state[0]
    food_locations = init_state[1].asList()

    init = None

    for x in range(1, width+1) :
        for y in range(1, height+1) :
            if (x, y) == pacman_init_location:
                if init != None:
                    init &= logic.PropSymbolExpr(pacman_str, x, y, 0)
                else:
                    init = logic.Expr(logic.PropSymbolExpr(pacman_str, x, y, 0))
            else:
                if init:
                    init &= ~logic.PropSymbolExpr(pacman_str, x, y, 0)
                else:
                    init = ~logic.PropSymbolExpr(pacman_str, x, y, 0)
    successors = []
    restrictions = []
    t = 0
    while 1:
        tmp = []
        if t > 0:
            for x in range(1, width + 1):
                for y in range(1, height + 1):
                    if (x, y) not in walls.asList():
                        tmp += [pacmanSuccessorStateAxioms(x, y, t, walls)]
            successor = logic.conjoin(tmp)
            if successors:
                success = successor & logic.conjoin(successors)
            else:
                success = successor
            successors.append(successor)

            tmp = []
            for action in actions:
                tmp.append(logic.PropSymbolExpr(action, t-1))
            n = exactlyOne(tmp)
            restrictions.append(n)
            restriction = logic.conjoin(restrictions)

            food_locations_eaten = list()
            for food_particle in food_locations:
                food_particles = list()
                for i in range(0, t+1):
                    food_particles.append(logic.PropSymbolExpr(pacman_str, food_particle[0], food_particle[1], i))
                food_particles = logic.disjoin(food_particles)
                food_locations_eaten.append(food_particles)
            food_locations_eaten = logic.conjoin(food_locations_eaten)
            sol = findModel(logic.conjoin(init, food_locations_eaten, restriction, success))
        else:
            food_locations_eaten = list()
            for food_particle in food_locations:
                food_locations_eaten.append(logic.PropSymbolExpr(pacman_str, food_particle[0], food_particle[1], 0))
            food_locations_eaten = logic.conjoin(food_locations_eaten)
            sol = findModel(logic.conjoin(init, food_locations_eaten))
        if sol != False:
            return extractActionSequence(sol, actions)

        t += 1


# Abbreviations
plp = positionLogicPlan
flp = foodLogicPlan

# Some for the logic module uses pretty deep recursion on long inits
sys.setrecursionlimit(100000)
    