import pygame
from .constants import RED, WHITE, BLUE, SQUARE_SIZE
from .board import Board

class Game:
  def __init__(self, win):
    self._init()
    self.win = win
  
  def _init(self):
    self.selected = None
    self.board = Board()
    self.turnCount = 1
    self.turn = RED
    self.valid_moves = {}

  def update(self):
    self.board.draw(self.win)
    self.draw_valid_moves(self.valid_moves)
    pygame.display.update()

  def display_score(self):
    player = "RED" if self.turn == RED else "WHITE"
    print('-----------------------')
    print("TURN " + str(self.turnCount) + ": " + player + " (SCORE: " + str(self.get_score()) + ")")
    print('-----------------------')
    print('DIFF IN PIECES: ' + str(self.board.get_piece_margin(self.turn)))
    print('DIFF IN KINGS: ' + str(self.board.get_king_margin(self.turn)))
    single_jumps, double_jumps, triple_jumps = self.board.get_jumps(self.turn)
    print('SINGLE JUMPS AVAILABLE: ' + str(single_jumps))
    print('DOUBLE JUMPS AVAILABLE: ' + str(double_jumps))
    print('TRIPLE JUMPS AVAILABLE: ' + str(triple_jumps))
    print('PIECES IN ENEMY HALF: ' + str(self.board.get_enemy_half_pieces(self.turn)))

  def get_score(self):
    single_jumps, double_jumps, triple_jumps = self.board.get_jumps(self.turn)
    return (2 * self.board.get_piece_margin(self.turn) + 5 * self.board.get_king_margin(self.turn) + 2 * (single_jumps > 0) +
            4 * (double_jumps > 0) + 6 * (triple_jumps > 0) + 2 * self.board.get_enemy_half_pieces(self.turn) + 100 * (self.winner() == self.turn) + 25 * (self.isDraw()))

  def winner(self):
    return self.board.winner()

  def isDraw(self):
    if self.turnCount > 65:
      print("Game is a draw - 65 moves have passed!")
      return True
    return False

  def reset(self):
    self._init()

  def select(self, row, col):
    if self.selected:
      result = self._move(row, col)
      if not result:
        self.selected = None
        self.select(row, col)
      
    piece = self.board.get_piece(row, col)
    if piece != 0 and piece.color == self.turn:
      self.selected = piece
      self.valid_moves = self.board.get_valid_moves(piece)
      return True
        
    return False

  def _move(self, row, col):
    piece = self.board.get_piece(row, col)
    if self.selected and piece == 0 and (row, col) in self.valid_moves:
      self.board.move(self.selected, row, col)
      skipped = self.valid_moves[(row, col)]
      if skipped:
        self.board.remove(skipped)
      self.change_turn()
    else:
        return False

    return True

  def draw_valid_moves(self, moves):
    for move in moves:
      row, col = move
      pygame.draw.circle(self.win, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 15)

  def change_turn(self):
    self.valid_moves = {}
    if self.turn == RED:
      self.turn = WHITE
    else:
      self.turn = RED
      self.turnCount += 1
    self.display_score()
