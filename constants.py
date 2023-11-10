import pygame

## GAME CONSTANTS ##

# is init needed??
pygame.init()
CAPTION = 'Checkers'
FPS = 60
WIN_WIDTH, WIN_HEIGHT = 800, 800
NUM_ROWS, NUM_COLS = 8, 8
SQUARE_SIZE = WIN_WIDTH // NUM_ROWS
PIECE_PADDING = 15

RED = 1
WHITE = -1

FONT = pygame.font.Font('freesansbold.ttf', 32)
CROWN = pygame.transform.scale(pygame.image.load('imgs/crown.png'), (44, 25)) # to change
PIECE_1 = pygame.transform.scale(pygame.image.load('imgs/red_piece.png'), 
                                (SQUARE_SIZE - PIECE_PADDING, SQUARE_SIZE - PIECE_PADDING)) # to change
PIECE_2 = pygame.transform.scale(pygame.image.load('imgs/white_piece.png'), 
                                (SQUARE_SIZE - PIECE_PADDING, SQUARE_SIZE - PIECE_PADDING)) # to change



## COLORS(R, G, B) ##

COLOR_1      = (255,  36,   0)  # Red // unneeded
COLOR_2      = (255, 255, 255)  # White // unneeded
BG_COLOR     = (250, 240, 230)  # Beige
BG_COLOR_ALT = (  0, 168, 107)  # Jade
BLACK        = (  0,   0,   0)
