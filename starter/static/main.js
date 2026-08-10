// Client-side rendering and interaction for the Flask-backed Sudoku
const SIZE = 9;
const LEADERBOARD_KEY = 'sudoku-top10-leaderboard';
let puzzle = [];
let timerIntervalId = null;
let timerStartTime = null;
let elapsedSeconds = 0;
let currentGameId = 0;
let hintsUsed = 0;
let hintedCells = new Set();
let leaderboardSavedForCurrentGame = false;

function sanitizePlayerName(rawName) {
  const cleaned = String(rawName || '').replace(/[<>]/g, '').trim();
  const trimmed = cleaned.slice(0, 20);
  return trimmed || 'Anonymous';
}

function getStoredLeaderboard() {
  try {
    const raw = window.localStorage.getItem(LEADERBOARD_KEY);
    if (!raw) {
      return [];
    }
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed : [];
  } catch (error) {
    return [];
  }
}

function normalizeLeaderboardEntry(entry) {
  const difficulty = String(entry && entry.difficulty ? entry.difficulty : 'easy');
  const time = Number(entry && entry.time);
  const hints = Number(entry && entry.hints);
  return {
    playerName: sanitizePlayerName(entry && entry.playerName),
    difficulty,
    time: Number.isFinite(time) ? time : 0,
    hints: Number.isFinite(hints) ? hints : 0,
  };
}

function saveLeaderboardEntry(entry) {
  const normalized = normalizeLeaderboardEntry(entry);
  const entries = getStoredLeaderboard().map(normalizeLeaderboardEntry);
  entries.push(normalized);
  entries.sort((a, b) => {
    if (a.time !== b.time) {
      return a.time - b.time;
    }
    if (a.hints !== b.hints) {
      return a.hints - b.hints;
    }
    return a.playerName.localeCompare(b.playerName);
  });

  const topEntries = entries.slice(0, 10);
  try {
    window.localStorage.setItem(LEADERBOARD_KEY, JSON.stringify(topEntries));
  } catch (error) {
    // Ignore localStorage write failures and keep the in-memory best effort.
  }
  return topEntries;
}

function renderLeaderboard() {
  const list = document.getElementById('leaderboard-list');
  if (!list) {
    return;
  }

  const entries = getStoredLeaderboard().map(normalizeLeaderboardEntry);
  if (!entries.length) {
    list.innerHTML = '<li class="empty">No scores yet — solve a puzzle to set the first record.</li>';
    return;
  }

  list.innerHTML = '';
  entries.slice(0, 10).forEach((entry, index) => {
    const item = document.createElement('li');
    item.innerText = `${index + 1}. ${entry.playerName} — ${entry.difficulty.toUpperCase()} — ${formatTime(entry.time)} — ${entry.hints} hints`;
    list.appendChild(item);
  });
}

function applyTheme(theme) {
  const isDarkMode = theme === 'dark';
  document.body.classList.toggle('dark-mode', isDarkMode);
  const toggleButton = document.getElementById('theme-toggle');
  if (toggleButton) {
    toggleButton.innerText = isDarkMode ? 'Light Mode' : 'Dark Mode';
    toggleButton.setAttribute('aria-label', isDarkMode ? 'Switch to light mode' : 'Switch to dark mode');
  }
  try {
    window.localStorage.setItem('sudoku-theme', theme);
  } catch (error) {
    // Ignore localStorage write failures.
  }
}

function initializeTheme() {
  try {
    const savedTheme = window.localStorage.getItem('sudoku-theme');
    applyTheme(savedTheme === 'dark' ? 'dark' : 'light');
  } catch (error) {
    applyTheme('light');
  }
}

function handleCellInput(event) {
  const input = event.target;
  if (!(input instanceof HTMLInputElement) || !input.classList.contains('sudoku-cell')) {
    return;
  }

  const val = input.value.replace(/[^1-9]/g, '');
  input.value = val;

  const row = parseInt(input.dataset.row, 10);
  const col = parseInt(input.dataset.col, 10);
  const nextValue = val ? parseInt(val, 10) : 0;
  puzzle[row][col] = nextValue;
  applyImmediateValidation(input);
}

function createBoardElement() {
  const boardDiv = document.getElementById('sudoku-board');
  boardDiv.innerHTML = '';
  for (let i = 0; i < SIZE; i++) {
    const rowDiv = document.createElement('div');
    rowDiv.className = 'sudoku-row';
    for (let j = 0; j < SIZE; j++) {
      const input = document.createElement('input');
      input.type = 'text';
      input.maxLength = 1;
      input.className = 'sudoku-cell';
      input.dataset.row = i;
      input.dataset.col = j;
      rowDiv.appendChild(input);
    }
    boardDiv.appendChild(rowDiv);
  }
}

function formatTime(totalSeconds) {
  const minutes = Math.floor(totalSeconds / 60).toString().padStart(2, '0');
  const seconds = (totalSeconds % 60).toString().padStart(2, '0');
  return `${minutes}:${seconds}`;
}

function updateTimerDisplay() {
  const elapsed = timerStartTime === null ? 0 : Math.floor((Date.now() - timerStartTime) / 1000);
  elapsedSeconds = elapsed;
  document.getElementById('timer').innerText = `Time: ${formatTime(elapsed)}`;
}

function stopTimer() {
  if (timerIntervalId !== null) {
    clearInterval(timerIntervalId);
    timerIntervalId = null;
  }
}

function startTimer() {
  stopTimer();
  timerStartTime = Date.now();
  elapsedSeconds = 0;
  updateTimerDisplay();
  timerIntervalId = window.setInterval(() => {
    updateTimerDisplay();
  }, 1000);
}

function updateHintCountDisplay() {
  document.getElementById('hints-used').innerText = `Hints: ${hintsUsed}`;
}

