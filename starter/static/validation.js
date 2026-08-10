function isCellConflict(board, row, col, value, options = {}) {
  if (!value) {
    return false;
  }

  if (options.locked) {
    return false;
  }

  const size = board.length;
  const boxSize = 3;

  for (let i = 0; i < size; i += 1) {
    if (i !== col && board[row][i] === value) {
      return true;
    }
    if (i !== row && board[i][col] === value) {
      return true;
    }
  }

  const boxRowStart = Math.floor(row / boxSize) * boxSize;
  const boxColStart = Math.floor(col / boxSize) * boxSize;

  for (let i = boxRowStart; i < boxRowStart + boxSize; i += 1) {
    for (let j = boxColStart; j < boxColStart + boxSize; j += 1) {
      if ((i !== row || j !== col) && board[i][j] === value) {
        return true;
      }
    }
  }

  return false;
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { isCellConflict };
}
