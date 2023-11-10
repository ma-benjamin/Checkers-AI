import game
import board
import random

def select_random_move(game, team):
    all_possible_moves = {}

    b = game.Board.board

    for i in range(0, 8):
        for j in range(0, 8):
            piece = b[i][j]
            if piece * team > 0:
                if abs(piece) > 1:
                    moves = game.Board.get_possible_moves(i, j, team, True)
                    if bool(moves):
                        all_possible_moves[(i,j)] = moves
                else:
                    moves = game.Board.get_possible_moves(i, j, team, False)
                    if bool(moves):
                        all_possible_moves[(i,j)] = moves
                
    print("all moves:")
    print(all_possible_moves.items())

    selected_piece, selected_moves = random.choice(list(all_possible_moves.items()))
    print("selected_piece:" +  str(selected_piece))
    print("selected_moves:" +  str(selected_moves))
    selected_move, pieces_skipped = random.choice(list(selected_moves.items()))
    game.select_square(selected_piece[0],selected_piece[1])
    game.select_square(selected_move[0], selected_move[1])
