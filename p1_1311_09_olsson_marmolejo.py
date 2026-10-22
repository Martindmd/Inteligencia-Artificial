from collections.abc import Sequence

import numpy as np

from game import (
    TwoPlayerGameState,
)
from heuristic import (
    simple_evaluation_function,
)
from reversi import Reversi, get_valid_moves, enemy_captured_by_move
from tournament import (
    StudentHeuristic,
)

VICTORY_SCORE = 99999


def func_glob(n: int, state: TwoPlayerGameState) -> float:
    return n + simple_evaluation_function(state)


def mobility(self, state: TwoPlayerGameState) -> float:
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
            return (Solution2.evaluation_function(self, state) + 0.5 * Solution3.evaluation_function(self,
                                                                                                     state) +
                    mobility(self, state))
        elif total_score <= 30:
            return (Solution2.evaluation_function(self, state) + 0.25 * Solution3.evaluation_function(self,
                                                                                                      state) +
                    mobility(self, state))
        else:
            return Solution2.evaluation_function(self, state) + mobility(self, state)


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

        enemy_label = (
            state.player2.label
            if state.player_max.label == state.player1.label
            else state.player1.label
        )

        score = 0
        for x in range(7):
            for y in range(7):
                x = x + 1
                y = y + 1
                BOARD = [120, -20, 20, 5, 5, 20, -20, 120,
                         -20, -40, -5, -5, -5, -5, -40, -20,
                         20, -5, 15, 3, 3, 15, -5, 20,
                         5, -5, 3, 3, 3, 3, -5, 5,
                         5, -5, 3, 3, 3, 3, -5, 5,
                         20, -5, 15, 3, 3, 15, -5, 20
                         - 20, -40, -5, -5, -5, -5, -40, -20,
                         120, -20, 20, 5, 5, 20, -20, 120, ]
                if (x, y) in [(1, 2), (2, 1)] and state.board.get((1, 1)) == state.player_max.label:
                    score = score + 20
                elif (x, y) in [(1, 7), (2, 8)] and state.board.get((8, 8)) == state.player_max.label:
                    score = score + 20
                elif (x, y) in [(7, 1), (8, 2)] and state.board.get((1, 8)) == state.player_max.label:
                    score = score + 20
                elif (x, y) in [(7, 8), (8, 7)] and state.board.get((8, 1)) == state.player_max.label:
                    score = score + 20
                elif state.player_max.label == state.board.get(x, y):
                    score = score + BOARD[x % 8 + y - 1]
                elif enemy_label == state.board.get(x, y):
                    score = score - BOARD[(x - 1) % 8 + y - 1]
        return score


class Solution3(StudentHeuristic):
    """prioriza aquellos estados en los que max_player
    tiene la menor cantidad de piezas posibles"""

    def get_name(self) -> str:
        return "maximalist"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        mob = mobility(self, state)
        """Potential mobility can be estimated by simply counting all the opponent's pieces that are adjacent to an empty field"""
        potential_mobility = 0
        enemy_label = (
            state.player2.label
            if state.player_max.label == state.player1.label
            else state.player1.label
        )
        for x, y in get_valid_moves(state.board, 8, 8, state.player_max.label, enemy_label, "O", False):
            # NO
            if state.board.get((x - 1, y - 1)) == enemy_label:
                potential_mobility = potential_mobility + 1
            # N
            elif state.board.get((x, y - 1)) == enemy_label:
                potential_mobility = potential_mobility + 1
            # NE
            elif state.board.get((x + 1, y - 1)) == enemy_label:
                potential_mobility = potential_mobility + 1
            # O
            elif state.board.get((x - 1, y)) == enemy_label:
                potential_mobility = potential_mobility + 1
            # E
            elif state.board.get((x + 1, y)) == enemy_label:
                potential_mobility = potential_mobility + 1
            # SO
            elif state.board.get((x - 1, y + 1)) == enemy_label:
                potential_mobility = potential_mobility + 1
            # S
            elif state.board.get((x, y + 1)) == enemy_label:
                potential_mobility = potential_mobility + 1
            # SE
            elif state.board.get((x + 1, y + 1)) == enemy_label:
                potential_mobility = potential_mobility + 1

        return mob + 0.25 * potential_mobility
