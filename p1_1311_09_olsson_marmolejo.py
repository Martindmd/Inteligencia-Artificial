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
            return Solution2.evaluation_function(self,state) + Solution3.evaluation_function(self, state)
        elif total_score <= 30:
            return Solution2.evaluation_function(self,state) + 0.5 * Solution3.evaluation_function(self, state)
        else:
            return Solution2.evaluation_function(self,state)


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
                    move = (x + 1, y + 1)
                    if (
                        move == (2, 2)
                        or move == (2, 7)
                        or move == (7, 2)
                        or move == (7, 7)
                    ):
                        score = score - 40
                    elif (
                        move == (1, 2)
                        or move == (1, 7)
                        or move == (2, 1)
                        or move == (2, 8)
                        or move == (7, 1)
                        or move == (7, 8)
                        or move == (8, 2)
                        or move == (8, 7)
                    ):
                        score = score - 20
                    elif (
                        move == (2, 3)
                        or move == (2, 4)
                        or move == (2, 5)
                        or move == (2, 6)
                        or move == (3, 2)
                        or move == (3, 7)
                        or move == (4, 2)
                        or move == (4, 7)
                        or move == (5, 2)
                        or move == (5, 7)
                        or move == (6, 2)
                        or move == (6, 7)
                        or move == (7, 3)
                        or move == (7, 4)
                        or move == (7, 5)
                        or move == (7, 6)
                    ):
                        score = score - 5
                    elif (
                        move == (3, 4)
                        or move == (3, 5)
                        or move == (4, 3)
                        or move == (4, 6)
                        or move == (5, 3)
                        or move == (5, 6)
                        or move == (6, 4)
                        or move == (6, 5)
                    ):
                        score = score + 3
                    elif (
                        move == (3, 3)
                        or move == (3, 6)
                        or move == (6, 3)
                        or move == (6, 6)
                    ):
                        score = score + 15
                    elif (
                        move == (1, 4)
                        or move == (1, 5)
                        or move == (4, 1)
                        or move == (4, 8)
                        or move == (5, 1)
                        or move == (5, 8)
                        or move == (8, 4)
                        or move == (8, 5)
                    ):
                        score = score + 5
                    elif (move == (1,3)
                        or move == (1,6)
                        or move == (3,8)
                        or move == (3,1)
                        or move == (6,8)
                        or move == (6,1)
                        or move == (8,6)
                        or move == (8,3)
                    ):
                        score = score + 20
                    elif (
                        move == (1, 1)
                        or move == (1, 8)
                        or move == (8, 1)
                        or move == (8, 8)
                    ):
                        score = score + 120
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

        return state_value
