#!/usr/local/bin/python3
# /usr/bin/python3
# Set the path to your python3 above

from gtp_connection_go3 import GtpConnectionNoGo3
from board_util import GoBoardUtil
from board import GoBoard
from board_util import GoBoardUtil, BLACK, WHITE, EMPTY, BORDER


class NoGo0:
    def __init__(self):
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
        self.policy = "random" #or "pattern"
        self.selection = "rr" #or "ucb"

    def get_move(self, board, color):
        return GoBoardUtil.generate_random_move(board, color, 
                                                use_eye_filter=False)

def getBestMove(self, gameState, color):
    state = gameState.copy()
    legal = self.generateLegalMoves(gameState, color)
    probability = {}
    if(len(legal) == 0):
        return 
    wins = 0
    if(self.selection == "rr"):
        for move in legal:
            for i in range(10):
                if(self.policy == "random"):
                    winner = self.randomSimulate(gameState, move, color)
                else:
                    pass #TODO
                if(winner == color ):
                    wins+=1;
            probability[move] = round(wins/(len(legal)*10),3)
        return max(probability, key=probability.get)

    #...UCB TODO

def randomSimulate(self, gameState, move, color):
    state = gameState.copy()
    state.play_move(move, color)
    while(True):
        move = self.randomMove(state, state.current_player) #TODO
        if move == None:
            return BLACK + WHITE - state.current_player
        state.play_move(move, state.current_player)
def generateLegalMoves(self, gameState, color):
    empty = gameState.get_empty_points()
    moves = []
    for pt in empty:
        if gameState.is_legal(pt, color):
            moves.append(pt)
    return moves

def run():
    """
    start the gtp connection and wait for commands.
    """
    board = GoBoard(7)
    con = GtpConnectionNoGo3(NoGo0(), board)
    con.start_connection()


if __name__ == "__main__":
    run()
