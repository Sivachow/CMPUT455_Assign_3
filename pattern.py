from gtp_connection import point_to_coord, format_point


def load_weights():
        weights = {}
        with open('weights.txt') as f:
            lines = f.readlines()
            for line in lines:
                weights[int(line.split()[0])] = float(line.split()[1])
        return weights

def get_pattern(board, point, color):
    neighbors = sorted(board._neighbors(point)+board._diag_neighbors(point))
    pattern = ''
    for nb in neighbors:
        pattern += str(board.board[nb])
    return pattern

def get_pattern_probs(board, moves, color, weights):
    
    pattern_moves = {}
    weight_sum = 0
    for move in moves:
        #play move
        board.play_move(move, color)

        pattern = get_pattern(board, move, color)
        address = int(pattern,4)
        pattern_moves[move] = weights[address]
        weight_sum += weights[address]

        #undo move
        board.board[move] = 0
        board.current_player = color

    return pattern_moves, weight_sum

