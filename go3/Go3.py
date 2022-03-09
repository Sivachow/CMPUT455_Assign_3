#!/usr/local/bin/python3
# /usr/bin/python3
# Set the path to your python3 above

from gtp_connection_go3 import GtpConnectionGo3
from board_score import winner
from board_util import GoBoardUtil, PASS
from pattern_util import PatternUtil
from board import GoBoard
from simulation_util import writeMoves, select_best_move
from ucb import runUcb
import numpy as np
import argparse
import sys

class Go3:
    def __init__(self, sim, move_select, sim_rule, move_filter, size=7, limit=100):
        """
        Go player that selects moves by simulation.
        """
        self.name = "Go3"
        self.version = 1.0
        self.komi = 6.5
        self.sim = sim
        self.limit = limit
        self.use_ucb = False if move_select == "simple" else True
        self.random_simulation = True if sim_rule == "random" else False
        self.use_pattern = not self.random_simulation
        self.check_selfatari = move_filter

    def simulate(self, board, move, toplay):
        """
        Run a simulated game for a given move.
        """
        cboard = board.copy()
        cboard.play_move(move, toplay)
        opp = GoBoardUtil.opponent(toplay)
        return self.playGame(cboard, opp)

    def simulateMove(self, board, move, toplay):
        """
        Run simulations for a given move.
        """
        wins = 0
        for _ in range(self.sim):
            result = self.simulate(board, move, toplay)
            if result == toplay:
                wins += 1
        return wins

    def get_move(self, board, color):
        """
        Run one-ply MC simulations to get a move to play.
        """
        cboard = board.copy()
        emptyPoints = board.get_empty_points()
        moves = []
        for p in emptyPoints:
            if board.is_legal(p, color):
                moves.append(p)
        if not moves:
            return None
        moves.append(None)
        if self.use_ucb:
            C = 0.4  # sqrt(2) is safe, this is more aggressive
            best = runUcb(self, cboard, C, moves, color)
            return best
        else:
            moveWins = []
            for move in moves:
                wins = self.simulateMove(cboard, move, color)
                moveWins.append(wins)
            writeMoves(cboard, moves, moveWins, self.sim)
            return select_best_move(board, moves, moveWins)

    def playGame(self, board, color):
        """
        Run a simulation game.
        """
        nuPasses = 0
        for _ in range(self.limit):
            color = board.current_player
            if self.random_simulation:
                move = GoBoardUtil.generate_random_move(board, color, True)
            else:
                move = PatternUtil.generate_move_with_filter(
                    board, self.use_pattern, check_selfatari
                )
            board.play_move(move, color)
            if move == PASS:
                nuPasses += 1
            else:
                nuPasses = 0
            if nuPasses >= 2:
                break
        return winner(board, self.komi)

def run(sim, move_select, sim_rule, move_filter):
    """
    Start the gtp connection and wait for commands.
    """
    board = GoBoard(7)
    con = GtpConnectionGo3(Go3(sim, move_select, sim_rule, move_filter), board)
    con.start_connection()


def parse_args():
    """
    Parse the arguments of the program.
    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--sim",
        type=int,
        default=10,
        help="number of simulations per move, so total playouts=sim*legal_moves",
    )
    parser.add_argument(
        "--moveselect",
        type=str,
        default="simple",
        help="type of move selection: simple or ucb",
    )
    parser.add_argument(
        "--simrule",
        type=str,
        default="random",
        help="type of simulation policy: random or rulebased",
    )
    parser.add_argument(
        "--movefilter",
        action="store_true",
        default=False,
        help="whether use move filter or not",
    )

    args = parser.parse_args()
    sim = args.sim
    move_select = args.moveselect
    sim_rule = args.simrule
    move_filter = args.movefilter

    if move_select != "simple" and move_select != "ucb":
        print("moveselect must be simple or ucb")
        sys.exit(0)
    if sim_rule != "random" and sim_rule != "rulebased":
        print("simrule must be random or rulebased")
        sys.exit(0)

    return sim, move_select, sim_rule, move_filter


if __name__ == "__main__":
    sim, move_select, sim_rule, move_filter = parse_args()
    run(sim, move_select, sim_rule, move_filter)
