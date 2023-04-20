import pygame
from constants import CROWN, PIECE_1, PIECE_2, SQUARE_SIZE

class Piece:
    def __init__(self, team):
        self.team = team
        self.image = PIECE_1 if self.team == 1 else PIECE_2
        self.is_king = False

    def draw(self, row, col, screen):
        x = SQUARE_SIZE * col + SQUARE_SIZE // 2
        y = SQUARE_SIZE * row + SQUARE_SIZE // 2
        screen.blit(self.image, (x - self.image.get_width() // 2, y - self.image.get_height() // 2))
        if self.is_king:
            screen.blit(CROWN, (x - CROWN.get_width() // 2, y - CROWN.get_height() // 2))
