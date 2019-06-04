""" practice my skills

    Chess game!
"""

import numpy as np
import sys
import time
import os


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


class Piece:
    def __init__(self, piece=False):
        global chess_board
        global taken_pieces
        self.map = chess_board
        self.piece = piece
        self.times_moved = 0
        if piece:
            self.take_dir = 'on_land' if self.piece[1] != 'P' else 'on_d'
            self.opponent = 'B' if self.piece[0] == 'W' else 'W'

    def move(self, x_m, y_m):
        x, y = self.location()
        if x + x_m < 0 or y + y_m < 0:
            return False
        try:
            if x_m and y_m and self.piece[1] not in ['P', 'B', 'K', 'Q']:  # if the piece is trying to move on a slant
                #                                                            it must be one of these pieces.
                return False
            elif self.piece[1] == 'P':  # Pawn conditions
                if x_m > 1:  # if the pawn is trying to move right more than 1 square somethings up...
                    return False
                elif self.times_moved and y_m > 1:  # if it's not the first move and it's trying to move two squares
                    #                                 return False
                    return False
                elif not self.times_moved and y_m > 2 and x_m:  # if it is the first move, it can't move two squares and
                    #                                             to the right or left, so return False
                    return False

                # taking a piece
                if self.map[y + y_m][x + x_m][0] != self.opponent:
                    if x_m:
                        return False
                    self.map[y + y_m][x] = self.piece
                    self.map[y][x] = '███'
                    return True
                else:
                    if not y_m or not x_m:
                        return False
                    else:
                        taken_pieces[self.opponent].append(self.map[y + y_m][x + x_m])
                        self.map[y + y_m][x + x_m] = self.piece
                        self.map[y][x] = '███'
                        return True
            elif self.piece[1] == 'K':  # Knight conditions
                if abs(x_m) == 2 and abs(y_m) == 1 or abs(y_m) == 2 and abs(x_m) == 1:
                    if self.map[y + y_m][x + x_m] == '███':
                        self.map[y + y_m][x + x_m] = self.piece
                        self.map[y][x] = '███'
                        return True
                    elif self.map[y + y_m][x + x_m][0] == self.piece[0]:
                        return False
                    elif self.map[y + y_m][x + x_m][0] == self.opponent:
                        taken_pieces[self.opponent].append(self.map[y + y_m][x + x_m])
                        self.map[y + y_m][x + x_m] = self.piece
                        self.map[y][x] = '███'
                        return True
                else:
                    return False
            elif self.piece[1] == 'R':  # conditions for a rook
                if abs(x_m + x) > 8 or abs(y_m + y) > 8:
                    return False
                move = x_m if x_m else y_m
                _dir = -1 if move < 0 else 1
                for mv in range(abs(move)+1):
                    if x_m:
                        if self.map[y][x + ((mv + 1)*_dir)][0] == self.piece[0]:
                            add = 1 if _dir < 0 else -1
                            self.map[y][x + ((mv + 1)*_dir + add)] = self.piece
                            self.map[y][x] = '███'
                            if mv == 0:
                                return False
                            return True
                        elif self.map[y][x + (mv + 1)*_dir] == '███':
                            self.map[y][x + (mv + 1)*_dir] = self.piece
                            self.map[y][x + mv * _dir] = '███'
                        elif self.map[y][x + (mv + 1)*_dir][0] == self.opponent:
                            taken_pieces[self.opponent].append(self.map[y][x + (mv + 1)*_dir])
                            self.map[y][x + (mv + 1)*_dir] = self.piece
                            self.map[y][x + mv*_dir] = '███'
                            return True
                    else:
                        if self.map[y + (mv + 1)*_dir][x][0] == self.piece[0]:
                            self.map[y + (mv*_dir)][x] = self.piece
                            self.map[y][x] = '███'
                            return True
                        elif self.map[y + (mv + 1)*_dir][x] == '███':
                            self.map[y + (mv + 1)*_dir][x] = self.piece
                            self.map[y + mv * _dir][x] = '███'
                        elif self.map[y + (mv + 1)*_dir][x][0] == self.opponent:
                            taken_pieces[self.opponent].append(self.map[y + (mv + 1)*_dir][x])
                            self.map[y + (mv + 1)*_dir][x] = self.piece
                            self.map[y + mv*_dir][x] = '███'
                            return True
                    if abs(move) == 1:
                        return True
                return True

            elif self.piece[1] == 'B':  # conditions for a bishop
                if abs(x_m) != abs(y_m):
                    return False
                else:
                    x_dir = -1 if x_m < 0 else 1
                    y_dir = -1 if y_m < 0 else 1
                    if abs(x_m) == 1 and abs(y_m) == 1:
                        if self.map[y + x_m][x + x_m][0] == self.piece[0]:
                            return False
                    for mv in range(abs(x_m)):
                        if self.piece[0] == self.map[y + (mv + 1)*y_dir][x + (mv + 1)*x_dir][0] == self.piece[0]:
                            self.map[y + mv*y_dir][x + mv*x_dir] = self.piece
                            if not mv:
                                return False
                            return True
                        elif self.map[y + (mv + 1)*y_dir][x + (mv + 1)*x_dir] == '███':
                            self.map[y + (mv + 1) * y_dir][x + (mv + 1) * x_dir] = self.piece
                            self.map[y + mv * y_dir][x + mv * x_dir] = '███'
                        elif self.map[y + (mv + 1)*y_dir][x + (mv + 1)*x_dir][0] == self.opponent:
                            taken_pieces[self.opponent].append(self.map[y + (mv + 1)*y_dir][x + (mv + 1)*x_dir])
                            self.map[y + (mv + 1) * y_dir][x + (mv + 1) * x_dir] = self.piece
                            self.map[y + mv * y_dir][x + mv * x_dir] = '███'
                            return True
                    return True
            elif 'QN' in self.piece:  # conditions for queen
                if x_m and y_m and abs(x_m) != abs(y_m):
                    return False
                elif x_m and y_m:
                    x_dir = -1 if x_m < 0 else 1
                    y_dir = -1 if y_m < 0 else 1
                    for mv in range(abs(x_m)):
                        if self.piece[0] == self.map[y + (mv + 1)*y_dir][x + (mv + 1)*x_dir][0] == self.piece[0]:
                            self.map[y + mv*y_dir][x + mv*x_dir] = self.piece
                            if not mv:
                                return False
                            return True
                        elif self.map[y + (mv + 1)*y_dir][x + (mv + 1)*x_dir] == '███':
                            self.map[y + (mv + 1) * y_dir][x + (mv + 1) * x_dir] = self.piece
                            self.map[y + mv * y_dir][x + mv * x_dir] = '███'
                        elif self.map[y + (mv + 1)*y_dir][x + (mv + 1)*x_dir][0] == self.opponent:
                            taken_pieces[self.opponent].append(self.map[y + (mv + 1)*y_dir][x + (mv + 1)*x_dir])
                            self.map[y + (mv + 1) * y_dir][x + (mv + 1) * x_dir] = self.piece
                            self.map[y + mv * y_dir][x + mv * x_dir] = '███'
                            return True
                    return True
                else:
                    if abs(x_m + x) > 8 or abs(y_m + y) > 8:
                        return False
                    move = x_m if x_m else y_m
                    _dir = -1 if move < 0 else 1
                    for mv in range(abs(move) + 1):
                        if x_m:
                            if self.map[y][x + ((mv + 1) * _dir)][0] == self.piece[0]:
                                add = 1 if _dir < 0 else -1
                                self.map[y][x + ((mv + 1) * _dir + add)] = self.pieceQ
                                self.map[y][x] = '███'
                                return True
                            elif self.map[y][x + (mv + 1) * _dir] == '███':
                                self.map[y][x + (mv + 1) * _dir] = self.piece
                                self.map[y][x + mv * _dir] = '███'
                            elif self.map[y][x + (mv + 1) * _dir][0] == self.opponent:
                                taken_pieces[self.opponent].append(self.map[y][x + (mv + 1) * _dir])
                                self.map[y][x + (mv + 1) * _dir] = self.piece
                                self.map[y][x + mv * _dir] = '███'
                                return True
                        else:
                            if self.map[y + (mv + 1) * _dir][x][0] == self.piece[0]:
                                self.map[y + (mv * _dir)][x] = self.piece
                                self.map[y][x] = '███'
                                return True
                            elif self.map[y + (mv + 1) * _dir][x] == '███':
                                self.map[y + (mv + 1) * _dir][x] = self.piece
                                self.map[y + mv * _dir][x] = '███'
                            elif self.map[y + (mv + 1) * _dir][x][0] == self.opponent:
                                taken_pieces[self.opponent].append(self.map[y + (mv + 1) * _dir][x])
                                self.map[y + (mv + 1) * _dir][x] = self.piece
                                self.map[y + mv * _dir][x] = '███'
                                return True
                    return True
            elif 'KN' in self.piece:  # conditions for king
                if sum(abs(x_m), abs(y_m)) > 2:
                    return False
                elif x_m and y_m and x_m != y_m:
                    return False
                elif x_m and y_m:
                    if self.map[y + y_m][x + x_m][0] == self.opponent:
                        pass

            elif x_m == y_m:
                return False

        except IndexError:
            return False

        self.times_moved += 1

    def in_check(self):
        y = next((c for c, line in enumerate(self.map) if "{}KN".format(self.piece[0]) in line))
        x = next((c for c, n in enumerate(self.map[y]) if n == "{}KN".format(self.piece[0])))

        vuln_diags = [False, False, False, False, False, False, False, False]  # [upper right, upper left, lower right
        #                                                                        lower left, right, left, up, down,
        #                                                                        knight]

        dirs = [[-1, 1], [-1, -1], [1, 1], [1, -1], [0, 1], [0, -1], [1, 0], [-1, 0]]

        for _ in range(len(dirs)):
            y_dir, x_dir = dirs[_]
            for c_row in range(8):
                row = c_row + 1
                try:
                    if y + y_dir < 0 or x + x_dir < 0:
                        break
                    if self.map[y + y_dir * row][x + x_dir * row][0] == self.piece[0]:
                        vuln_diags[_] = False
                        break
                    elif self.map[y + y_dir * row][x + x_dir * row][0] == self.opponent:
                        if _ < 2 and self.map[y + y_dir * row][x + x_dir * row][1] == 'P' and row < 1:
                            vuln_diags[_] = True
                            break
                        if self.map[y + y_dir * row][x + x_dir * row][1] in ['B', 'Q']:
                            vuln_diags[_] = True
                            break
                        else:
                            vuln_diags[_] = False
                            break
                except IndexError:
                    break

        k_dirs = [[-2, 1], [2, 1], [-2, -1], [2, -1], [1, 2], [-1, 2], [1, -2], [-1, -2]]
        for k_dir in k_dirs:
            k_y, k_x = k_dir
            try:
                if y + k_y < 0 or x + k_x < 0:
                    continue
                if "{}K".format(self.opponent) in self.map[y + k_y][x + k_x]:
                    if self.map[y + k_y][x + k_x] == '{}KN'.format(self.opponent):
                        continue
                    else:
                        vuln_diags[-1] = True
                        break
            except IndexError:
                continue

        if any(vuln_diags):
            return True
        else:
            return False

    def location(self):
        try:
            y = next((c for c, line in enumerate(self.map) if self.piece in line))
            x = next((c for c, n in enumerate(self.map[y]) if n == self.piece))
            return x, y
        except StopIteration:
            pass

    def show_map(self):
        print(self.map)
        print('\n')

    def next_move(self):
        self.map = np.flip(self.map, 0)
        global chess_board
        chess_board = self.map


