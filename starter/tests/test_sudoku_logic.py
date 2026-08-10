import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import sudoku_logic


def test_create_empty_board_returns_nine_by_nine_grid():
    board = sudoku_logic.create_empty_board()

    assert len(board) == sudoku_logic.SIZE
    assert all(len(row) == sudoku_logic.SIZE for row in board)
    assert all(cell == sudoku_logic.EMPTY for row in board for cell in row)


def test_is_safe_allows_valid_move_and_rejects_conflict():
    board = sudoku_logic.create_empty_board()

    assert sudoku_logic.is_safe(board, 0, 0, 5)

    board[0][1] = 5
    assert not sudoku_logic.is_safe(board, 0, 0, 5)


def test_generate_puzzle_returns_puzzle_and_solution():
    puzzle, solution = sudoku_logic.generate_puzzle(35)

    assert len(puzzle) == sudoku_logic.SIZE
    assert len(solution) == sudoku_logic.SIZE
    assert all(len(row) == sudoku_logic.SIZE for row in puzzle)
    assert all(len(row) == sudoku_logic.SIZE for row in solution)


def test_easy_puzzle_has_expected_clue_count():
    puzzle, _ = sudoku_logic.generate_puzzle(difficulty="easy")

    assert count_clues(puzzle) == 40


def test_medium_puzzle_has_expected_clue_count():
    puzzle, _ = sudoku_logic.generate_puzzle(difficulty="medium")

    assert count_clues(puzzle) == 32


def test_hard_puzzle_has_expected_clue_count():
    puzzle, _ = sudoku_logic.generate_puzzle(difficulty="hard")

    assert count_clues(puzzle) == 24


def test_generated_puzzles_for_each_difficulty_have_exactly_one_solution():
    for difficulty in ["easy", "medium", "hard"]:
        puzzle, _ = sudoku_logic.generate_puzzle(difficulty=difficulty)
        assert sudoku_logic.count_solutions(puzzle) == 1


def test_invalid_difficulty_raises_value_error():
    with pytest.raises(ValueError):
        sudoku_logic.generate_puzzle(difficulty="insane")


def test_completed_valid_board_has_exactly_one_solution():
    board = [
        [5, 3, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4],
        [2, 8, 7, 4, 1, 9, 6, 3, 5],
        [3, 4, 5, 2, 8, 6, 1, 7, 9],
    ]

    assert sudoku_logic.count_solutions(board) == 1


def test_board_with_multiple_solutions_has_more_than_one_solution():
    board = sudoku_logic.create_empty_board()
    board[0][0] = 1
    board[0][1] = 2

    assert sudoku_logic.count_solutions(board) >= 2


def test_generated_puzzle_has_exactly_one_solution():
    puzzle, _ = sudoku_logic.generate_puzzle(35)

    assert sudoku_logic.count_solutions(puzzle) == 1


def test_has_conflict_detects_row_duplicate():
    board = sudoku_logic.create_empty_board()
    board[0][1] = 5

    assert sudoku_logic.has_conflict(board, 0, 0, 5)


def test_has_conflict_detects_column_duplicate():
    board = sudoku_logic.create_empty_board()
    board[1][0] = 5

    assert sudoku_logic.has_conflict(board, 0, 0, 5)


def test_has_conflict_detects_box_duplicate():
    board = sudoku_logic.create_empty_board()
    board[2][2] = 5

    assert sudoku_logic.has_conflict(board, 0, 0, 5)


def test_has_conflict_allows_valid_value():
    board = sudoku_logic.create_empty_board()

    assert not sudoku_logic.has_conflict(board, 0, 0, 5)


def test_has_conflict_skips_empty_value():
    board = sudoku_logic.create_empty_board()

    assert not sudoku_logic.has_conflict(board, 0, 0, sudoku_logic.EMPTY)


def test_has_conflict_skips_locked_cells():
    board = sudoku_logic.create_empty_board()
    board[0][1] = 5

    assert not sudoku_logic.has_conflict(board, 0, 0, 5, locked=True)


def count_clues(board):
    return sum(1 for row in board for cell in row if cell != sudoku_logic.EMPTY)
