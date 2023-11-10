import pygame
from game import Game
from constants import RED, WHITE
from random_bot import select_random_move

def main():
    pygame.init()
    game = Game()
    game.initial_setup()

    run = True
    # Game loop
    while run:

        if game.turn == RED:
            game.players_move()
            game.update()
            
        else:
            select_random_move(game, WHITE)
            # game.players_move()
            game.update()

        if game.is_finished:
            run = False

    pygame.quit()

main()
