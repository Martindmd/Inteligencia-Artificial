"""Implementation of search functions for reversi.

    Authors:
        Alejandro Bellogin <alejandro.bellogin@uam.es>
"""

import search
import random

from timeit import default_timer as timer
from datetime import timedelta

import util
from reversi import (
    get_valid_moves, 
    enemy_captured_by_move,
    create_standard_board,
    )


class CornerReversiState:
    """
    This class defines the mechanics of a Reversi game.
    The task of recasting this game state as a search problem is left to
    the CornerReversiSearchProblem class.
    """

    def __init__(self, board: dict, player1='B', player2='W', cur_player='B', height=8, width=8, ignore_block_cells_in_captures: bool = False):
        "Creates a new CornerReversiState, very similar to Reversi."
        self.board = board
        self.player1 = player1
        self.player2 = player2
        self.blocked_cell_label = 'O'
        self.cur_player = cur_player
        self.height = height
        self.width = width
        self.ignore_block_cells_in_captures = ignore_block_cells_in_captures

    def isGoal(self, min_corners=1):
        """
          Checks to see if any of the players have conquered min_corners in the board.
        """
        corners = [self.board.get((1, 1)), self.board.get((1, self.height)),
                   self.board.get((self.width, 1)), self.board.get((self.width, self.height))]
        return corners.count(self.player1) + corners.count(self.player2) >= min_corners

    def legalMoves(self):
        """
          Returns a list of legal moves from the current state.
        """
        next_player = self.player2 if self.cur_player == self.player1 else self.player1
        return """YOUR CODE HERE""" # RETURN THE LIST OF VALID MOVES

    def result(self, move):
        """
          Returns a new board with the current state updated based on the provided move.

        NOTE: This function *does not* change the current object.  Instead,
        it returns a new object.
        """
        result_board = self.board.copy()  # shallow copy is enough
        # show the move on the board
        adversary = self.player2 if self.cur_player == self.player1 else self.player1
        result_board[move] = self.cur_player
        # flip enemy
        for enemy in enemy_captured_by_move(self.board, move, self.cur_player, adversary, self.blocked_cell_label, self.ignore_block_cells_in_captures):
            result_board[enemy] = """YOUR CODE HERE""" # update the board
        return """YOUR CODE HERE""" # RETURN THE NEW STATE CONSIDERING THE UPDATES

    # Utilities for comparison and display
    def __eq__(self, other):
        """
            Overloads '=='.
        """
        return self.board == other.board

    def __hash__(self):
        return hash(self.__getAsciiString())

    def __getAsciiString(self):
        """
          Returns a display string for the state
        """
        adversary = self.player2 if self.cur_player == self.player1 else self.player1
        moves = get_valid_moves(self.board, self.height, self.width, self.cur_player, adversary, self.blocked_cell_label, self.ignore_block_cells_in_captures)
        lines = []
        for y in range(0, self.height + 1):
            rowLine = ''
            for x in range(0, self.width + 1):
                if x > 0 and y > 0:
                    if (x, y) in moves:
                        rowLine = rowLine + self.board.get((x, y), '_',)
                    else:
                        rowLine = rowLine + self.board.get((x, y), '.',)
                if x == 0:
                    if y > 0:
                        rowLine = rowLine + str(y) + ' '
                if y == 0:
                    rowLine = rowLine + (chr(x+96) if x > 0 else '  ')
            lines.append(rowLine)
        return '\n'.join(lines)

    def __str__(self):
        return self.__getAsciiString()


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        raise NotImplementedError

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        raise NotImplementedError

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of tuples, 
        (successor, action), where 'successor' is a successor to the current
        state, and 'action' is the action required to get there.
        """
        raise NotImplementedError


class CornerReversiSearchProblem(SearchProblem):
    """
      Implementation of a SearchProblem for Reversi

      Each state is represented by an instance of a valid Reversi board.
      The problem is solved when at least one corner is captured.
    """

    def __init__(self, reversi_state: CornerReversiState):
        "Creates a new ReversiSearchProblem which stores search information."
        self.state = reversi_state

    def getStartState(self):
        return self.state

    def isGoalState(self, state):
        return state.isGoal(1)

    def getSuccessors(self, state):
        """
          Returns list of (successor, action) pairs where
          each succesor is a new board from the original state
        """
        succ = []
        for a in state.legalMoves():
            succ.append((state.result(a), a))
        return succ


class AllCornersReversiSearchProblem(CornerReversiSearchProblem):
    """
      Implementation of a SearchProblem for Reversi

      Each state is represented by an instance of a valid Reversi board.
      The problem is solved when every corner is captured.
    """

    def isGoalState(self, state):
        return state.isGoal(4)


def build_game_tree(search_problem, max_depth):
    """
    Greates a game tree from a search problem until max_depth.
    
    Returns:
    root: the root node of the tree
    stats: a dictionary with the computed statistics
    """
    stats = {
        "nodes": 0,
        "leaves": 0,
        "max_depth": 0,
        "branching_sum": 0,
        "internal_nodes": 0,
        }

    """YOUR CODE HERE"""

    return None, stats


def depthFirstSearch(search_problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", search_problem.getStartState())
    print("Is the start a goal?", search_problem.isGoalState(search_problem.getStartState()))
    print("Start's successors:", search_problem.getSuccessors(search_problem.getStartState()))
    """
    num_visited = 0
    structure = util.Stack()
    structure.push("""YOUR CODE HERE""") # DEFINE THE INITIAL STATE
    visited = []

    while not structure.isEmpty():
        path = structure.pop()
        current_state = """YOUR CODE HERE""" # INDEX THE CURRENT STATE

        if search_problem.isGoalState(current_state):
            return """YOUR CODE HERE""" # RETURN THE PATH OF STATES

        if current_state not in visited:
            visited.append(current_state)

            for successor in search_problem.getSuccessors(current_state):
                if successor[0] not in visited:
                    new_path = """YOUR CODE HERE""" # CREATE THE NEW PATH OF STATES
                    structure.push(new_path)

    return num_visited, None


