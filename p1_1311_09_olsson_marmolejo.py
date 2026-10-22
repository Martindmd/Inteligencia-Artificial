from collections.abc import Sequence

import numpy as np

from game import (
    TwoPlayerGameState,
)
from reversi import get_valid_moves
from tournament import (
    StudentHeuristic,
)


def mobility(state: TwoPlayerGameState) -> float:
    """
    It evaluates the number of possible moves that can be made by the current player aka their mobility
    """

    enemy_label = (
        state.player2.label
        if state.player_max.label == state.player1.label
        else state.player1.label
    )

    return len(get_valid_moves(state.board, 8, 8, state.player_max.label, enemy_label, "O", False))


class Solution1(StudentHeuristic):
    """
    La función heurística "morning-victory" combina la funcionalidad de las otras dos estrategias heurísticas:
    para maximalist, va perdiendo importancia según avanza el juego, ya que la estrategia es más efectiva en los early
    stages
    """

    def get_name(self) -> str:
        return "morning-victory"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        # Combinación de las otras dos heurísticas en función a la fase del juego actual
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

        total_score = state.scores[0] + state.scores[1]

        if total_score <= 15:
            return (Solution2.evaluation_function(self, state) + 0.5 * Solution3.evaluation_function(self,
                                                                                                     state) + mobility(
                state))
        elif total_score <= 30:
            return (Solution2.evaluation_function(self, state) + 0.25 * Solution3.evaluation_function(self,
                                                                                                      state) + mobility(
                state))
        else:
            return Solution2.evaluation_function(self, state) + mobility(state)


class Solution2(StudentHeuristic):
    """
    Evalúa las posiciones ocupadas por ambos jugadores y priorizando aquellas donde el jugador principal posee
    casillas más valiosas y su enemigo las más desfavorables
    """

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
                """ Move = (x,y) """
                x = x + 1
                y = y + 1
                """ Valor estratégico de cada casilla """
                BOARD = [120, -20, 20, 5, 5, 20, -20, 120,
                         -20, -40, -5, -5, -5, -5, -40, -20,
                         20, -5, 15, 3, 3, 15, -5, 20,
                         5, -5, 3, 3, 3, 3, -5, 5,
                         5, -5, 3, 3, 3, 3, -5, 5,
                         20, -5, 15, 3, 3, 15, -5, 20
                         - 20, -40, -5, -5, -5, -5, -40, -20,
                         120, -20, 20, 5, 5, 20, -20, 120, ]
                """ Si el jugador posee una esquina, las casillas anexas a ella son ventajosas """
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
    """ Prioriza estados donde el jugador posea el mayor número de movimientos posibles y fichas contrarias anexas a
    dichos movimientos """

    def get_name(self) -> str:
        return "maximalist"

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

        mob = mobility(state)
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
