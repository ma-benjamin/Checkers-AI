import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE
from checkers.game import Game

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')

def get_row_col_from_mouse(pos):
  x,y = pos
  row = y // SQUARE_SIZE
  col = x // SQUARE_SIZE
  return row, col

def main():
  run = True
  clock = pygame.time.Clock()
  game = Game(WIN)

  # Input is formatted as "row_piece col_piece row_next col_next", for example: 5 2 4 1 
  with open('input') as file:
    for line in file:
      piece_pos = line.split(" ")[0:2]
      next_square = line.split(" ")[2: 4]
      game.select(int(piece_pos[0]), int(piece_pos[1]))
      game.select(int(next_square[0]), int(next_square[1]))
      game.update()

  while run:
    clock.tick(FPS)
    
    if game.winner() != None:
      print(game.winner())

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False

      if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        row, col = get_row_col_from_mouse(pos)
        game.select(row, col)


    game.update()
  pygame.quit()
  
main()