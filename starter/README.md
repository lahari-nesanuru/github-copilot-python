# Sudoku Game — Refactored with GitHub Copilot

A modern, responsive Sudoku game built with **Python Flask, JavaScript, HTML, and CSS**. This project started from a simple Flask Sudoku application and was refactored to improve maintainability, user experience, validation, puzzle generation, and gameplay features.

## Features

* 🎯 **Valid Sudoku Puzzle Generation**

  * Generates a complete valid Sudoku solution.
  * Creates puzzles by removing cells from the solution.
  * Ensures the generated puzzle has a unique solution.
  * Supports Easy, Medium, and Hard difficulty levels.

* 🎚️ **Difficulty Selection**

  * Easy — 40 clues
  * Medium — 32 clues
  * Hard — 24 clues

* ⏱️ **Game Timer**

  * Automatically starts when a new puzzle is created.
  * Displays the elapsed solving time.
  * Stops when the puzzle is successfully completed.

* 💡 **Hint System**

  * Provides a correct value for an empty cell.
  * Tracks the number of hints used.
  * Hint-filled cells are visually distinguished from normal cells.

* ✅ **Solution Checking**

  * Checks the current board against the correct solution.
  * Highlights incorrect cells.
  * Displays a success message when the puzzle is solved.

* ⚡ **Immediate Input Validation**

  * Detects duplicate numbers in rows, columns, and 3×3 boxes.
  * Invalid entries are highlighted immediately.
  * Input is restricted to Sudoku values from 1–9.
  * Uses event delegation for board input handling.

* 🏆 **Top 10 Leaderboard**

  * Stores the best 10 scores using browser `localStorage`.
  * Stores:

    * Player name
    * Completion time
    * Number of hints used
    * Difficulty level
  * Scores are sorted by time, then hints used.

* 🌙 **Light/Dark Mode**

  * Includes a theme toggle.
  * Remembers the selected theme using `localStorage`.

* 📱 **Responsive Design**

  * Works on desktop and mobile screen sizes.
  * Uses responsive CSS and flexible controls.

* ♿ **Accessible and Distinct UI Feedback**

  * Different visual states are provided for:

    * Prefilled cells
    * Hint cells
    * Incorrect cells
    * Conflicting cells
  * Uses readable colors and accessible contrast.

## Technologies Used

### Backend

* Python 3
* Flask

### Frontend

* HTML5
* CSS3
* JavaScript

### Testing

* pytest
* Node.js built-in test runner

### Browser Storage

* `localStorage` for leaderboard and theme preferences

## Project Structure

```text
starter/
│
├── app.py
├── sudoku_logic.py
├── requirements.txt
├── README.md
│
├── static/
│   ├── main.js
│   ├── validation.js
│   └── styles.css
│
├── templates/
│   └── index.html
│
└── tests/
    ├── test_app.py
    ├── test_sudoku_logic.py
    └── validation.test.js
```

## How the Application Works

1. The user opens the Sudoku application.
2. A new Sudoku puzzle is generated automatically.
3. The user selects a difficulty level.
4. The application displays the generated puzzle.
5. The timer starts automatically.
6. The user enters values into empty cells.
7. Immediate validation detects conflicts.
8. The user can request hints when needed.
9. The user can use **Check Solution** to verify the current board.
10. When the puzzle is completely correct:

    * The timer stops.
    * A congratulatory message is displayed.
    * The completion time and hints used are shown.
    * The player can be recorded on the Top 10 leaderboard.

## Sudoku Puzzle Generation

The backend generates a complete valid Sudoku board using a randomized backtracking algorithm.

After generating the solution:

1. A copy of the solved board is created.
2. Cells are progressively removed.
3. After removing a cell, the application counts the number of possible solutions.
4. A removed cell is kept only when the puzzle still has exactly one solution.
5. The process continues until the requested clue count is reached.

This ensures that generated puzzles have a **unique solution**.

## Difficulty Levels

| Difficulty | Starting Clues |
| ---------- | -------------- |
| Easy       | 40             |
| Medium     | 32             |
| Hard       | 24             |

Fewer clues generally result in a more challenging puzzle.

## Input Validation

The frontend validates every user-entered value.

A value is considered conflicting if the same value already exists in:

* The same row
* The same column
* The same 3×3 box

The validation logic is implemented in:

```text
static/validation.js
```

The board uses **event delegation**, allowing input handling to be managed through the Sudoku board rather than attaching separate handlers to every cell.

