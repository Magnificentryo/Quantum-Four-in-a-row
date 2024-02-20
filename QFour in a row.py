# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 18:10:30 2024

@author: Administrator
"""

import numpy as np
import random
import pygame
import sys
import math
from qiskit import QuantumCircuit,Aer , execute
BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
PURPLE = (128,0,128)
ROW_COUNT = 6
COLUMN_COUNT = 7
backend = Aer.get_backend('qasm_simulator')
PLAYER = 0
PLAYER2 = 1

EMPTY = 0
PLAYER_PIECE = 1
PLAYER2_PIECE = 2
i = 1
WINDOW_LENGTH = 4

def create_board():
    board = np.zeros((ROW_COUNT,COLUMN_COUNT))
    return board

def drop_piece(board, row, col, piece):
   
       
   
        
    board[row][col] = piece
    return row,col
def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r
def hga():
    qc = QuantumCircuit(1,1)
    
    qc.h(0)
    qc.measure(0,0)
    oo = 0
    job = execute(qc, backend)
    output = job.result().get_counts()
   
    for key in output:
        oo = key
    print(oo)
    if oo == 0:
        return oo
    else:
        return oo
    
   
    
    
    
def print_board(board):
    print(np.flip(board, 0))

def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check positively sloped diaganols
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check negatively sloped diaganols
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_piece = PLAYER2_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score

def score_position(board, piece):
    score = 0

    ## Score center column
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    ## Score Horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COLUMN_COUNT-3):
            window = row_array[c:c+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    ## Score Vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(ROW_COUNT-3):
            window = col_array[r:r+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    ## Score posiive sloped diagonal
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score

def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, PLAYER2_PIECE) or len(get_valid_locations(board)) == 0


def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations

def pick_best_move(board, piece):

    valid_locations = get_valid_locations(board)
    best_score = -10000
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col

    return best_col

def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
    
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):      
            if board[r][c] == PLAYER_PIECE:
                
                    pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)  
            elif board[r][c] == PLAYER2_PIECE: 
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            
            
    pygame.display.update()

board = create_board()
print_board(board)
game_over = False

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()
FPS = 60
clock = pygame.time.Clock()
myfont = pygame.font.SysFont("monospace", 75)

turn = random.randint(PLAYER, PLAYER2)
s = hga()
print(s)
while not game_over:
   
   for event in pygame.event.get():
    if event.type == pygame.QUIT:
        sys.exit()

    if event.type == pygame.MOUSEMOTION:
        pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
        posx = event.pos[0]
        if turn == PLAYER:
            if(i %3==0 and i > 0 ):
                label = myfont.render("superposition", 1, RED)
                screen.blit(label, (10,5))
                pygame.draw.circle(screen, PURPLE, (posx, int(SQUARESIZE/2)), RADIUS) 
            else:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
        elif turn == PLAYER2:
            if(i %3==0 and i > 0 ):
                label = myfont.render("superposition", 1, YELLOW)
                screen.blit(label, (10,5))
                pygame.draw.circle(screen, PURPLE, (posx, int(SQUARESIZE/2)), RADIUS) 
            else:
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
        
        pygame.display.update()

    if event.type == pygame.MOUSEBUTTONDOWN:
        pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
        posx = event.pos[0]
        col = int(math.floor(posx/SQUARESIZE))

        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
          
            if turn == PLAYER:
                if(i %3==0 and i>0):
                    s = hga()
                    if s == '0':
                        drop_piece(board, row, col, PLAYER2_PIECE)
                    elif s == '1':
                        drop_piece(board, row, col, PLAYER_PIECE)
                else:
                    drop_piece(board, row, col, PLAYER_PIECE)
                if winning_move(board, PLAYER_PIECE):
                    label = myfont.render("You Won", 1, RED)
                    screen.blit(label, (40,10))
                    game_over = True
            elif turn == PLAYER2:
                if(i %3==0 and i>0):
                    s = hga()
                    if s == '0':
                        drop_piece(board, row, col, PLAYER_PIECE)
                    elif s == '1':
                        drop_piece(board, row, col, PLAYER2_PIECE)
                else:
                    drop_piece(board, row, col, PLAYER2_PIECE)
                if winning_move(board, PLAYER2_PIECE):
                    label = myfont.render("You Won", 1, YELLOW)
                    screen.blit(label, (40,10))
                    game_over = True
                
            i +=1
            turn += 1
            turn = turn % 2

            print_board(board)
            draw_board(board)