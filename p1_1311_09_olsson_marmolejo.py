from collections.abc import Sequence

import numpy as np

from game import (
    TwoPlayerGameState,
)
from heuristic import (
    simple_evaluation_function,
)
from tournament import (
    StudentHeuristic,
)


def func_glob(n: int, state: TwoPlayerGameState) -> float:
    return n + simple_evaluation_function(state)


class Solution1(StudentHeuristic):
    """
    La función heurística "random-esque" asigna un valor aleatorio a los estados de juego,
      no ser que se trate de un estado final, en cuyo caso priorizará los casos de victoria
    """

    def get_name(self) -> str:
        return "random-esque"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        # let's use a global function
        return func_glob(0, state)


class Solution2(StudentHeuristic):
    def get_name(self) -> str:
        return "solution2"

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
                if state.player_max.label == state.board.get((x, y)):
                    move = (x, y)
                    if (
                        move == (1, 1)
                        or move == (1, 6)
                        or move == (6, 1)
                        or move == (6, 6)
                    ):
                        score = score - 3
                    elif (
                        move == (0, 1)
                        or move == (0, 6)
                        or move == (1, 0)
                        or move == (1, 7)
                        or move == (6, 0)
                        or move == (6, 7)
                        or move == (7, 1)
                        or move == (7, 6)
                    ):
                        score = score - 2
                    elif (
                        move == (1, 2)
                        or move == (1, 3)
                        or move == (1, 4)
                        or move == (1, 5)
                        or move == (2, 1)
                        or move == (2, 6)
                        or move == (3, 1)
                        or move == (3, 6)
                        or move == (4, 1)
                        or move == (4, 6)
                        or move == (5, 1)
                        or move == (5, 6)
                        or move == (6, 2)
                        or move == (6, 3)
                        or move == (6, 4)
                        or move == (6, 5)
                    ):
                        score = score - 1
                    elif (
                        move == (2, 3)
                        or move == (2, 4)
                        or move == (3, 2)
                        or move == (3, 5)
                        or move == (4, 2)
                        or move == (4, 5)
                        or move == (5, 3)
                        or move == (5, 4)
                    ):
                        score = score + 0
                    elif (
                        move == (2, 2)
                        or move == (2, 5)
                        or move == (5, 2)
                        or move == (5, 5)
                    ):
                        score = score + 1
                    elif (
                        move == (0, 2)
                        or move == (0, 3)
                        or move == (0, 4)
                        or move == (0, 5)
                        or move == (2, 0)
                        or move == (2, 7)
                        or move == (3, 0)
                        or move == (3, 7)
                        or move == (4, 0)
                        or move == (4, 7)
                        or move == (5, 0)
                        or move == (5, 7)
                        or move == (7, 2)
                        or move == (7, 3)
                        or move == (7, 4)
                        or move == (7, 5)
                    ):
                        score = score + 2
                    elif (
                        move == (0, 0)
                        or move == (0, 7)
                        or move == (7, 0)
                        or move == (7, 7)
                    ):
                        score = score + 3
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
            state_value += -5
        else:
            state_value += 5
        if state.end_of_game:
            scores = state.scores
            score_difference = scores[0] - scores[1]

            if state.is_player_max(state.player1):
                state_value = score_difference
            elif state.is_player_max(state.player2):
                state_value = -score_difference
            else:
                raise ValueError("Player MAX not defined")

        return state_value