def breadthFirstSearch(search_problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    raise NotImplementedError



def nullHeuristic(state, search_problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def simpleHeuristic(state, search_problem=None):
    # it rewards states with more coins
    return len(state.board)


def heuristic1(state, search_problem=None):
    "*** YOUR CODE HERE ***"
    return 0


def heuristic2(state, search_problem=None):
    "*** YOUR CODE HERE ***"
    return 0


def heuristic3(state, search_problem=None):
    "*** YOUR CODE HERE ***"
    return 0


def aStarSearch(search_problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    raise NotImplementedError


def createRandomReversiGeneralState(moves, h, w):
    puzzle = CornerReversiState(create_standard_board(h, w, 'B', 'W'), height=h, width=w)
    for _ in range(moves):
        # Execute a random legal move
        puzzle = puzzle.result(random.sample(puzzle.legalMoves(), 1)[0])
    return puzzle


def createSmallRandomReversiState(moves=10):
    """
      moves: number of random moves to apply

      Creates a random Othello board by applying
      a series of 'moves' random moves to a solved
      board. The size of the board is smaller than
      the default board.
    """
    return createRandomReversiGeneralState(moves, 6, 6)


def createRandomReversiState(moves=100):
    """
      moves: number of random moves to apply

      Creates a random Othello board by applying
      a series of 'moves' random moves to a solved
      board.
    """
    return createRandomReversiGeneralState(moves, 8, 8)


if __name__ == '__main__':
    ## variables to play with
    iterations_initial_state = 0
    create_small_board = True
    print_steps = False
    ##

    if create_small_board:
        reversi_state = createSmallRandomReversiState(iterations_initial_state)
    else:
        reversi_state = createRandomReversiState(iterations_initial_state)

    print('Initial state after %d iterations:' % (iterations_initial_state))
    print(reversi_state)

    problem = CornerReversiSearchProblem(reversi_state)
    # for question 1.7
    # problem = AllCornersReversiSearchProblem(reversi_state)
    print('Problem to be solved: %s' % (problem.__class__))

    # game tree
    for depth in [1, 2, 3, 4]:
        root, stats = build_game_tree(problem, depth)
        print('Depth', depth, '\t', stats)


    # search methods
    for method in ['DFS', 'BFS']:
        start = timer()
        if method == 'DFS':
            visited, path = depthFirstSearch(problem)
        elif method == 'BFS':
            visited, path = breadthFirstSearch(problem)
        end = timer()

        if path:
            print_path = [(chr(x+96), y) for x, y in path]
            print('%s found a path of %d moves visiting %d nodes in %s: %s' %
                  (method, len(path), visited, str(timedelta(seconds=end - start)), str(print_path)))
            
            if print_steps:
                curr = reversi_state
                i = 1
                for a in path:
                    cur_player = curr.cur_player
                    curr = curr.result(a)
                    print_a = (chr(a[0]+96), a[1])
                    print('After %d move%s by %s: %s' % (i, ("", "s")[i > 1], cur_player, print_a))
                    print(curr)
        else:
            print('%s found no path in %s' % (method, str(timedelta(seconds=end - start))))

    for h in [
        simpleHeuristic,
        heuristic1,
        heuristic2,
        heuristic3,
        ]:
        method = 'A* with ' + h.__name__
        start = timer()
        visited, path = aStarSearch(problem, h)
        end = timer()

        if path:
            print_path = [(chr(x+96), y) for x, y in path]
            print('%s found a path of %d moves visiting %d nodes in %s: %s' %
                    (method, len(path), visited, str(timedelta(seconds=end - start)), str(print_path)))

            if print_steps:
                curr = reversi_state
                i = 1
                for a in path:
                    cur_player = curr.cur_player
                    curr = curr.result(a)
                    print_a = (chr(a[0]+96), a[1])
                    print('After %d move%s by %s: %s' % (i, ("", "s")[i > 1], cur_player, print_a))
                    print(curr)
        else:
            print('%s found no path in %s' % (method, str(timedelta(seconds=end - start))))
