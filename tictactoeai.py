import pygame
import numpy as np
import sys
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 500, 500
LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4

# Colors
RED = (255, 0, 0)
BLACK = (0, 0, 0)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)
MENU_COLOR = (100, 100, 100)

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe')
screen.fill(BLACK)

def calculate_font_size(width):
    """Calculate font size based on screen width."""
    base_size = 74
    return int(base_size * (width / 500))

# Font setup
font_size = calculate_font_size(WIDTH)
font = pygame.font.Font(None, font_size)

# Board
board = np.full((BOARD_ROWS, BOARD_COLS), ' ')

# Game modes
AI_MODE = "AI"
TWO_PLAYER_MODE = "Two Player"
game_mode = None

# Functions
def draw_board():
    # Horizontal lines
    pygame.draw.line(screen, RED, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, RED, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
    # Vertical lines
    pygame.draw.line(screen, RED, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, RED, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row, col] == 'X':
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), 
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), 
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)
            elif board[row, col] == 'O':
                pygame.draw.circle(screen, CIRCLE_COLOR, 
                                   (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 
                                   CIRCLE_RADIUS, CIRCLE_WIDTH)

def print_winner(winner):
    global font
    font_size = calculate_font_size(WIDTH)
    font = pygame.font.Font(None, font_size)
    text = font.render(f"{winner} Wins!", True, RED)
    screen.blit(text, (WIDTH // 4, HEIGHT // 2))
    pygame.display.update()
    time.sleep(2)

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
    if not any(' ' in row for row in board):
        return 'Draw'
    return None

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

def restart_game():
    global board
    board = np.full((BOARD_ROWS, BOARD_COLS), ' ')
    screen.fill(BLACK)
    draw_board()

def draw_menu():
    global font
    font_size = calculate_font_size(WIDTH)
    font = pygame.font.Font(None, font_size)
    screen.fill(BLACK)
    ai_text = font.render('Play AI', True, RED)
    two_player_text = font.render('Play Two Player', True, RED)
    screen.blit(ai_text, (WIDTH // 5, HEIGHT // 3))
    screen.blit(two_player_text, (WIDTH // 5, HEIGHT // 2))
    pygame.display.update()

def handle_menu_click(pos):
    global game_mode
    x, y = pos
    if WIDTH // 4 < x < 3 * WIDTH // 4:
        if HEIGHT // 3 < y < HEIGHT // 3 + font_size:
            game_mode = AI_MODE
        elif HEIGHT // 2 < y < HEIGHT // 2 + font_size:
            game_mode = TWO_PLAYER_MODE
        return True
    return False

# Main loop
game_mode = None
while game_mode is None:
    draw_menu()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if handle_menu_click(event.pos):
                break

# Initialize game settings based on chosen mode
restart_game()
player = 'X'
game_over = False
winner = None

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0] // SQUARE_SIZE
            mouseY = event.pos[1] // SQUARE_SIZE

            if board[mouseY, mouseX] == ' ':
                board[mouseY, mouseX] = player
                if check_winner() is None:
                    if player == 'X':
                        if game_mode == AI_MODE:
                            player = 'O'
                            pygame.display.update()
                            time.sleep(0.5)
                            move = best_move()
                            if move:
                                board[move[0], move[1]] = 'O'
                                player = 'X'
                        elif game_mode == TWO_PLAYER_MODE:
                            player = 'O'
                    else:
                        player = 'X'
                game_over = check_winner() is not None
                winner = check_winner()
                if winner:
                    print_winner(winner)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart_game()
                player = 'X'
                game_over = False
                winner = None

        if event.type == pygame.VIDEORESIZE:
            WIDTH, HEIGHT = event.size
            SQUARE_SIZE = WIDTH // BOARD_COLS
            CIRCLE_RADIUS = SQUARE_SIZE // 3
            SPACE = SQUARE_SIZE // 4
            font_size = calculate_font_size(WIDTH)
            font = pygame.font.Font(None, font_size)
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
            restart_game()

    draw_figures()
    pygame.display.update()
