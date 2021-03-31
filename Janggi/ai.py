from .board import *
from .piece import Piece
import random


class Ai:
    def __init__(self):
        self._ai_player_turn = "RED"
        self._ai_pieces = []
        self._ai_moves = {}

    def get_ai_moves(self):
        return self._ai_moves

    def set_ai_moves(self, new_moves):
        self._ai_moves = new_moves

    def get_ai_pieces(self):
        return self._ai_pieces

    def set_ai_pieces(self, new_pieces):
        self._ai_pieces = new_pieces

    def get_ai_player_turn(self):
        return self._ai_player_turn

    def ai_move(self):
        random_piece_move_list = []
        board = Board()
        ai_piece_list = []
        for piece in Board.get_pieces(board):
            if piece.get_player() == self.get_ai_player_turn()[0].lower():
                ai_piece_list.append(piece)
        self.set_ai_pieces(ai_piece_list)

        # Get ai moves
        ai_moves = Board.get_opposing_player_moves(board, Board.get_moves(board), Board.get_player_turn(board))
        self.set_ai_moves(ai_moves)

        # Get Random piece
        random_int_for_piece = random.randint(0, len(self.get_ai_pieces()) - 1)
        random_piece = self.get_ai_pieces()[random_int_for_piece]

        # Get random move from random_piece
        random_piece_move_list_empty = True
        while random_piece_move_list_empty:
            print(random_piece.get_move_key())

            random_piece_move_list = self.get_ai_moves()[random_piece.get_move_key()]
            if not random_piece_move_list:
                random_int_for_piece = random.randint(0, len(self.get_ai_pieces()) - 1)
                random_piece = self.get_ai_pieces()[random_int_for_piece]
                continue
            elif random_piece_move_list:
                random_piece_move_list_empty = False
        random_int_for_move = random.randint(0, len(random_piece_move_list) - 1)
        random_move = random_piece_move_list[random_int_for_move]
        print(random_move)
        rand_row, rand_col = random_move[0], random_move[1]

        return random_piece, rand_row, rand_col

