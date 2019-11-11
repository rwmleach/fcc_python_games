"""
Connect 4 Tutorial
https://www.youtube.com/watch?v=XGf2GcyHPhc
"""

import numpy
import pygame
import sys
import math

ROW_COUNT = 6
COLUMN_COUNT = 7

RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)


def create_board():
    new_board = numpy.zeros((ROW_COUNT, COLUMN_COUNT))
    return new_board


def print_board(board):
    print(numpy.flip(board, 0))


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def winning_move(board, piece):
    # Check horizontal locations
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece \
                    and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 2):
            if board[r][c] == piece and board[r+1][c] == piece \
                    and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check positive slope diagonals
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r+1][c+1] == piece \
                    and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check negative slope diagonals
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece \
                    and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True


def draw_board(board):
    flipped = numpy.flip(board, 0)
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARE_SIZE,
                                            r*SQUARE_SIZE+SQUARE_SIZE,
                                            SQUARE_SIZE, SQUARE_SIZE))
            if flipped[r][c] == 1:
                color = RED
            elif flipped[r][c] == 2:
                color = YELLOW
            else:
                color = BLACK
            pygame.draw.circle(screen, color,
                               (int(c*SQUARE_SIZE+SQUARE_SIZE/2),
                                int(r*SQUARE_SIZE+SQUARE_SIZE
                                + SQUARE_SIZE/2),), RADIUS)
    pygame.display.update()


game_board = create_board()
game_over = False
turn = 0

pygame.init()

SQUARE_SIZE = 100

width = COLUMN_COUNT * SQUARE_SIZE
height = (ROW_COUNT + 1) * SQUARE_SIZE

size = (width, height)

RADIUS = int(SQUARE_SIZE/2 - 5)

screen = pygame.display.set_mode(size)
draw_board(game_board)
pygame.display.update()

my_font = pygame.font.SysFont("monospace", 75)

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARE_SIZE))
            posx = event.pos[0]
            if turn == 0:
                color = RED
            else:
                color = YELLOW
            pygame.draw.circle(screen, color,
                               (posx, int(SQUARE_SIZE/2)), RADIUS)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
            # Ask for Player 1 input
            if turn == 0:
                posx = event.pos[0]
                col = posx // SQUARE_SIZE

                if is_valid_location(game_board, col):
                    row = get_next_open_row(game_board, col)
                    drop_piece(game_board, row, col, 1)

                    if winning_move(game_board, 1):
                        label = my_font.render("Player 1 wins!!", 1, RED)
                        screen.blit(label, (40, 10))
                        game_over = True

            # Ask for Player 2 input
            else:
                posx = event.pos[0]
                col = posx // SQUARE_SIZE

                if is_valid_location(game_board, col):
                    row = get_next_open_row(game_board, col)
                    drop_piece(game_board, row, col, 2)

                    if winning_move(game_board, 2):
                        label = my_font.render("Player 2 wins!!", 1, YELLOW)
                        screen.blit(label, (40, 10))
                        game_over = True

            draw_board(game_board)
            turn += 1
            turn = turn % 2

            # if game_over:
            #     pygame.time.wait(3000)

# pygame.time.wait(3000)
