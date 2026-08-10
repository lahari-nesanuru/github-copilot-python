from flask import Flask, render_template, jsonify, request
import sudoku_logic

app = Flask(__name__)

# Keep a simple in-memory store for current puzzle and solution
CURRENT = {
    'puzzle': None,
    'solution': None,
    'elapsed_seconds': None,
    'hints_used': 0
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new')
def new_game():
    difficulty = request.args.get('difficulty')
    clues = request.args.get('clues')

    try:
        parsed_clues = int(clues) if clues is not None else None
        if parsed_clues is None:
            if difficulty is None:
                puzzle, solution = sudoku_logic.generate_puzzle(clues=35)
            else:
                puzzle, solution = sudoku_logic.generate_puzzle(difficulty=difficulty)
        else:
            puzzle, solution = sudoku_logic.generate_puzzle(clues=parsed_clues, difficulty=difficulty)
    except (TypeError, ValueError) as exc:
        return jsonify({'error': str(exc)}), 400

    CURRENT['puzzle'] = puzzle
    CURRENT['solution'] = solution
    CURRENT['elapsed_seconds'] = None
    CURRENT['hints_used'] = 0
    return jsonify({'puzzle': puzzle})

@app.route('/hint', methods=['POST'])
def give_hint():
    puzzle = CURRENT.get('puzzle')
    solution = CURRENT.get('solution')
    if puzzle is None or solution is None:
        return jsonify({'error': 'No game in progress'}), 400

    for row in range(sudoku_logic.SIZE):
        for col in range(sudoku_logic.SIZE):
            if puzzle[row][col] == sudoku_logic.EMPTY:
                puzzle[row][col] = solution[row][col]
                CURRENT['hints_used'] += 1
                return jsonify({'row': row, 'col': col, 'value': solution[row][col], 'hints_used': CURRENT['hints_used']})

    return jsonify({'message': 'No hint available', 'hints_used': CURRENT['hints_used']})

@app.route('/check', methods=['POST'])
def check_solution():
    data = request.get_json(silent=True) or {}
    board = data.get('board')
    solution = CURRENT.get('solution')
    if solution is None:
        return jsonify({'error': 'No game in progress'}), 400
    incorrect = []
    for i in range(sudoku_logic.SIZE):
        for j in range(sudoku_logic.SIZE):
            if board[i][j] != solution[i][j]:
                incorrect.append([i, j])

    if not incorrect:
        elapsed_seconds = data.get('elapsed_seconds')
        if elapsed_seconds is None:
            elapsed_seconds = CURRENT.get('elapsed_seconds')
        if elapsed_seconds is None:
            elapsed_seconds = 0
        CURRENT['elapsed_seconds'] = elapsed_seconds
        return jsonify({'solved': True, 'incorrect': [], 'elapsed_seconds': elapsed_seconds})

    return jsonify({'incorrect': incorrect})

if __name__ == '__main__':
    app.run(debug=True)