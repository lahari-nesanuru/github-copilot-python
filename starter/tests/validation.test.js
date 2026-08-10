const test = require('node:test');
const assert = require('node:assert/strict');

const { isCellConflict } = require('../static/validation.js');

function createBoard() {
  return Array.from({ length: 9 }, () => Array(9).fill(0));
}

test('detects duplicates in the same row', () => {
  const board = createBoard();
  board[0][1] = 5;

  assert.equal(isCellConflict(board, 0, 0, 5), true);
});

test('detects duplicates in the same column', () => {
  const board = createBoard();
  board[1][0] = 5;

  assert.equal(isCellConflict(board, 0, 0, 5), true);
});

test('detects duplicates in the same 3x3 box', () => {
  const board = createBoard();
  board[2][2] = 5;

  assert.equal(isCellConflict(board, 0, 0, 5), true);
});

test('allows a valid value when no conflict exists', () => {
  const board = createBoard();

  assert.equal(isCellConflict(board, 0, 0, 5), false);
});

test('does not treat empty input as a conflict', () => {
  const board = createBoard();

  assert.equal(isCellConflict(board, 0, 0, 0), false);
});

test('does not flag protected cells', () => {
  const board = createBoard();
  board[0][1] = 5;

  assert.equal(isCellConflict(board, 0, 0, 5, { locked: true }), false);
});
