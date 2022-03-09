"""
gtp_connection_go3.py
Example for extending a GTP engine with extra commands
"""
from gtp_connection import GtpConnection, point_to_coord, format_point
from board_util import GoBoardUtil, BLACK, WHITE, EMPTY, BORDER, PASS
from pattern_util import PatternUtil
from board_util import GoBoardUtil


def sorted_point_string(points, boardsize):
    result = []
    for point in points:
        x, y = point_to_coord(point, boardsize)
        result.append(format_point((x, y)))
    return " ".join(sorted(result))


class GtpConnectionGo3(GtpConnection):
    def __init__(self, go_engine, board, debug_mode=False):
        """
        GTP connection of Go3
        """
        GtpConnection.__init__(self, go_engine, board, debug_mode)

        self.commands["policy"] = self.policy_cmd
        self.commands["selection"] = self.selection_cmd
        self.commands["policy_moves"] = self.policy_moves_cmd
        self.commands["genmove"] = self.genmove_cmd
        self.argmap["policy"] = (1, "Usage: policy {random, pattern}")
        self.argmap["selection"] = (1, "Usage: selection {rr, ucb}")

    def get_parameter_cmd(self, args):
        pars = self.go_engine.get_pars()
        self.respond(pars)

    def selection_cmd(self, args):
        if(args[0] != "rr" and args[0] != "ucb"):
            self.respond("Usage: selection {rr, ucb}");
            return;
        self.go_engine.selection = args[0]
        self.respond()
    def policy_cmd(self, args):
        if(args[0] != "random" and args[0] != "pattern"):
            self.respond("Usage: policy {random, pattern}");
            return;
        self.go_engine.policy = args[0]
        self.respond()
    
    def policy_moves_cmd(self, args):
        """
        Return list of policy moves for the current_player of the board
        """
        cp = self.board.current_player
        legalMoves = GoBoardUtil.generate_legal_moves(self.board, cp)
        if self.go_engine.policy == 'random':
            remainingMoves = len(legalMoves)
            if remainingMoves == 0:
                self.respond()
            else:
                pass #Calc and respond()
        else:
            pass
            #TODO


    def genmove_cmd(self, args):
        color = WHITE if args[0] == 'w' else BLACK
        bestMove = self.go_engine.getMoves(self.board, color)
        if bestMove == None:
            self.respond()
        else:
            self.respond(self.strPoint(bestMove).lower())

    def genmove_cmd(self, args):
        """ generate a move for color args[0] in {'b','w'} """
        if(args[0] == 'w'):
            color = WHITE
        else:
            color = BLACK
        move = self.go_engine.get_move(self.board, color)
        if move is None:
            self.respond('unknown')
            return
        move_coord = point_to_coord(move, self.board.size)
        move_as_string = format_point(move_coord)
        self.respond(move_as_string)