## Error Handling

The application handles common errors gracefully.

Examples include:

* Invalid difficulty values
* Invalid clue counts
* No active game when requesting a hint
* Puzzle generation failures
* Invalid or incomplete solutions

Errors are returned by the Flask API and displayed to the user through the interface.

## API Endpoints

### `GET /`

Loads the Sudoku game interface.

### `GET /new`

Generates a new Sudoku puzzle.

Example:

```text
/new?difficulty=easy
```

The endpoint returns the generated puzzle as JSON.

### `POST /hint`

Provides a correct value for an empty cell in the current puzzle.

### `POST /check`

Checks the submitted board against the current Sudoku solution.

The response identifies incorrect cells and indicates when the puzzle has been successfully solved.

## Running the Project Locally

### 1. Clone the repository

```bash
git clone <YOUR-GITHUB-REPOSITORY-URL>
```

### 2. Navigate to the project

```bash
cd github-copilot-python/starter
```

### 3. Create a virtual environment

Windows:

```powershell
python -m venv .venv
```

### 4. Activate the virtual environment

PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```powershell
pip install -r requirements.txt
```

### 6. Start the Flask application

```powershell
python app.py
```

### 7. Open the application

Open your browser and visit:

```text
http://127.0.0.1:5000
```

## Running Tests

### Python Tests

Run:

```powershell
python -m pytest -q
```

The project currently passes all Python tests:

```text
33 passed
```

### JavaScript Validation Tests

Node.js is required for the JavaScript tests.

Run:

```powershell
node --test tests/validation.test.js
```

The validation test suite currently passes all tests:

```text
7 passed
0 failed
```

## Testing Coverage

The project includes tests for:

### Backend

* Flask application behavior
* Sudoku generation
* Sudoku solving logic
* Puzzle uniqueness
* Difficulty handling
* API behavior

### Frontend Validation

* Row conflicts
* Column conflicts
* 3×3 box conflicts
* Valid values
* Empty values
* Protected/locked cells

## Data Storage

The leaderboard does not require a database.

Scores are stored in the browser using:

```text
localStorage
```

The leaderboard stores a maximum of 10 entries.

The selected light/dark theme is also saved in `localStorage`.

## Security and Input Handling

The application performs basic client-side input sanitization for player names.

Player names are:

* Converted to strings
* Trimmed
* Limited to 20 characters
* Sanitized to remove `<` and `>` characters

The leaderboard is rendered using DOM text content rather than inserting player names as HTML.

## Improvements Made During Refactoring

The original Sudoku application was improved by introducing:

* Unique-solution puzzle generation
* Difficulty levels
* Timer functionality
* Hint functionality
* Immediate conflict validation
* Event delegation
* Solution checking
* Top 10 leaderboard
* Player names
* Light/dark theme
* Responsive UI
* Accessible visual feedback
* Automated Python and JavaScript tests
* Improved error handling
* More maintainable frontend and backend structure

## GitHub Copilot Usage

GitHub Copilot was used as a development assistance tool during the refactoring process.

It assisted with tasks such as:

* Refactoring existing code
* Implementing new game features
* Improving frontend interaction
* Adding validation
* Adding tests
* Improving error handling
* Reviewing and modifying existing functionality

The final project was manually tested using the application's test suites and browser functionality.

## Current Verification Status

| Requirement                   | Status      |
| ----------------------------- | ----------- |
| Sudoku puzzle generator       | ✅           |
| Unique solution               | ✅           |
| Difficulty selector           | ✅           |
| Timer                         | ✅           |
| Hint feature                  | ✅           |
| Hint cell styling             | ✅           |
| Solution checker              | ✅           |
| Event delegation              | ✅           |
| Immediate validation          | ✅           |
| Top 10 leaderboard            | ✅           |
| Player name                   | ✅           |
| Time and hints in leaderboard | ✅           |
| Congratulations message       | ✅           |
| Light/Dark mode               | ✅           |
| Responsive design             | ✅           |
| Error handling                | ✅           |
| Python tests                  | ✅ 33 passed |
| JavaScript tests              | ✅ 7 passed  |

## Conclusion

This project demonstrates how a basic Flask Sudoku application can be refactored into a more modern, maintainable, and user-friendly web application.

The final version combines backend Sudoku generation and validation with interactive frontend features such as difficulty selection, hints, timers, immediate validation, leaderboard storage, responsive design, and theme support.
