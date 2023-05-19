import pygame
from constants import *

class Graphics:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIN_HEIGHT, WIN_WIDTH))

    def setup(self, Board, possible_moves):
        pygame.display.set_caption(CAPTION)
        self.draw_all(Board, possible_moves)

    def draw_board(self):
        self.screen.fill(BG_COLOR)
        for row in range(NUM_ROWS):
            for col in range(NUM_COLS):
                if (row + col) % 2 == 1:
                    pygame.draw.rect(self.screen, BG_COLOR_ALT, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                
    def draw_pieces(self, Board):
        for row in range(NUM_ROWS):
            for col in range(NUM_COLS):
                square = Board.board[row][col]
                if square: 
                    x = SQUARE_SIZE * col + SQUARE_SIZE // 2
                    y = SQUARE_SIZE * row + SQUARE_SIZE // 2
                    if square > 0:
                        self.screen.blit(PIECE_1, (x - PIECE_1.get_width() // 2, y - PIECE_1.get_height() // 2))
                    else: 
                        self.screen.blit(PIECE_2, (x - PIECE_2.get_width() // 2, y - PIECE_2.get_height() // 2))
                    if abs(square) == 2:
                        self.screen.blit(CROWN, (x - CROWN.get_width() // 2, y - CROWN.get_height() // 2))

    ## SHAMELESSLY COPIED FROM TIM ##
    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.screen, BLACK, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 15)

    def draw_all(self, Board, possible_moves):
        self.draw_board()
        self.draw_pieces(Board)
        self.draw_valid_moves(possible_moves)
        pygame.display.update()
        self.clock.tick(FPS)
        