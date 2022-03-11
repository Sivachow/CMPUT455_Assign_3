"""
gtp_connection_go3.py
Example for extending a GTP engine with extra commands
"""
from turtle import color

from numpy import moveaxis
from gtp_connection import GtpConnection, point_to_coord, format_point
from board_util import GoBoardUtil, BLACK, WHITE, EMPTY, BORDER, PASS
from pattern import *
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
            self.respond("Usage: selection {rr, ucb}")
            return
        self.go_engine.selection = args[0]
        self.respond()
    def policy_cmd(self, args):
        if(args[0] != "random" and args[0] != "pattern"):
            self.respond("Usage: policy {random, pattern}")
            return
        self.go_engine.policy = args[0]
        self.respond()
    
    def respondProb(self,moves):
        str_build = ""
        num = round( 3/( 3*len(moves)), 3)
        lst = []
        for move in moves:
            move_coord = point_to_coord(move, self.board.size)
            move_as_string = format_point(move_coord)
            lst.append(move_as_string.lower())
        lst.sort()
        for move in lst:
            str_build = str_build + " " + move

        for move in moves:
            str_build = str_build + " " + str(num)

        return str_build[1:]

    def policy_moves_cmd(self, args):
        """
        Return list of policy moves for the current_player of the board
        """
        color = self.board.current_player
        moves = GoBoardUtil.generate_legal_moves(self.board, color)
        if self.go_engine.policy == 'random':
            if len(moves) == 0:
                self.respond()
            else:
                self.respond(self.respondProb(moves))
        elif self.go_engine.policy == 'pattern':
            pattern_moves, weight_sum = get_pattern_probs(self.board, moves, color) #Returns a dictionary of move:weight items. Move is an integer

            moves = list(pattern_moves.keys())
            points = []
            for move in moves:
                point = format_point(point_to_coord(move, self.board.size)).lower()
                points.append(point)

            weights = list(pattern_moves.values())
            probs = []

            for x in weights:
                probs.append(round(x/weight_sum, 3)) #Converting weights to probabilities

            new_dic = dict(zip(points, probs))
            result = sorted(list(new_dic.keys()))
            result = ' '.join(result) + ' ' + ' '.join([str(new_dic[x]) for x in result])
            self.respond(result)

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
        self.board.play_move(move, color)
        move_coord = point_to_coord(move, self.board.size)
        move_as_string = format_point(move_coord).lower()
        self.respond(move_as_string)

    # def genmove_cmd(self, args):
    #     """ generate a move for color args[0] in {'b','w'} """
    #     # change this method to use your solver
    #     board_color = args[0].lower()
    #     color = color_to_int(board_color)
    #     move = self.go_engine.get_move(self.board, color)
    #     if move is None:
    #         self.respond('unknown')
    #         return
    #     move_coord = point_to_coord(move, self.board.size)
    #     move_as_string = format_point(move_coord)
    #     if self.board.is_legal(move, color):
    #         self.board.play_move(move, color)
    #         self.respond(move_as_string)
    #     else:
    #         self.respond("Illegal move: {}".format(move_as_string))