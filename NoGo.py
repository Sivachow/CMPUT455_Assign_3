#!/usr/local/bin/python3
# /usr/bin/python3
# Set the path to your python3 above

import random
from gtp_connection_go3 import GtpConnectionGo3
from board_util import GoBoardUtil
from board import GoBoard
from board_util import GoBoardUtil, BLACK, WHITE, EMPTY, BORDER, PASS
from simulation_util import writeMoves, select_best_move
from ucb import runUcb
import argparse
import sys
from pattern import *


class NoGo0:
    def __init__(self, move_select, sim_rule, size=7, limit=100):
        """
        NoGo player that selects moves randomly from the set of legal moves.

        Parameters
        ----------
        name : str
            name of the player (used by the GTP interface).
        version : float
            version number (used by the GTP interface).
        """
        self.name = "NoGo"
        self.version = 1.0
        self.sim = 10
        self.limit = limit
        self.policy = "random" # random or pattern
        self.selection = "rr" # rr or ucb
        #self.use_pattern = not self.random_simulation


    def get_move(self, board, color):
        """
        Run one-ply MC simulations to get a move to play.
        """
        cboard = board.copy()
        emptyPoints = board.get_empty_points()
        moves = []
        for p in emptyPoints:
            if board.is_legal(p, color): #Can make this faster by just getting legal moves? GoBoardUtil.generate_legal_moves(self.board, color)
                moves.append(p)
        if not moves:
            return None
        moves.append(None)

        if self.selection == "ucb":
            C = 0.4  # sqrt(2) is safe, this is more aggressive
            best = runUcb(self, cboard, C, moves, color)
            return best
            
        else: #use round robin move selection policy
            moveWins = []
            for move in moves: #Simulate all the legal moves self.sim times
                wins = self.simulateMove(cboard, move, color)
                moveWins.append(round(wins/(len(moves)*self.sim),3))

            return select_best_move(board, moves, moveWins)

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

    def simulate(self, board, move, toplay):
        """
        Run a simulated game for a given move.
        """
        cboard = board.copy()
        cboard.play_move(move, toplay)
        opp = GoBoardUtil.opponent(toplay)
        return self.playGame(cboard, opp)

    def playGame(self, board, color):
        """
        Run a simulation game.
        """
        if self.policy == "random":
            while(True): 
                color = board.current_player
                move = GoBoardUtil.generate_random_move(board, color, True)
                if(move == None):
                    return BLACK + WHITE - color
                board.play_move(move, color)
        elif self.policy == "pattern":
             while(True): 
                color = board.current_player
                legal_moves = GoBoardUtil.generate_legal_moves(board, color)
                if not legal_moves:
                    return BLACK + WHITE - color
                
                pattern_moves = get_pattern_probs(board, legal_moves, color)[0] #Get a dictionary of all the legal moves with their weights
                moves = list(pattern_moves.keys())
                weights = list(pattern_moves.values())
                
                move = random.choices(moves, weights = weights, k=1)[0] #Generate a random move from moves based on weights
                #print(move)
                board.play_move(move, color)
            
       
    

def run(sim, move_select, sim_rule):
    """
    start the gtp connection and wait for commands.
    """
    board = GoBoard(7)
    con = GtpConnectionGo3(NoGo0(sim, move_select, sim_rule), board)
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
    #parser.add_argument(
    #    "--movefilter",
    #    action="store_true",
    #    default=False,
    #    help="whether use move filter or not",
    #)

    args = parser.parse_args()
    sim = args.sim
    move_select = args.moveselect
    sim_rule = args.simrule
    #move_filter = args.movefilter

    if move_select != "simple" and move_select != "ucb":
        print("moveselect must be simple or ucb")
        sys.exit(0)
    if sim_rule != "random" and sim_rule != "rulebased":
        print("simrule must be random or rulebased")
        sys.exit(0)

    return sim, move_select, sim_rule


if __name__ == "__main__":
    sim, move_select, sim_rule = parse_args()
    run(sim, move_select, sim_rule)