if __name__ == '__main__':
    chess_board = setup_board()
    taken_pieces = {'W': [], 'B': []}
    cur_move = 'W'
    Piece().next_move()
    active_pieces = {'W': {'WP0': Piece('WP0'), 'WP1': Piece('WP1'), 'WP2': Piece('WP2'), 'WP3': Piece('WP3'),
                           'WP4': Piece('WP4'), 'WP5': Piece('WP5'), 'WP6': Piece('WP6'), 'WP7': Piece('WP7'),
                           'WR0': Piece('WR0'), 'WR1': Piece('WR1'), 'WK0': Piece('WK0'), 'WK1': Piece('WK1'),
                           'WB0': Piece('WB0'), 'WB1': Piece('WB1'), 'WQN': Piece('WQN'), 'WKN': Piece('WKN')},
                     'B': {'BP0': Piece('BP0'), 'BP1': Piece('BP1'), 'BP2': Piece('BP2'), 'BP3': Piece('BP3'),
                           'BP4': Piece('BP4'), 'BP5': Piece('BP5'), 'BP6': Piece('BP6'), 'BP7': Piece('BP7'),
                           'BR0': Piece('BR0'), 'BR1': Piece('BR1'), 'BK0': Piece('BK0'), 'BK1': Piece('BK1'),
                           'BB0': Piece('BB0'), 'BB1': Piece('BB1'), 'BQN': Piece('BQN'), 'BKN': Piece('BKN')}}
    while True:
        f_c = 'White' if cur_move == 'W' else 'Black'
        opponent = 'White' if cur_move == 'B' else 'Black'

        print(chess_board)
        print("Taken pieces:", taken_pieces)

        pc = False
        while "{}{}".format(cur_move, pc) not in active_pieces[cur_move].keys():
            pc = input("{}: What piece: ".format(cur_move)).upper()
            if pc == 'QUIT':
                print('{} gives up and {} wins the game.'.format(f_c, opponent))
                quit()

        if "{}{}".format(cur_move, pc) in taken_pieces[cur_move]:
            print('The piece {} has already been taken.'.format(pc))
            continue

        try:
            _x, _y = input("[Distance/Direction X, Distance/Direction Y]: ").replace(' ', '').split(',')
        except ValueError:
            print('Format: x, y   (HELP: -x = right, x = left, -y = down, y = up)')
            continue

        if cur_move == 'B':
            _y = int(_y) * -1

        if not active_pieces[cur_move][cur_move+pc].move(-int(_x), -int(_y)):
            print('Bad move')
            continue

        elif active_pieces[cur_move][cur_move+pc].in_check():
            print('\n{}: You are currently in check, you may only make a move that gets you out of check.'.format(f_c))
            active_pieces[cur_move][cur_move+pc].move(int(_x), int(_y))
            continue
        else:
            print('\n')

        Piece().next_move()

        cur_move = 'W' if cur_move != 'W' else 'B'

