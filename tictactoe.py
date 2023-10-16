"""
Tic Tac Toe Player
"""

import copy
import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    total_moves = sum(row.count(X) + row.count(O) for row in board)
    return X if total_moves % 2 == 0 else O

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions_list = [(i,j) for i in range(3) for j in range(3) if board[i][j] is EMPTY]     
    return set(actions_list)


def result(board, action) -> list:
    """
    Returns the board that results from making move (i, j) on the board.
    """
    current_player = player(board)
    i, j = action
    valid_actions = actions(board)

    if action not in valid_actions:
        raise Exception("Invalid action")

    result_board = copy.deepcopy(board)
    result_board[i][j] = current_player
    return result_board



def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for row in board:
        if row.count(X) == 3:
            return X
        elif row.count(O) == 3:
            return O

    for col in range(3):
        if all(board[row][col] == X for row in range(3)):
            return X
        elif all(board[row][col] == O for row in range(3)):
            return O

    if all(board[i][i] == X for i in range(3)) or all(board[i][2 - i] == X for i in range(3)):
        return X
    elif all(board[i][i] == O for i in range(3)) or all(board[i][2 - i] == O for i in range(3)):
        return O

    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board):
        return True
    
    remaining_actions = actions(board)
    if not remaining_actions or len(remaining_actions) == 0:
        return True
    
    return False


def utility(board) -> int:
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    
    moves = actions(board)
    best_move = None
    alpha = -math.inf
    beta = math.inf

    if player(board) == X:
        best_v = -math.inf
        for move in moves:
            v = max_value(result(board, move), alpha, beta)
            if v > best_v:
                best_v = v
                best_move = move
    else:
        best_v = math.inf
        for move in moves:
            v = min_value(result(board, move), alpha, beta)
            if v < best_v:
                best_v = v
                best_move = move

    return best_move

def max_value(board, alpha, beta):
    if terminal(board):
        return utility(board)

    v = -math.inf
    moves = actions(board)
    if  len(moves) == 0:
        return utility(board)

    for move in moves:
        v = max(v, min_value(result(board, move), alpha, beta))
        alpha = max(alpha, v)
        if beta <= alpha:
            break
    return v

def min_value(board, alpha, beta):
    if terminal(board):
        return utility(board)

    v = math.inf
    moves = actions(board)
    if len(moves) == 0:
        return utility(board)

    for move in moves:
        v = min(v, max_value(result(board, move), alpha, beta))
        beta = min(beta, v)
        if beta <= alpha:
            break
    return v
