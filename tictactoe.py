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
    total_actions = sum(row.count(X) + row.count(O) for row in board)
    return X if total_actions % 2 == 0 else O

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = [(i,j) for i in range(3) for j in range(3) if board[i][j] is EMPTY]     
    return set(possible_actions)


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
    if not remaining_actions:
        return True
    
    return False


def utility(board) -> int:
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    game_winner = winner(board)
    if game_winner == X:
        return 1
    elif game_winner == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    
    available_actions = actions(board)
    best_action = None
    alpha = -math.inf
    beta = math.inf

    if player(board) == X:
        best_score = -math.inf
        for action in available_actions:
            score = max_value(result(board, action), alpha, beta)
            if score > best_score:
                best_score = score
                best_action = action
    else:
        best_score = math.inf
        for action in available_actions:
            score = min_value(result(board, action), alpha, beta)
            if score < best_score:
                best_score = score
                best_action = action

    return best_action

def max_value(board, alpha, beta):
    if terminal(board):
        return utility(board)

    score = -math.inf
    available_actions = actions(board)
    if not available_actions:
        return utility(board)

    for action in available_actions:
        score = max(score, min_value(result(board, action), alpha, beta))
        alpha = max(alpha, score)
        if beta <= alpha:
            break
    return score

def min_value(board, alpha, beta):
    if terminal(board):
        return utility(board)

    score = math.inf
    available_actions = actions(board)
    if not available_actions:
        return utility(board)

    for action in available_actions:
        score = min(score, max_value(result(board, action), alpha, beta))
        beta = min(beta, score)
        if beta <= alpha:
            break
    return score
