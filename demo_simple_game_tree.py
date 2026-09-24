"""Illustration of a match for a game tree.

    Author:
        Alberto Suárez <alberto.suarez@uam.es>
"""
from __future__ import annotations  # For Python 3.7

from game import Player, TwoPlayerGameState, TwoPlayerMatch
from heuristic import heuristic
from simple_game_tree import SimpleGameTree
from strategy import (
    MinimaxAlphaBetaStrategy,
    MinimaxStrategy,
)

# Define players

player1_minimax = Player(
    name='Minimax 1',
    strategy=MinimaxStrategy(
        heuristic=heuristic,
        max_depth_minimax=4,
        verbose=3,
    ),
)

player2_minimax = Player(
    name='Minimax 4',
    strategy=MinimaxStrategy(
        heuristic=heuristic,
        max_depth_minimax=4,
        verbose=3,
    ),
)

player1_minimax_alpha_beta = Player(
    name='Minimax + alpha-beta 1',
    strategy=MinimaxAlphaBetaStrategy(
        heuristic=heuristic,
        max_depth_minimax=4,
        verbose=3,
    ),
)


player2_minimax_alpha_beta = Player(
    name='Minimax + alpha-beta 2',
    strategy=MinimaxAlphaBetaStrategy(
        heuristic=heuristic,
        max_depth_minimax=4,
        verbose=3,
    ),
)

# Select players

player1, player2 = player1_minimax, player2_minimax
# player1, player2 = player1_minimax_alpha_beta, player2_minimax_alpha_beta

game = SimpleGameTree(
    player1=player1,
    player2=player2,
)

"""
Here you can initialize the board and the player who moves first
to any valid state; e.g., it can be an intermediate state.
"""

# Select initial player

initial_player = player1

# Setup and play match

game_state = TwoPlayerGameState(
    game=game,
    initial_player=initial_player,
    board='A',
)

match = TwoPlayerMatch(
    game_state,
    max_seconds_per_move=10000,
)

scores = match.play_match()
