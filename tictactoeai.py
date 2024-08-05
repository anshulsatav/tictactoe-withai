# Importing the necessary libraries
import pygame
import numpy as np
import sys
import time

# Initialize Pygame
pygame.init()

# Constants for the game
WIDTH, HEIGHT = 500, 500  # Screen width and height
LINE_WIDTH = 15  # Width of the lines on the board
BOARD_ROWS = 3  # Number of rows in the board
BOARD_COLS = 3  # Number of columns in the board
SQUARE_SIZE = WIDTH // BOARD_COLS  # Size of each square on the board
CIRCLE_RADIUS = SQUARE_SIZE // 3  # Radius of the circles
CIRCLE_WIDTH = 15  # Width of the circle outline
CROSS_WIDTH = 25  # Width of the cross lines
SPACE = SQUARE_SIZE // 4  # Space between lines in the cross

# Colors used in the game
RED = (255, 0, 0)
BLACK = (0, 0, 0)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)
MENU_COLOR = (100, 100, 100)  # Color for the menu text

# Setup the display window
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption('Tic Tac Toe')
screen.fill(BLACK)  # Fill the screen with black color

# Calculate font size based on screen width
def calculate_font_size(width):
    base_size = 74  # Base font size
    return int(base_size * (width / 500))  # Adjust font size based on screen width

# Set up the font
font_size = calculate_font_size(WIDTH)  # Calculate initial font size
font = pygame.font.Font(None, font_size)  # Create a font object with the calculated size

# Initialize the game board
board = np.full((BOARD_ROWS, BOARD_COLS), ' ')

# Game modes
AI_MODE = "AI"  # Mode where player plays against AI
TWO_PLAYER_MODE = "Two Player"  # Mode where two players play against each other
game_mode = None  # To store the selected game mode

