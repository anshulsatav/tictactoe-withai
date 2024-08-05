# Tic-Tac-Toe with AI

This project is a simple implementation of the Tic-Tac-Toe game using Pygame. It includes an AI opponent that uses the minimax algorithm with alpha-beta pruning to make optimal moves.

## Features

- **Two-player mode**: Play against another human.
- **AI opponent**: Challenge the AI, which uses the minimax algorithm with alpha-beta pruning to make decisions.
- **Restart functionality**: Press the `R` key to restart the game.
- **Game status display**: The game announces the winner or if it's a draw.

## Requirements

- Python 3.x
- Pygame
- NumPy

## Usage

1. **Run the game**:

    ```bash
    python tic_tac_toe.py
    ```

2. **Playing the Game**:
   - Click on the cells to make a move if playing against another human.
   - If playing against the AI, click to place 'X', and the AI will automatically make a move as 'O'.
   - The game will display "X Wins!", "O Wins!", or "Draw!" when the game ends.
   - Press the `R` key to restart the game.

## Code Overview

- **Game Setup**:
  - `pygame` is used for rendering the game board and handling user input.
  - The board is a 3x3 grid where 'X' and 'O' are placed.

- **Functions**:
  - `draw_lines()`: Draws the grid lines on the game board.
  - `draw_figures()`: Draws 'X' and 'O' on the board based on the current state.
  - `draw_winner(winner)`: Displays the result of the game on the screen.
  - `check_winner()`: Checks the current state of the board to determine if there is a winner or if the game is a draw.
  - `minimax(board, depth, alpha, beta, is_maximizing)`: Implements the minimax algorithm with alpha-beta pruning for optimal AI moves.
  - `best_move()`: Determines the best move for the AI using the minimax function.
  - `restart_game()`: Resets the board and prepares for a new game.


