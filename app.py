from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# ================= GAME LOGIC CLASSES ==================

class Cell:
    def __init__(self, value='.'):
        self.value = value

    def __str__(self):
        return self.value

    def set_cell(self, value):
        if value in ['X', 'O']:
            if self.value == '.':
                self.value = value
                return True
            else:
                return False
        else:
            raise ValueError("Cell value must be 'X' or 'O'.")

class Board:
    def __init__(self, size=3):
        self.size = size
        self.grid = [[Cell() for _ in range(size)] for _ in range(size)]

    def set_cell(self, row, col, value):
        return self.grid[row][col].set_cell(value)

    def get_cell_value(self, row, col):
        return self.grid[row][col].value

    def check_draw(self):
        return all(self.grid[i][j].value != '.' for i in range(self.size) for j in range(self.size))

    def check_win(self, value):
        for i in range(self.size):
            if all(self.grid[i][j].value == value for j in range(self.size)):
                return [(i, j) for j in range(self.size)]
            if all(self.grid[j][i].value == value for j in range(self.size)):
                return [(j, i) for j in range(self.size)]
        if all(self.grid[i][i].value == value for i in range(self.size)):
            return [(i, i) for i in range(self.size)]
        if all(self.grid[i][self.size - 1 - i].value == value for i in range(self.size)):
            return [(i, self.size - 1 - i) for i in range(self.size)]
        return []

    def get_available_moves(self):
        return [(i, j) for i in range(self.size) for j in range(self.size) if self.grid[i][j].value == '.']

# ================= AI ==================

def get_ai_move_easy(board):
    return random.choice(board.get_available_moves())

def get_ai_move_medium(board, ai_symbol='O', player_symbol='X'):
    for row, col in board.get_available_moves():
        board.grid[row][col].value = ai_symbol
        if board.check_win(ai_symbol):
            board.grid[row][col].value = '.'
            return (row, col)
        board.grid[row][col].value = '.'

    for row, col in board.get_available_moves():
        board.grid[row][col].value = player_symbol
        if board.check_win(player_symbol):
            board.grid[row][col].value = '.'
            return (row, col)
        board.grid[row][col].value = '.'

    return get_ai_move_easy(board)

def minimax(board, depth, is_maximizing, ai_symbol, player_symbol):
    if board.check_win(ai_symbol):
        return 10 - depth
    elif board.check_win(player_symbol):
        return depth - 10
    elif board.check_draw():
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for row, col in board.get_available_moves():
            board.grid[row][col].value = ai_symbol
            score = minimax(board, depth + 1, False, ai_symbol, player_symbol)
            board.grid[row][col].value = '.'
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for row, col in board.get_available_moves():
            board.grid[row][col].value = player_symbol
            score = minimax(board, depth + 1, True, ai_symbol, player_symbol)
            board.grid[row][col].value = '.'
            best_score = min(score, best_score)
        return best_score

def get_ai_move_hard(board, ai_symbol='O', player_symbol='X'):
    best_score = -float('inf')
    best_move = None
    for row, col in board.get_available_moves():
        board.grid[row][col].value = ai_symbol
        score = minimax(board, 0, False, ai_symbol, player_symbol)
        board.grid[row][col].value = '.'
        if score > best_score:
            best_score = score
            best_move = (row, col)
    return best_move

# ============ GAME STATE ============
board = Board()
current_turn = 'X'
mode = 'two'
ai_difficulty = 'easy'

# ============ ROUTES ============

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new_game', methods=['POST'])
def new_game():
    global board, current_turn, mode, ai_difficulty
    data = request.json
    board = Board()
    current_turn = 'X'
    mode = data.get('mode', 'two')
    ai_difficulty = data.get('difficulty', 'easy')
    return jsonify({'status': 'started', 'mode': mode, 'difficulty': ai_difficulty})

@app.route('/move', methods=['POST'])
def move():
    global current_turn, board

    data = request.json
    row = data['row']
    col = data['col']

    if not board.set_cell(row, col, current_turn):
        return jsonify({'status': 'occupied'})

    win_cells = board.check_win(current_turn)
    is_draw = board.check_draw()

    result = {
        'status': 'ok',
        'board': [[board.get_cell_value(i, j) for j in range(3)] for i in range(3)],
        'current': current_turn,
        'win': win_cells,
        'draw': is_draw
    }

    if win_cells or is_draw:
        return result

    current_turn = 'O' if current_turn == 'X' else 'X'

    # AI Move if applicable
    if mode == 'single' and current_turn == 'O':
        if ai_difficulty == 'easy':
            ai_move = get_ai_move_easy(board)
        elif ai_difficulty == 'medium':
            ai_move = get_ai_move_medium(board)
        else:
            ai_move = get_ai_move_hard(board)

        board.set_cell(*ai_move, 'O')
        win_cells = board.check_win('O')
        is_draw = board.check_draw()

        result['ai_move'] = {'row': ai_move[0], 'col': ai_move[1]}
        result['win'] = win_cells
        result['draw'] = is_draw
        result['board'] = [[board.get_cell_value(i, j) for j in range(3)] for i in range(3)]
        current_turn = 'X'

    return result

if __name__ == '__main__':
    app.run(debug=True)