# Draw the game board
def draw_board():
    # Draw horizontal lines
    pygame.draw.line(screen, RED, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, RED, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
    # Draw vertical lines
    pygame.draw.line(screen, RED, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, RED, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

# Draw Xs and Os on the board
def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row, col] == 'X':
                # Draw X
                pygame.draw.line(screen, CROSS_COLOR, 
                                 (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), 
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, 
                                 (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), 
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)
            elif board[row, col] == 'O':
                # Draw O
                pygame.draw.circle(screen, CIRCLE_COLOR, 
                                   (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 
                                   CIRCLE_RADIUS, CIRCLE_WIDTH)

# Display the winner message
def print_winner(winner):
    global font
    font_size = calculate_font_size(WIDTH)  # Recalculate font size
    font = pygame.font.Font(None, font_size)  # Update the font size
    text = font.render(f"{winner} Wins!", True, RED)  # Create the winner text
    screen.blit(text, (WIDTH // 4, HEIGHT // 2))  # Render text on the screen
    pygame.display.update()  # Update the display
    time.sleep(2)  # Pause for 2 seconds

# Check if there is a winner
def check_winner():
    # Horizontal check
    for row in board:
        if all([cell == 'X' for cell in row]):
            return 'X'
        if all([cell == 'O' for cell in row]):
            return 'O'
    # Vertical check
    for col in board.T:
        if all([cell == 'X' for cell in col]):
            return 'X'
        if all([cell == 'O' for cell in col]):
            return 'O'
    # Diagonal check
    if all([board[i, i] == 'X' for i in range(BOARD_ROWS)]) or all([board[i, BOARD_COLS - 1 - i] == 'X' for i in range(BOARD_ROWS)]):
        return 'X'
    if all([board[i, i] == 'O' for i in range(BOARD_ROWS)]) or all([board[i, BOARD_COLS - 1 - i] == 'O' for i in range(BOARD_ROWS)]):
        return 'O'
    # Check for a draw
    if not any(' ' in row for row in board):
        return 'Draw'
    return None

# Minimax algorithm with alpha-beta pruning
def minimax(board, depth, alpha, beta, is_maximizing):
    winner = check_winner()
    if winner == 'X':
        return -1
    if winner == 'O':
        return 1
    if winner == 'Draw':
        return 0

    if is_maximizing:
        best_score = -1000000
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row, col] == ' ':
                    board[row, col] = 'O'
                    score = minimax(board, depth + 1, alpha, beta, False)
                    board[row, col] = ' '
                    best_score = max(score, best_score)
                    alpha = max(alpha, best_score)
                    if beta <= alpha:
                        break
        return best_score
    else:
        best_score = 1000000
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row, col] == ' ':
                    board[row, col] = 'X'
                    score = minimax(board, depth + 1, alpha, beta, True)
                    board[row, col] = ' '
                    best_score = min(score, best_score)
                    beta = min(beta, best_score)
                    if beta <= alpha:
                        break
        return best_score

# Determine the best move for the AI
def best_move():
    best_score = -1000000
    move = None
    alpha = -1000000
    beta = 1000000
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row, col] == ' ':
                board[row, col] = 'O'
                score = minimax(board, 0, alpha, beta, False)
                board[row, col] = ' '
                if score > best_score:
                    best_score = score
                    move = (row, col)
                alpha = max(alpha, best_score)
    return move

# Restart the game and drawing the initial board
def restart_game():
    global board
    board = np.full((BOARD_ROWS, BOARD_COLS), ' ')
    screen.fill(BLACK)
    draw_board()

# Draw the game menu
def draw_menu():
    global font
    font_size = calculate_font_size(WIDTH)  # Recalculate font size
    font = pygame.font.Font(None, font_size)  # Update the font size
    screen.fill(BLACK)  # Fill the screen with black
    ai_text = font.render('Play AI', True, RED)  # Render text for AI mode
    two_player_text = font.render('Play Two Player', True, RED)  # Render text for two-player mode
    screen.blit(ai_text, (WIDTH // 5, HEIGHT // 3))  # Display AI option text
    screen.blit(two_player_text, (WIDTH // 5, HEIGHT // 2))  # Display Two Player option text
    pygame.display.update()  # Update the display

# Handle clicks in the menu
def handle_menu_click(pos):
    global game_mode
    x, y = pos
    # Check if click is within the area for AI mode
    if WIDTH // 4 < x < 3 * WIDTH // 4:
        if HEIGHT // 3 < y < HEIGHT // 3 + font_size:
            game_mode = AI_MODE
        # Check if click is within the area for Two Player mode
        elif HEIGHT // 2 < y < HEIGHT // 2 + font_size:
            game_mode = TWO_PLAYER_MODE
        return True
    return False

# Main loop for menu selection
game_mode = None
while game_mode is None:
    draw_menu()  # Draw the menu
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()  # Quit Pygame
            sys.exit()  # Exit the program
        if event.type == pygame.MOUSEBUTTONDOWN:
            if handle_menu_click(event.pos):  # Handle menu click
                break

# Initialize game settings based on the chosen mode
restart_game()  # Restart the game
player = 'X'  # Starting player
game_over = False  # Game status
winner = None  # Winner status

# Main loop for the game
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()  # Quit Pygame
            sys.exit()  # Exit the program
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            # Calculate the row and column of the clicked cell
            mouseX = event.pos[0] // SQUARE_SIZE
            mouseY = event.pos[1] // SQUARE_SIZE

            if board[mouseY, mouseX] == ' ':
                board[mouseY, mouseX] = player  # Place the player's move
                if check_winner() is None:
                    if player == 'X':
                        if game_mode == AI_MODE:
                            player = 'O'
                            pygame.display.update()  # Update display to show AI move
                            time.sleep(0.5)  # Short pause before AI move
                            move = best_move()  # Get the AI's move
                            if move:
                                board[move[0], move[1]] = 'O'
                                player = 'X'
                        elif game_mode == TWO_PLAYER_MODE:
                            player = 'O'
                    else:
                        player = 'X'
                game_over = check_winner() is not None  # Check if the game is over
                winner = check_winner()  # Get the winner
                if winner:
                    print_winner(winner)  # Display the winner message

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart_game()  # Restart the game when 'R' is pressed
                player = 'X'
                game_over = False
                winner = None

        if event.type == pygame.VIDEORESIZE:
            WIDTH, HEIGHT = event.size  # Update screen size
            SQUARE_SIZE = WIDTH // BOARD_COLS  # Recalculate square size
            CIRCLE_RADIUS = SQUARE_SIZE // 3  # Recalculate circle radius
            SPACE = SQUARE_SIZE // 4  # Recalculate space for cross lines
            font_size = calculate_font_size(WIDTH)  # Recalculate font size
            font = pygame.font.Font(None, font_size)  # Update font size
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)  # Set new screen size
            restart_game()  # Redraw the board with new dimensions

    draw_figures()  # Draw Xs and Os
    pygame.display.update()  # Update the display
