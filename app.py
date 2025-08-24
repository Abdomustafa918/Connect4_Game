from flask import Flask, render_template, request, jsonify
import numpy as np
import random

app = Flask(__name__)

ROWS = 6
COLS = 7
PLAYER = 1
AI = 2

def create_board():
    return np.zeros((ROWS, COLS), dtype=int)

def is_valid_location(board, col):
    return board[0][col] == 0

def get_next_open_row(board, col):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == 0:
            return r

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def check_winner(board, piece):
    
    for c in range(COLS-3):
        for r in range(ROWS):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    for c in range(COLS):
        for r in range(ROWS-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    for c in range(COLS-3):
        for r in range(ROWS-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    for c in range(COLS-3):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True
    return False

def minimax(board, depth, alpha, beta, maximizing):
    valid_locations = [c for c in range(COLS) if is_valid_location(board, c)]
    is_terminal = check_winner(board, PLAYER) or check_winner(board, AI) or len(valid_locations) == 0
    
    if depth == 0 or is_terminal:
        if check_winner(board, AI):
            return (None, 10000000)
        elif check_winner(board, PLAYER):
            return (None, -10000000)
        else:
            return (None, 0)
    
    if maximizing:
        value = -np.inf
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, AI)
            new_score = minimax(temp_board, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return best_col, value
    else:
        value = np.inf
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, PLAYER)
            new_score = minimax(temp_board, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                best_col = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return best_col, value

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def player_move():
    data = request.get_json()
    board = np.array(data['board'])
    col = data['column']
    
    if check_winner(board, PLAYER) or check_winner(board, AI):
        return jsonify({'board': board.tolist(), 'error': 'Game already over'})
    
    if is_valid_location(board, col):
        row = get_next_open_row(board, col)
        drop_piece(board, row, col, PLAYER)
        if check_winner(board, PLAYER):
            return jsonify({'board': board.tolist(), 'winner': 'Player'})
        
        ai_col, _ = minimax(board, 4, -np.inf, np.inf, True)
        if is_valid_location(board, ai_col):
            ai_row = get_next_open_row(board, ai_col)
            drop_piece(board, ai_row, ai_col, AI)
            if check_winner(board, AI):
                return jsonify({'board': board.tolist(), 'winner': 'AI'})
    
    return jsonify({'board': board.tolist()})

if __name__ == '__main__':
    app.run(debug=True)