"""
gtp_connection_go3.py
Example for extending a GTP engine with extra commands
"""
from turtle import color

from numpy import moveaxis
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
        self.weights = self.load_weights()

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

        return "[" + str_build[1:]+"]"

    def load_weights(self):
        weights = {}
        with open('weights.txt') as f:
            lines = f.readlines()
            for line in lines:
                weights[int(line.split()[0])] = float(line.split()[1])
        return weights

    def base4_to_base10(self, num, base=4):
        base10 = 0
        for i, digit in enumerate(num):
            base10 += int(digit)*base**i
        return base10

    def get_pattern(self, board, point, color):
        neighbors = sorted(board._neighbors(point)+board._diag_neighbors(point))
        pattern = ''
        for nb in neighbors:
            # print(nb, format_point(point_to_coord(nb, self.board.size)), board.board[nb])
            pattern += str(board.board[nb])
        return pattern


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
            pattern_moves = {}
            weight_sum = 0
            for move in moves:
                # print(format_point(point_to_coord(move, self.board.size)))
                #play move
                self.board.play_move(move, color)

                pattern = self.get_pattern(self.board, move, color)
                address = self.base4_to_base10(pattern)
                point = format_point(point_to_coord(move, self.board.size)).lower()
                pattern_moves[point] = self.weights[address]
                weight_sum += self.weights[address]

                #undo move
                self.board.board[move] = 0
                self.board.current_player = color
            result = sorted(list(pattern_moves.keys()))
            result = '[' + ' '.join(result) + ' ' + ' '.join([str(round(pattern_moves[x]/weight_sum, 3)) for x in result]) + ']'
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