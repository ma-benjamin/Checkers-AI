import pygame
from game import Game

def main():
    pygame.init()
    game = Game()
    game.initial_setup()

    run = True
    # Game loop
    while run:

        if game.turn == 1:
            game.players_move()
            game.update()
            
        else:
            game.players_move()
            game.update()

        if game.is_finished:
            run = False

    pygame.quit()

main()
