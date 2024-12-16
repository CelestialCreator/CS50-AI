"""
Tic Tac Toe Player
"""

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
    # Count X's and O's on the board
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    
    # X plays first, so if equal numbers, it's X's turn
    return X if x_count <= o_count else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    
    # Check each cell
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))
                
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Validate action
    i, j = action
    if board[i][j] != EMPTY:
        raise ValueError("Invalid action")
        
    # Create deep copy of board
    import copy
    new_board = copy.deepcopy(board)
    
    # Make the move
    new_board[i][j] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check rows
    for row in board:
        if row.count(row[0]) == 3 and row[0] != EMPTY:
            return row[0]
    
    # Check columns
    for j in range(3):
        column = [board[i][j] for i in range(3)]
        if column.count(column[0]) == 3 and column[0] != EMPTY:
            return column[0]
    
    # Check diagonals
    diagonal1 = [board[i][i] for i in range(3)]
    if diagonal1.count(diagonal1[0]) == 3 and diagonal1[0] != EMPTY:
        return diagonal1[0]
        
    diagonal2 = [board[i][2-i] for i in range(3)]
    if diagonal2.count(diagonal2[0]) == 3 and diagonal2[0] != EMPTY:
        return diagonal2[0]
    
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # Game is over if someone won
    if winner(board) is not None:
        return True
    
    # Game is over if board is full
    return not any(EMPTY in row for row in board)


def utility(board):
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
        
    current_player = player(board)
    
    if current_player == X:
        best_value = float('-inf')
        best_move = None
        
        for action in actions(board):
            min_value = min_value_function(result(board, action))
            if min_value > best_value:
                best_value = min_value
                best_move = action
    else:
        best_value = float('inf')
        best_move = None
        
        for action in actions(board):
            max_value = max_value_function(result(board, action))
            if max_value < best_value:
                best_value = max_value
                best_move = action
                
    return best_move

def max_value_function(board):
    if terminal(board):
        return utility(board)
    v = float('-inf')
    for action in actions(board):
        v = max(v, min_value_function(result(board, action)))
    return v

def min_value_function(board):
    if terminal(board):
        return utility(board)
    v = float('inf')
    for action in actions(board):
        v = min(v, max_value_function(result(board, action)))
    return v
