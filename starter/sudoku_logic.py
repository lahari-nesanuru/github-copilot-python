import copy
import random

SIZE = 9
EMPTY = 0

DIFFICULTY_SETTINGS = {
    "easy": 40,
    "medium": 32,
    "hard": 24,
}


def deep_copy(board):
    return copy.deepcopy(board)


def create_empty_board():
    return [[EMPTY for _ in range(SIZE)] for _ in range(SIZE)]


def is_safe(board, row, col, num):
    # Check row and column
    for x in range(SIZE):
        if board[row][x] == num or board[x][col] == num:
            return False
    # Check 3x3 box
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True


def has_conflict(board, row, col, value, locked=False):
    if locked or value == EMPTY:
        return False

    for x in range(SIZE):
        if x != col and board[row][x] == value:
            return True
        if x != row and board[x][col] == value:
            return True

    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if (start_row + i != row or start_col + j != col) and board[start_row + i][start_col + j] == value:
                return True
    return False


def fill_board(board):
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == EMPTY:
                possible = list(range(1, SIZE + 1))
                random.shuffle(possible)
                for candidate in possible:
                    if is_safe(board, row, col, candidate):
                        board[row][col] = candidate
                        if fill_board(board):
                            return True
                        board[row][col] = EMPTY
                return False
    return True


def count_solutions(board, limit=2):
    working_board = deep_copy(board)

    def search():
        nonlocal count
        if count >= limit:
            return

        best_row = None
        best_col = None
        best_candidates = None
        for row in range(SIZE):
            for col in range(SIZE):
                if working_board[row][col] == EMPTY:
                    candidates = get_candidates(working_board, row, col)
                    if not candidates:
                        return
                    if best_candidates is None or len(candidates) < len(best_candidates):
                        best_row = row
                        best_col = col
                        best_candidates = candidates

        if best_row is None:
            count += 1
            return

        for candidate in best_candidates:
            if count >= limit:
                return
            working_board[best_row][best_col] = candidate
            search()
            working_board[best_row][best_col] = EMPTY

    count = 0
    search()
    return count


def find_empty_cell(board):
    best_cell = None
    best_candidates = None
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == EMPTY:
                candidates = get_candidates(board, row, col)
                if not candidates:
                    return None, None
                if best_candidates is None or len(candidates) < len(best_candidates):
                    best_cell = (row, col)
                    best_candidates = candidates
    return best_cell if best_cell is not None else (None, None)


def get_candidates(board, row, col):
    candidates = []
    for num in range(1, SIZE + 1):
        if is_safe(board, row, col, num):
            candidates.append(num)
    return candidates


def resolve_clues(clues=None, difficulty=None):
    if difficulty is not None:
        normalized = difficulty.lower()
        if normalized not in DIFFICULTY_SETTINGS:
            raise ValueError(f"Unsupported difficulty: {difficulty}")
        return DIFFICULTY_SETTINGS[normalized]

    if clues is None:
        return 35
    return clues


def remove_cells(board, clues):
    target_clues = clues
    if target_clues < 17:
        raise ValueError("Target clue count is too low to guarantee a unique solution")

    positions = [(row, col) for row in range(SIZE) for col in range(SIZE)]
    max_passes = 200

    for _ in range(max_passes):
        if sum(1 for row in board for cell in row if cell != EMPTY) <= target_clues:
            break

        progress = False
        random.shuffle(positions)
        for row, col in positions:
            if sum(1 for row_value in board for cell in row_value if cell != EMPTY) <= target_clues:
                break
            if board[row][col] == EMPTY:
                continue

            original_value = board[row][col]
            board[row][col] = EMPTY
            if count_solutions(board) == 1:
                progress = True
            else:
                board[row][col] = original_value

        if not progress:
            break

    if sum(1 for row in board for cell in row if cell != EMPTY) != target_clues:
        raise ValueError("Unable to reach the requested clue count while preserving a unique solution")


def generate_puzzle(clues=35, difficulty=None):
    resolved_clues = resolve_clues(clues=clues, difficulty=difficulty)

    for _ in range(20):
        board = create_empty_board()
        fill_board(board)
        solution = deep_copy(board)
        puzzle = deep_copy(board)
        try:
            remove_cells(puzzle, resolved_clues)
            return puzzle, solution
        except ValueError:
            continue

    raise ValueError("Unable to generate a puzzle with the requested difficulty")
