from constants import NUM_ROWS, NUM_COLS, RED, WHITE
import random as rd

class Board:
    def __init__(self):
        self.board = self.new_board()      
        self.team_1_pieces = self.team_2_pieces = 12
        self.team_1_kings = self.team_2_kings = 0

    def new_board(self):   ## 2D array of pieces ##
        new_board = []
        for row in range(NUM_ROWS):
            new_row = []
            for col in range(NUM_COLS):
                if ((row + col) % 2 == 0 or row == 3 or row == 4):
                    new_row.append(0)
                elif (row < 3):
                    new_row.append(WHITE)
                else:
                    new_row.append(RED)
            new_board.append(new_row)
        return new_board
    
    def get_possible_moves(self, row, col, team, is_king):
        possible_moves = {}

        steps = self.get_steps(row, col, team, is_king)
        possible_moves.update(steps)
        jumps = self.get_jumps(row, col, [], team, is_king)
        possible_moves.update(jumps)

        return possible_moves
    
    def get_steps(self, row, col, team, is_king):
        steps = {}

        # check for steps going up one row
        if row != 0 and (team == RED or is_king):
            if col - 1 >= 0 and self.board[row - 1][col - 1] == 0:
                steps.update({(row - 1, col - 1): []})
            if col + 1 < 8 and self.board[row - 1][col + 1] == 0:
                steps.update({(row - 1, col + 1): []})

        # check for steps going down one row
        if row != 7 and (team == WHITE or is_king):
            if col - 1 >= 0 and self.board[row + 1][col - 1] == 0:
                steps.update({(row + 1, col - 1): []})
            if col + 1 < 8 and self.board[row + 1][col + 1] == 0:
                steps.update({(row + 1, col + 1): []})

        return steps
    
    def get_jumps(self, row: int, col: int, jumped: list, team: int, is_king: bool) -> dict:
        jumps_dict = {}
        # force terminate if men jumped three times (and no restriction on king)
        if jumped and len(jumped) == 3 and not is_king:
            return jumps_dict

        if row - 2 >= 0 and (team == RED or is_king):
            # top left
            if col - 2 >= 0 and self.board[row - 1][col - 1] and self.board[row - 1][col - 1] * team < 0 and self.board[row - 2][col - 2] == 0 and [row - 1, col - 1] not in jumped:
                new_jumped = jumped + [[row - 1, col - 1]]
                jumps_dict.update({(row - 2, col - 2): new_jumped})
                jumps_dict.update(self.get_jumps(row - 2, col - 2, new_jumped, team, is_king))
            # top right
            if col + 2 <= 7 and self.board[row - 1][col + 1] and self.board[row - 1][col + 1] * team < 0 and self.board[row - 2][col + 2] == 0 and [row - 1, col + 1] not in jumped:
                new_jumped = jumped + [[row - 1, col + 1]]
                jumps_dict.update({(row - 2, col + 2): new_jumped})
                jumps_dict.update(self.get_jumps(row - 2, col + 2, new_jumped, team, is_king))

        if row + 2 <= 7 and (team == WHITE or is_king):
            # bottom left
            if col - 2 >= 0 and self.board[row + 1][col - 1] and self.board[row + 1][col - 1] * team < 0 and self.board[row + 2][col - 2] == 0 and [row + 1, col - 1] not in jumped:
                new_jumped = jumped + [[row + 1, col - 1]]
                jumps_dict.update({(row + 2, col - 2): new_jumped})
                jumps_dict.update(self.get_jumps(row + 2, col - 2, new_jumped, team, is_king))
            # bottom right
            if col + 2 <= 7 and self.board[row + 1][col + 1] and self.board[row + 1][col + 1] * team < 0 and self.board[row + 2][col + 2] == 0 and [row + 1, col + 1] not in jumped:
                new_jumped = jumped + [[row + 1, col + 1]]
                jumps_dict.update({(row + 2, col + 2): new_jumped})
                jumps_dict.update(self.get_jumps(row + 2, col + 2, new_jumped, team, is_king))
        
        return jumps_dict
    
    def remove_positions(self, removals, turn):
        for [row, col] in removals:
            if turn == RED:
                self.team_2_pieces -= 1
                if abs(self.board[row][col]) == 2:
                    self.team_2_kings -= 1
            else:
                self.team_1_pieces -= 1
                if abs(self.board[row][col]) == 2:
                    self.team_1_kings -= 1
              
            self.board[row][col] = 0

    def winner(self, team):
        ## if out of pieces
        if self.team_1_pieces <= 0:
            return WHITE
        if self.team_2_pieces <= 0:
            return RED
        
        ## if no more moves
        for row in range(NUM_ROWS):
            for col in range(NUM_COLS):
                if self.board[row][col] and self.board[row][col] * team > 0:
                    if self.get_possible_moves(row, col, team, abs(self.board[row][col]) == 2):
                        return 0

        return WHITE if team == RED else RED

    def compress_board(self):
        rtn = []
        for row in range(NUM_ROWS):
            for col in range(NUM_COLS):
                if (row + col) % 2 == 1:
                    rtn.append(self.board[row][col])
        rtn.reverse()
        return rtn

    # def generate_next(self):
    #     all_moves = get_all_moves():
    #     idx = rd.randint(0, len(all_moves) - 1)
    #     from_row, from_col = all_moves[idx][0]
    #     to_row, to_col = all_moves[idx][2]
    #     self.board[to_row][to_col] = self.board[from_row][from_col]

    #     # not sure if this needs to be implemented?
    #     # check if became king
    #     # if (to_row == 0 or to_row == 7) and self.board[to_row][to_col].is_king == False:
    #     #     self.board[to_row][to_col].is_king = True
    #     #     if self.turn == 1:
    #     #         self.Board.team_1_kings += 1
    #     #     else:
    #     #         self.Board.team_2_kings += 1

    #     # clear original position
    #     self.board[from_row][from_col] = 0

    #     # remove skipped pieces
    #     if self.possible_moves[(to_row, to_col)]:
    #         self.Board.remove_positions(self.possible_moves[(to_row, to_col)], self.turn)
    
    
########################
# Feature calculations #
########################

    def get_piece_margin(self, turn):
        return (self.team_1_pieces - self.team_2_pieces) if turn == 1 else (self.team_2_pieces - self.team_1_pieces)

    def get_king_margin(self, turn):
        return (self.team_1_kings - self.team_2_kings) if turn == 1 else (self.team_2_kings - self.team_1_kings)

    def get_jump_lengths(self, turn):
        single_jumps = []
        double_jumps = []
        triple_jumps = []

        for row in range(NUM_ROWS):
            for col in range(NUM_COLS):
                if self.board[row][col] and self.board[row][col] * turn > 0:
                    all_jumps = self.get_jumps(row, col, [], turn, abs(self.board[row][col]) == 2)

                    # loop through all moves and add to the respective lists
                    for key, value in all_jumps.items():
                        if len(value) == 1:
                            single_jumps.append(key)
                        elif len(value) == 2:
                            double_jumps.append(key)
                        elif len(value) >= 3:
                            triple_jumps.append(key)

        return single_jumps, double_jumps, triple_jumps

    def get_pieces_in_enemy_half(self, turn):
        count = 0
        start = 0 if turn == 1 else NUM_ROWS // 2
        end = NUM_ROWS // 2 if turn == 1 else NUM_ROWS

        for row in range(start, end):
                for col in range(NUM_COLS):
                    if self.board[row][col] and self.board[row][col] * turn > 0:
                        count += 1

        return count
    