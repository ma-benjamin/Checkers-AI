import pygame
from .constants import RED, WHITE, GREY, SQUARE_SIZE, CROWN, FONT

class Piece:
  PADDING = 15
  OUTLINE = 2
  ID = 1

  def __init__(self, row, col, color):
    self.row = row
    self.col = col
    self.color = color
    self.king = False
    self.x = 0
    self.y = 0
    self.calc_pos()
    self.id = self.ID
    Piece.ID += 1

  def calc_pos(self):
    self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
    self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

  def make_king(self):
    self.king = True

  def draw(self, win):
    radius = SQUARE_SIZE//2 - self.PADDING
    pygame.draw.circle(win, GREY, (self.x, self.y), radius + self.OUTLINE)
    pygame.draw.circle(win, self.color, (self.x, self.y), radius)
    if self.king:
      win.blit(CROWN, (self.x - CROWN.get_width()//2, self.y - CROWN.get_height()//2))

    text = FONT.render(str(self.id), True, RED, GREY)
    textRect = text.get_rect()
    textRect.center = (self.x, self.y)
    win.blit(text, textRect)


  def move(self, row, col):
    self.row = row
    self.col = col
    self.calc_pos()

  def __repr__(self):
    return str(self.color)

