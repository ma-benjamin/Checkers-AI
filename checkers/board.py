import pygame
from .constants import BLACK, ROWS, RED, SQUARE_SIZE, COLS, WHITE, GREY
from .piece import Piece


class Board:
    def __init__(self):
        self.board = []
        self.red_left = self.white_left = 12
        self.red_kings = self.white_kings = 0
        self.create_board()

    def draw_squares(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, RED, (row*SQUARE_SIZE,
                                 col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == ROWS - 1 or row == 0:
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.red_kings += 1

    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, RED))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == RED:
                    self.red_left -= 1
                else:
                    self.white_left -= 1

    def winner(self):
        if self.red_left <= 0:
            return WHITE
        elif self.white_left <= 0:
            return RED

        return None

    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == RED or piece.king:
            moves.update(self._traverse_left(
                row - 1, max(row-3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(
                row - 1, max(row-3, -1), -1, piece.color, right))
        if piece.color == WHITE or piece.king:
            moves.update(self._traverse_left(
                row + 1, min(row+3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(
                row + 1, min(row+3, ROWS), 1, piece.color, right))

        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break

            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last

                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(
                        r+step, row, step, color, left-1, skipped=last+skipped))
                    moves.update(self._traverse_right(
                        r+step, row, step, color, left+1, skipped=last+skipped))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1

        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break

            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last

                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(
                        r+step, row, step, color, right-1, skipped=last+skipped))
                    moves.update(self._traverse_right(
                        r+step, row, step, color, right+1, skipped=last+skipped))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1

        return moves

    # functions to get features
    def get_piece_margin(self, turn):
        if turn == WHITE:
            return self.white_left - self.red_left
        else:
            return self.red_left - self.white_left

    def get_king_margin(self, turn):
        if turn == WHITE:
            return self.white_kings - self.red_kings
        else:
            return self.red_kings - self.white_kings

    def filter_jumps(self, pair):
        key, value = pair
        if len(value) == 1:
            return True
        else:
            return False

    def filter_double_jumps(self, pair):
        key, value = pair
        if len(value) == 2:
            return True
        else:
            return False
        
    def filter_triple_jumps(self, pair):
        key, value = pair
        if len(value) == 3:
            return True
        else:
            return False

    def get_jumps(self, turn):
        all_moves = {}
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if (piece != 0 and piece.color == turn):
                    all_moves.update(self.get_valid_moves(piece))
        print("All moves: " + str(all_moves))

        filtered_moves = dict(filter(self.filter_jumps, all_moves.items()))
        single_jumps = len(filtered_moves)

        filtered_double_jumps = dict(
            filter(self.filter_double_jumps, all_moves.items()))
        double_jumps = len(filtered_double_jumps)

        filtered_triple_jumps = dict(
            filter(self.filter_triple_jumps, all_moves.items()))
        triple_jumps = len(filtered_triple_jumps)

        print(" -> single moves: " + str(filtered_moves))
        print(" -> double moves: " + str(filtered_double_jumps))
        print(" -> triple moves: " + str(filtered_triple_jumps))

        return single_jumps, double_jumps, triple_jumps
    
    def get_enemy_half_pieces(self, turn):
        count = 0
        if turn == RED:
            for row in range(0, 4):
                for col in range(COLS):
                    piece = self.board[row][col]
                    if (piece != 0 and piece.color == turn):
                        count += 1
            return count
        else:
            for row in range(4, 8):
                for col in range(COLS):
                    piece = self.board[row][col]
                    if (piece != 0 and piece.color == turn):
                        count += 1
            return count