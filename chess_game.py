""" practice my skills

    Chess game!
"""

import numpy as np
import sys


def setup_board():
    """ sets up a fresh game for chess """

    board = np.array([['███'] * 8] * 8)
    board[1] = ['WP{}'.format(num) for num in range(8)]  # white pawns
    board[-2] = ['BP{}'.format(num) for num in range(8)]  # black pawns
    board[0][0], board[0, -1] = 'WR0', 'WR1'  # white rooks
    board[-1][0], board[-1, -1] = 'BR0', 'BR1'  # black rooks
    board[0][1], board[0][-2] = 'WK0', 'WK1'  # white knights
    board[-1][1], board[-1][-2] = 'BK0', 'BK1'  # black knights
    board[0][2], board[0][-3] = 'WB0', 'WB1'  # white bishops
    board[-1][2], board[-1][-3] = 'BB0', 'BB1'  # black bishops
    board[0][3], board[0][-4] = 'WQN', 'WKN'  # white king/queen
    board[-1][3], board[-1][-4] = 'BKN', 'BQN'  # black queen/king

    return board


chess_board = setup_board()


class Piece:
    def __init__(self, piece, jump=False):
        global chess_board
        self.map = chess_board
        self.piece = piece
        self.jump = jump

    def right(self):
        x, y = self.location()
        self.map[y][x] = '███'
        try:
            if self.map[y][x + 1][0] == self.piece[0]:
                if not self.jump:
                    return False
                else:
                    self.map[y][x + 1] = self.piece
                    return self.map[y][x + 1]
            self.map[y][x + 1] = self.piece

        except IndexError:
            self.map[y][x] = self.piece

    def left(self):
        x, y = self.location()
        self.map[y][x] = '███'
        try:
            if self.map[y][x - 1][0] == self.piece[0]:
                if not self.jump:
                    return False
                else:
                    self.map[y][x - 1] = self.piece
                    return self.map[y][x - 1]
            self.map[y][x - 1] = self.piece
        except IndexError:
            self.map[y][x] = self.piece

    def up(self):
        x, y = self.location()
        self.map[y][x] = '███'
        try:
            self.map[y - 1][x] = self.piece
        except IndexError:
            self.map[y][x] = self.piece

    def down(self):
        x, y = self.location()
        self.map[y][x] = '███'
        try:
            self.map[y + 1][x] = self.piece
        except IndexError:
            self.map[y][x] = self.piece

    def location(self):
        try:
            y = next((c for c, line in enumerate(self.map) if self.piece in line))
            x = next((c for c, n in enumerate(self.map[y]) if n == self.piece))
            return x, y
        except StopIteration:
            pass

    def show_map(self):
        print(self.map)


BQN = Piece('BQN')
BP0 = Piece('BP0')

BQN.up()
BQN.right()
BP0.up()
BQN.up()


BQN.show_map()