function applyImmediateValidation(input) {
  const row = parseInt(input.dataset.row, 10);
  const col = parseInt(input.dataset.col, 10);
  const value = input.value ? parseInt(input.value, 10) : 0;
  const isLocked = input.disabled || input.classList.contains('prefilled') || input.classList.contains('hinted');

  if (!input.value || isLocked) {
    input.classList.remove('conflict');
    return;
  }

  const conflict = isCellConflict(puzzle, row, col, value, { locked: isLocked });
  if (conflict) {
    input.classList.add('conflict');
  } else {
    input.classList.remove('conflict');
  }
}

function renderPuzzle(puz) {
  puzzle = puz.map((row) => row.slice());
  hintedCells = new Set();
  hintsUsed = 0;
  createBoardElement();
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  for (let i = 0; i < SIZE; i++) {
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = puzzle[i][j];
      const inp = inputs[idx];
      inp.className = 'sudoku-cell';
      if (val !== 0) {
        inp.value = val;
        inp.disabled = true;
        inp.classList.add('prefilled');
      } else {
        inp.value = '';
        inp.disabled = false;
      }
      if (hintedCells.has(idx)) {
        inp.disabled = true;
        inp.classList.add('hinted');
      }
      inp.classList.remove('conflict');
    }
  }
}

async function newGame() {
  currentGameId += 1;
  leaderboardSavedForCurrentGame = false;
  stopTimer();
  const difficulty = document.getElementById('difficulty').value;
  const res = await fetch(`/new?difficulty=${difficulty}`);
  const data = await res.json();
  if (data.error) {
    document.getElementById('message').style.color = '#d32f2f';
    document.getElementById('message').innerText = data.error;
    return;
  }
  renderPuzzle(data.puzzle);
  updateHintCountDisplay();
  document.getElementById('message').innerText = '';
  renderLeaderboard();
  startTimer();
}

async function requestHint() {
  const gameId = currentGameId;
  const res = await fetch('/hint', {method: 'POST'});
  const data = await res.json();
  if (gameId !== currentGameId) {
    return;
  }
  if (data.error) {
    document.getElementById('message').style.color = '#d32f2f';
    document.getElementById('message').innerText = data.error;
    return;
  }
  if (data.message) {
    document.getElementById('message').style.color = '#d32f2f';
    document.getElementById('message').innerText = data.message;
    return;
  }
  const idx = data.row * SIZE + data.col;
  puzzle[data.row][data.col] = data.value;
  hintedCells.add(idx);
  hintsUsed = data.hints_used;
  updateHintCountDisplay();
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  const input = inputs[idx];
  if (input) {
    input.value = data.value;
    input.disabled = true;
    input.className = 'sudoku-cell hinted';
  }
  document.getElementById('message').innerText = '';
}

async function checkSolution() {
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  const board = [];
  for (let i = 0; i < SIZE; i++) {
    board[i] = [];
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = inputs[idx].value;
      board[i][j] = val ? parseInt(val, 10) : 0;
    }
  }
  const gameId = currentGameId;
  const res = await fetch('/check', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({board, elapsed_seconds: elapsedSeconds})
  });
  const data = await res.json();
  if (gameId !== currentGameId) {
    return;
  }
  const msg = document.getElementById('message');
  if (data.error) {
    msg.style.color = '#d32f2f';
    msg.innerText = data.error;
    return;
  }
  const incorrect = new Set(data.incorrect.map(x => x[0]*SIZE + x[1]));
  for (let idx = 0; idx < inputs.length; idx++) {
    const inp = inputs[idx];
    if (inp.disabled) continue;
    inp.classList.remove('incorrect');
    inp.classList.remove('conflict');
    if (incorrect.has(idx)) {
      inp.classList.add('incorrect');
    }
  }
  if (incorrect.size === 0 && data.solved === true) {
    stopTimer();
    if (!leaderboardSavedForCurrentGame) {
      const playerName = sanitizePlayerName(document.getElementById('player-name').value);
      saveLeaderboardEntry({
        playerName,
        difficulty: document.getElementById('difficulty').value,
        time: elapsedSeconds,
        hints: hintsUsed,
      });
      leaderboardSavedForCurrentGame = true;
      renderLeaderboard();
    }
    msg.style.color = '#388e3c';
    msg.innerText = `Congratulations! You solved it! Time: ${formatTime(elapsedSeconds)} | Hints: ${hintsUsed}`;
  } else if (incorrect.size === 0) {
    msg.style.color = '#388e3c';
    msg.innerText = `Congratulations! You solved it! Time: ${formatTime(elapsedSeconds)} | Hints: ${hintsUsed}`;
  } else {
    msg.style.color = '#d32f2f';
    msg.innerText = 'Some cells are incorrect.';
  }
}

// Wire buttons
if (typeof window !== 'undefined') {
  window.addEventListener('load', () => {
    const boardDiv = document.getElementById('sudoku-board');
    if (boardDiv) {
      boardDiv.addEventListener('input', handleCellInput);
    }
    document.getElementById('new-game').addEventListener('click', newGame);
    document.getElementById('check-solution').addEventListener('click', checkSolution);
    document.getElementById('hint').addEventListener('click', requestHint);
    document.getElementById('theme-toggle').addEventListener('click', () => {
      const currentTheme = document.body.classList.contains('dark-mode') ? 'dark' : 'light';
      applyTheme(currentTheme === 'dark' ? 'light' : 'dark');
    });
    initializeTheme();
    renderLeaderboard();
    // initialize
    newGame();
  });
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    sanitizePlayerName,
    getStoredLeaderboard,
    normalizeLeaderboardEntry,
    saveLeaderboardEntry,
    renderLeaderboard,
    applyTheme,
    initializeTheme,
  };
}