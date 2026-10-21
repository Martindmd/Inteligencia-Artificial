from collections.abc import Sequence

import numpy as np

from game import (
    TwoPlayerGameState,
)
from heuristic import (
    simple_evaluation_function,
)
from reversi import Reversi, get_valid_moves
from tournament import (
    StudentHeuristic,
)

VICTORY_SCORE = 99999


def func_glob(n: int, state: TwoPlayerGameState) -> float:
    return n + simple_evaluation_function(state)


class Solution1(StudentHeuristic):
    """
    La función heurística "morning-victory" combina la funcionalidad de las otras dos estrategias heurísticas:
    para minimalist, va sumando menos conforme va avanzando el juego, ya que la estrategia es más efectiva en los early stages
    """

    def get_name(self) -> str:
        return "morning-victory"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        # combination of both heuristics
        total_score = state.scores[0] + state.scores[1]
        """print(" first score --> " + str(state.scores[0]))
        print(" second score --> " + str(state.scores[1]))
        print(total_score)"""
        if total_score <= 15:
            return Solution2.evaluation_function(self, state) + Solution3.evaluation_function(self, state)
        elif total_score <= 30:
            return Solution2.evaluation_function(self, state) + 0.5 * Solution3.evaluation_function(self, state)
        else:
            return Solution2.evaluation_function(self, state)


class Solution2(StudentHeuristic):
    def get_name(self) -> str:
        return "underdog"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        if state.end_of_game:
            scores = state.scores
            # Evaluation of the state from the point of view of MAX

            assert isinstance(scores, (Sequence, np.ndarray))
            score_difference = scores[0] - scores[1]

            if state.is_player_max(state.player1):
                state_value = score_difference
            elif state.is_player_max(state.player2):
                state_value = -score_difference
            else:
                raise ValueError("Player MAX not defined")

            return state_value

        score = 0
        for x in range(7):
            for y in range(7):
                if state.player_max.label == state.board.get((x + 1, y + 1)):
                    BOARD = [120, -20, 20, 5, 5, 20, -20, 120,
                             -20, -40, -5, -5, -5, -40, -20,
                             5, -5, 3, 3, 3, 3, -5, 5,
                             5, -5, 3, 3, 3, 3, -5, 5,
                             - 20, -40, -5, -5, -5, -40, -20,
                             120, -20, 20, 5, 5, 20, -20, 120, ]
                    score = score + BOARD[x % 8 + y - 1]
        return score


class Solution3(StudentHeuristic):
    """prioriza aquellos estados en los que max_player
    tiene la menor cantidad de piezas posibles"""

    def get_name(self) -> str:
        return "minimalist"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        number_max = None
        number_min = None
        if state.player1.label == state.player_max.label:
            number_max = 0
            number_min = 1
        else:
            number_max = 1
            number_min = 0
        scores_max = state.scores[number_max]
        scores_min = state.scores[number_min]

        state_value = 0
        if scores_max > scores_min:
            state_value += -15
        else:
            state_value += 15
        if state.end_of_game:
            scores = state.scores
            score_difference = scores[0] - scores[1]

            if state.is_player_max(state.player1):
                state_value = score_difference
            elif state.is_player_max(state.player2):
                state_value = -score_difference
            else:
                raise ValueError("Player MAX not defined")

        return state_value + Solution4.evaluation_function(self, state)


class Solution4(StudentHeuristic):
    """prioriza aquellos estados en los que max_player
    tiene la menor cantidad de piezas posibles"""

    def get_name(self) -> str:
        return "uh"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        if state.end_of_game:
            scores = state.scores
            # Evaluation of the state from the point of view of MAX

            assert isinstance(scores, (Sequence, np.ndarray))
            score_difference = scores[0] - scores[1]

            if state.is_player_max(state.player1):
                state_value = score_difference
            elif state.is_player_max(state.player2):
                state_value = -score_difference
            else:
                raise ValueError("Player MAX not defined")

            return state_value

        enemy_label = (
            state.player2.label
            if state.player_max.label == state.player1.label
            else state.player1.label
        )

        return len(get_valid_moves(state.board, 8, 8, state.player_max.label, enemy_label, "O", False))
