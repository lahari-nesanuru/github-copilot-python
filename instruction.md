# GitHub Copilot Instructions - Sudoku Project

## Project Overview

This project is a Python Flask Sudoku game being refactored and extended
from legacy code into a clean, maintainable web application.

Existing functionality must continue working while new features are added.

## General Development Rules

- Write clean, readable and maintainable code.
- Use meaningful variable and function names.
- Keep functions small and focused.
- Prefer modular and reusable code.
- Avoid unnecessary duplication.
- Follow Python PEP 8 conventions.
- Handle errors gracefully.
- Avoid unnecessary dependencies.
- Do not modify unrelated files.
- Preserve working functionality when adding new features.
- Test changes before considering them complete.

## Sudoku Requirements

The application must:

- Generate valid Sudoku puzzles.
- Ensure every generated puzzle has exactly one solution.
- Support Easy, Medium and Hard difficulty levels.
- Keep prefilled cells locked.
- Validate user input.
- Provide immediate feedback for invalid entries.
- Provide a Check Puzzle feature.
- Provide a Hint feature.
- Display a completion message when the puzzle is solved.
- Track the player's solving time.

## User Interface Requirements

The interface should:

- Work on desktop and mobile devices.
- Support light and dark modes.
- Clearly distinguish the nine 3x3 Sudoku sections.
- Keep text and controls readable.
- Provide clear visual feedback.
- Use accessible labels and controls where appropriate.
- Avoid unnecessary layout shifts.

## Leaderboard Requirements

The application should maintain a Top 10 leaderboard using browser
localStorage.

Each completed game should store:

- Player name
- Completion time
- Difficulty
- Number of hints used

Only the best ten scores should be displayed.

## Testing Requirements

Before modifying existing functionality:

- Establish a baseline test suite.
- Run the tests before refactoring.
- Run the tests after significant changes.
- Add tests for important new functionality when appropriate.
- Investigate test failures instead of hiding them.
- Do not claim functionality works without actually testing it.

## GitHub Copilot Guidelines

When suggesting changes:

1. First inspect and understand the existing project.
2. Prefer small, controlled changes.
3. Preserve existing functionality.
4. Avoid unnecessary rewrites.
5. Explain significant architectural changes.
6. Identify possible edge cases.
7. Suggest appropriate tests.
8. Do not modify unrelated files.

If a suggested solution conflicts with these instructions, explain the
conflict before implementing it.

## Code Quality

Prioritize:

- Correctness
- Readability
- Maintainability
- Modularity
- Testability
- Accessibility
- Responsive design

Do not generate fake test results or claim that code works without
running and verifying it.