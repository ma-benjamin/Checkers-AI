import pygame
from graphics import Graphics
from board import Board
from constants import SQUARE_SIZE, NUM_ROWS, NUM_COLS

class Game:
    def __init__(self):
        self.Graphics: Graphics = Graphics()
        self.Board: Board = Board()
        self.turn: int = 1           # only 1 or 2
        self.total_turns: int = 1           # up to 65
        self.is_finished: bool = False
        self.selected_piece: set = None   # (row, col)
        self.possible_moves: dict = {}    # dictionary of moves

    def initial_setup(self):
        self.Graphics.setup(self.Board, self.possible_moves)

    def players_move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit_game()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                row, col = y // SQUARE_SIZE, x // SQUARE_SIZE
                self.select_square(row, col)

                # self.print_data() # TO BE DELETED

    def select_square(self, row, col):
        ## check if is in allowed moves -> move the piece
        if (row, col) in self.possible_moves:
            self.move_piece(row, col)
            self.change_turn()
            return
        
        ## check if team piece was selected
        if self.Board.board[row][col] and self.Board.board[row][col].team == self.turn:
            self.selected_piece = (row, col)
            self.possible_moves = self.Board.get_possible_moves(row, col, self.turn, self.Board.board[row][col].is_king)
            return

        ## otherwise, empty square/enemy piece was selected
        self.selected_piece = None
        self.possible_moves = {}

    def move_piece(self, to_row, to_col):
        # set the new position
        self.Board.board[to_row][to_col] = self.Board.board[self.selected_piece[0]][self.selected_piece[1]]

        # check if became king
        if (to_row == 0 or to_row == 7) and self.Board.board[to_row][to_col].is_king == False:
            self.Board.board[to_row][to_col].is_king = True
            if self.turn == 1:
                self.Board.team_1_kings += 1
            else:
                self.Board.team_2_kings += 1

        # clear original position
        self.Board.board[self.selected_piece[0]][self.selected_piece[1]] = None

        # remove skipped pieces
        if self.possible_moves[(to_row, to_col)]:
            self.Board.remove_positions(self.possible_moves[(to_row, to_col)], self.turn)
    
    def update(self):
        self.Graphics.draw_all(self.Board, self.possible_moves)

    def change_turn(self):
        if self.turn == 1:
            self.turn = 2
        else:
            self.turn = 1
            self.total_turns += 1
        
        self.selected_piece = None
        self.possible_moves = {}

        self.display_score()
        if self.check_winner(self.turn):
            return
        self.check_draw()

    def check_winner(self, team):
        winner = self.Board.winner(team)
        if winner:
            if winner == 1:
                print("Team 1 won!")
            else:
                print("Team 2 won!")
            self.exit_game()
            return True
        return False
            
    def check_draw(self):
        if self.is_draw():
            print("\nDraw")
            self.exit_game()

    def is_draw(self):
        ## if turn count passed 65
        if self.total_turns >= 65:
            return True
        
        ## if no more moves (ACTUALLY A WIN CONDITION, TO BE CHANGED)
        for row in range(NUM_ROWS):
            for col in range(NUM_COLS):
                if self.Board.board[row][col] and self.Board.board[row][col].team == self.turn:
                    if self.Board.get_possible_moves(row, col, self.turn, self.Board.board[row][col].is_king):
                        return False
        
        return True

    # def print_data(self):
    #     print('SELECTED PIECE: ' + str(self.selected_piece))
    #     print('POSSIBLE MOVES: ' + str(self.possible_moves))

    def display_score(self):
        print('-----------------------')
        print("TURN " + str(self.total_turns) + ": TEAM " + str(self.turn) + " (SCORE: " + str(self.get_score()) + ")")
        print('-----------------------')
        print('DIFF IN PIECES: ' + str(self.Board.get_piece_margin(self.turn)))
        print('DIFF IN KINGS: ' + str(self.Board.get_king_margin(self.turn)))
        single_jumps, double_jumps, triple_jumps = self.Board.get_jump_lengths(self.turn)
        print('SINGLE JUMPS AVAILABLE: ' + str(single_jumps))
        print('DOUBLE JUMPS AVAILABLE: ' + str(double_jumps))
        print('TRIPLE JUMPS AVAILABLE: ' + str(triple_jumps))
        print('PIECES IN ENEMY HALF: ' + str(self.Board.get_pieces_in_enemy_half(self.turn)))

    def get_score(self):
        single_jumps, double_jumps, triple_jumps = self.Board.get_jump_lengths(self.turn)
        return (2 * self.Board.get_piece_margin(self.turn) + 5 * self.Board.get_king_margin(self.turn) + 2 * (len(single_jumps) > 0) +
            4 * (len(double_jumps) > 0) + 6 * (len(triple_jumps) > 0) + 2 * self.Board.get_pieces_in_enemy_half(self.turn) + 100 * (self.Board.winner(self.turn) == (2 if self.turn == 1 else 1)) + 25 * (self.is_draw()))

    ## Fix exit game
    def exit_game(self):
        self.is_finished = True
