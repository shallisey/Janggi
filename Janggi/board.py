import pygame
from .constants import *
from .piece import *


pygame.font.init()
font = pygame.font.SysFont(None, 24)


class Board:
    PADDING = (SQUARE_SIZE) // COLS

    def __init__(self):
        """This will return the JanngiGame class."""
        self.reset()

    def reset(self):
        self._game_state = "UNFINISHED"
        self._player_turn = 'BLUE'  # Blue always starts the game.
        self._pieces = self.new_pieces()
        self._board = self.initial_placements(self.new_board(9, 10), self.get_pieces())
        self._moves = self.possible_moves(self.get_board(), self.get_pieces())
        self._spaceWidth = (WIDTH - PADDING_ON_LEFT - PADDING_ON_TOP) // COLS
        self._spaceHeight = (HEIGHT - PADDING_ON_TOP - PADDING_ON_LEFT) // ROWS
        self._player_in_check = None
        self._selected = None

    def draw_player_turn(self, window):
        if self.get_player_turn() == "BLUE":
            pygame.draw.circle(window, BLUE, (WIDTH - (WIDTH//8), HEIGHT//2), RADIUS+1)
        elif self.get_player_turn() == "RED":
            pygame.draw.circle(window, RED, (WIDTH - (WIDTH//8), HEIGHT//2), RADIUS+1)


    def check(self, window):
        if self.is_in_check('BLUE', window) is True:
            # PLAYER IN CHECK IS BLUE
            if self.check_for_checks(self.get_pieces(), self.get_moves(), self.get_board(),
                                     'b', window) is not False:
                update_moves = self.check_for_checks(self.get_pieces(), self.get_moves(), self.get_board(),
                                                     'b', window)
                # self.swap_player_turn(self.get_player_turn())
                self.set_moves(update_moves)
                return True
            # If this returns false then the player in check has no moves left.
            else:
                self.set_game_state("RED_WON")


        elif self.is_in_check('RED', window) is True:
            # PLAYER IN CHECK IS RED
            if self.check_for_checks(self.get_pieces(), self.get_moves(), self.get_board(),
                                     'r', window) is not False:
                update_moves = self.check_for_checks(self.get_pieces(), self.get_moves(), self.get_board(),
                                                     'r', window)
                # self.swap_player_turn(self.get_player_turn())
                self.set_moves(update_moves)
                return True
            # If this returns false then the player in check has no moves left.
            else:
                self.set_game_state("BLUE_WON")

    def get_opposing_player_moves(self, moves_list, player_in_check):
        """
        This will be called in the check_for_check method

        The moves_list is a list of all the moves for both players.
        The player in check will be whoever is in check.

        The method will grab all the moves for the opposing player, from player_in_check,
        moves and return them to the check_for_check method

        """
        opposing_player_moves = {}

        for move in moves_list:
            if move[0] != player_in_check[0].lower():
                opposing_player_moves[move] = moves_list[move]

        return opposing_player_moves

    def check_for_checks(self, piece_list, moves_list, board, player_in_check, window):
        if player_in_check == 'r':
            self.set_player_in_check('RED')
        else:
            self.set_player_in_check("BLUE")

        check_piece_list = []
        opposing_moves = self.get_opposing_player_moves(moves_list, player_in_check)

        # Grab all pieces of the checked player
        for piece in piece_list:
            if piece.get_player() == player_in_check:
                check_piece_list.append(piece)

        # Store all checked players moves
        check_moves = {}

        # Grab all the moves of each piece from the checked player.
        for piece in check_piece_list:
            current_general_placement = (piece.get_row(), piece.get_col())
            for move in moves_list:
                move_row = int(move[4])
                move_col = int(move[6])
                if move[1:3] == piece.get_piece_display() and move[0] == piece.get_player() and \
                        (move_row, move_col) == current_general_placement:
                    key = str(piece.get_player()) + str(piece.get_piece_display()) + "(" + str(
                        piece.get_row()) + "," + str(piece.get_col()) + ")"
                    check_moves[piece] = moves_list[move]
                    # print(move, general_moves, "move checker")

        check_no_move_count = 0
        # Go through and update pieces move list
        for piece in check_moves:
            remove_list = []
            # Current position of the piece we are checking.
            curr_row = piece.get_row()
            curr_col = piece.get_col()
            key_from = next(iter(board[curr_row][curr_col].keys()))
            display = piece.get_piece_display()
            player_turn = piece.get_player()
            # This will give us where on the board the piece is.
            original_key = str(player_turn) + str(display) + "(" + str(curr_row) + "," + str(curr_col) + ")"
            curr_pos = (curr_row, curr_col)
            key_from = next(iter(board[piece.get_row()][piece.get_col()].keys()))
            for move in check_moves[piece]:
                # Check if we set this move would the general still be in check.
                # Set new coordinates for the move we are attempting
                # piece.set_row(move[0])
                # piece.set_col(move[1])
                attempt_move_pos = (move[0], move[1])
                # This will give us where on the board the piece will go
                key_to = next(iter(board[attempt_move_pos[0]][attempt_move_pos[1]].keys()))
                # Set the player turn to the player that is in check because we are attempting moves.
                self.swap_player_turn(self.get_player_in_check())
                # This will help when reverting move.
                piece_to_put_back = board[attempt_move_pos[0]][attempt_move_pos[1]][key_to]
                # If we come across a general then don't capture it. Go to next loop
                if piece_to_put_back != "    ":
                    if piece_to_put_back.get_piece_type() == 'general':
                        continue
                # Move the piece and update board, moves, and pieces
                self.move_in_check(piece, attempt_move_pos[0], attempt_move_pos[1], window)
                # self.move_piece(original_key, self.get_moves(), curr_pos, attempt_move_pos, key_to, key_from, board)
                self.update_pieces(self.get_board())
                self.update_moves(board, self.get_pieces())

                # If we made the move and player is still in check then remove that move from the move list.
                if self.is_in_check(self.get_player_in_check(), window) is True:
                    board = self.get_board()
                    key = str(player_turn) + str(display) + "(" + str(move[0]) + "," + str(move[1]) + ")"
                    # Reverts move
                    board[curr_row][curr_col][key_from] = board[move[0]][move[1]][key_to]
                    board[move[0]][move[1]][key_to] = piece_to_put_back

                    board[curr_row][curr_col][key_from].set_row(curr_row)
                    board[curr_row][curr_col][key_from].set_col(curr_col)

                    self.update_pieces(self.get_board())
                    self.update_moves(board, self.get_pieces())
                    remove_list.append(move)
                # If we made the move and player is not in check then keep that move from the move list.
                else:
                    key = str(player_turn) + str(display) + "(" + str(move[0]) + "," + str(move[1]) + ")"

                    # Reverts move
                    board[curr_row][curr_col][key_from] = board[move[0]][move[1]][key_to]
                    board[move[0]][move[1]][key_to] = piece_to_put_back

                    board[curr_row][curr_col][key_from].set_row(curr_row)
                    board[curr_row][curr_col][key_from].set_col(curr_col)

                    self.update_pieces(self.get_board())
                    self.update_moves(board, self.get_pieces())

            new_x_coord = (((WIDTH - PADDING_ON_LEFT - PADDING_ON_TOP) // COLS) * piece.get_col()) + PADDING_ON_LEFT

            new_y_coord = (((HEIGHT - PADDING_ON_TOP - PADDING_ON_LEFT) // ROWS) * piece.get_row()) + PADDING_ON_TOP

            piece.set_x_coord(new_x_coord)
            piece.set_y_coord(new_y_coord)

            # This is where we remove moves from the move list.
            for element in remove_list:
                check_moves[piece].remove(element)
            if check_moves[piece] == []:
                check_no_move_count += 1
            # Go through move list and update yourself

        # If there are no moves possible for the checked player then they have lost.
        if check_no_move_count == len(check_moves):
            return False

        all_moves = opposing_moves
        # Add the new updated checked players moves to the all moves dictionary
        for move in check_moves:
            row = move.get_row()
            col = move.get_col()
            display = move.get_piece_display()
            player_turn = move.get_player()
            key = str(player_turn) + str(display) + "(" + str(row) + "," + str(col) + ")"
            all_moves[key] = check_moves[move]

        self.swap_player_turn(self.get_player_turn())
        return all_moves

    def general_location(self, player_general_to_get):
        moves = self.get_moves()
        for piece in self.get_pieces():
            if piece.get_piece_type() == 'general':
                if piece.get_player() == 'r':
                    red_general = piece
                    red_general_location = (red_general.get_row(), red_general.get_col())
                    if player_general_to_get == "RED":
                        return red_general_location
                elif piece.get_player() == 'b':
                    blue_general = piece
                    blue_general_location = (blue_general.get_row(), blue_general.get_col())
                    if player_general_to_get == "BLUE":
                        return blue_general_location
        return None
        # if player_general_to_get == "RED":
        #     return red_general_location
        # elif player_general_to_get == "BLUE":
        #     return blue_general_location

    def is_in_check(self, player_to_check, window):
        """
        This will check if the player_to_check is in check.

        The parameter player_to_check will either be 'red' or 'blue'

        First we get the moves and pieces and go through all of the pieces to
        find the generals for each player and save the locations of the
        generals to their respective variables.

        Then we call the check helper method which will tell us if
        the player_to_check is in check.
        """
        moves = self.get_moves()
        for piece in self.get_pieces():
            if piece.get_piece_type() == 'general':
                if piece.get_player() == 'r':
                    red_general = piece
                elif piece.get_player() == 'b':
                    blue_general = piece
        blue_general_location = (blue_general.get_row(), blue_general.get_col())
        red_general_location = (red_general.get_row(), red_general.get_col())

        # if player_to_check is 'blue'. Search all red moves.
        if player_to_check == 'BLUE':
            if self.check_helper(moves, blue_general_location, player_to_check):
                return True

        # if player_to_check is 'red'. Search all blue moves.
        if player_to_check == 'RED':
            if self.check_helper(moves, red_general_location, player_to_check):
                return True

        return False

    def check_helper(self, moves_list, player_to_check_general_location, player_to_check):
        """
        This will help with the is_in_check method.

        The moves_list parameter is used to find if the player_to_check_general_location
        is any where in the move_list.

        If True, then the player_to_check in the is_in_check method is in fact
        in check.
        """
        for move in moves_list:
            x = moves_list[move]
            if player_to_check == 'BLUE' and move[0] == 'r':
                if player_to_check_general_location in moves_list[move]:
                    # Found a move that could be placed on a general.
                    return True
                else:
                    continue
            elif player_to_check == 'RED' and move[0] == 'b':
                if player_to_check_general_location in moves_list[move]:
                    # Found a move that could be placed on a general.
                    return True
                else:
                    continue
        # General was not in moves list.
        return False

    def get_mouse_on_board_position(self, mouse_position):
        x, y = mouse_position
        col = (x // ((WIDTH - PADDING_ON_LEFT - PADDING_ON_TOP) // COLS)) - 1
        row = (y // ((HEIGHT - PADDING_ON_LEFT - PADDING_ON_TOP) // ROWS)) - 1
        return row, col

    def move_in_move_list(self, row, col, move_list):
        piece = self.get_piece_from_board(row, col)
        move_key = str(piece.get_board_display()) + "(" + str(piece.get_row()) + "," + str(piece.get_col()) + ")"
        if self.get_selected() and (row, col) in move_list:
            print("This is a valid move.")

    def draw_possible_moves(self, piece, list_of_possible_moves, window):
        # If empty
        if not list_of_possible_moves:
            print("Nothing here")
        else:
            for move in list_of_possible_moves:
                row = move[0]
                col = move[1]
                x_coord = (((WIDTH - PADDING_ON_LEFT - PADDING_ON_TOP)//COLS) * col) + PADDING_ON_LEFT
                y_coord = (((HEIGHT - PADDING_ON_TOP - PADDING_ON_LEFT)//ROWS) * row) + PADDING_ON_TOP
                print((x_coord, y_coord))
                pygame.draw.circle(window, POSSIBLE_MOVE, (x_coord, y_coord), 10)

            pygame.display.update()


    def select_piece(self, row, col, window):
        # get piece from row, col
        while not self.get_selected():
            pygame.display.update()
            piece = self.get_piece_from_board(row, col)
            # result = self.move_in_move_list(row, col, moves_for_piece)
            # If selecting an empty space and color == playerturn
            if piece.get_player() == self.get_player_turn()[0].lower():
                print("your piece to move")
                self.set_selected(piece)
                return True
            return False

    def move_places_player_in_check(self, piece, board_position, player_turn, window):
        board = self.get_board()
        curr_row, curr_col = piece.get_row(), piece.get_col()
        key_from = next(iter(board[curr_row][curr_col].keys()))

        row, col = board_position
        print(piece, row, col, player_turn)
        key_to = next(iter(board[row][col].keys()))
        piece_to_put_back = board[row][col][key_to]
        if piece_to_put_back != "    ":
            if piece_to_put_back.get_piece_type() == 'general':
                return False
        self.move_in_check(piece, row, col, window)
        self.set_player_turn(player_turn)
        # get playerturn generals location, and opposing player moves.
        if player_turn == "RED":
            general_location = self.general_location(player_turn)
            opposing_moves = self.get_opposing_player_moves(self.get_moves(), player_turn)
        elif player_turn == "BLUE":
            general_location = self.general_location(player_turn)
            opposing_moves = self.get_opposing_player_moves(self.get_moves(), player_turn)

        # Make the move and the general is in the opposing player moves.
        for move in opposing_moves:
            if general_location in opposing_moves[move]:
                print("SELF CHECK")
                board[curr_row][curr_col][key_from] = board[row][col][key_to]
                board[row][col][key_to] = piece_to_put_back

                board[curr_row][curr_col][key_from].set_row(curr_row)
                board[curr_row][curr_col][key_from].set_col(curr_col)

                self.update_pieces(self.get_board())
                self.update_moves(board, self.get_pieces())
                return True

        print("No Self Check")
        board[curr_row][curr_col][key_from] = board[row][col][key_to]
        board[row][col][key_to] = piece_to_put_back

        board[curr_row][curr_col][key_from].set_row(curr_row)
        board[curr_row][curr_col][key_from].set_col(curr_col)

        self.update_pieces(self.get_board())
        self.update_moves(board, self.get_pieces())
        piece.set_move_key(piece.get_board_display() + "(" + str(piece.get_row()) + "," + str(piece.get_col()) + ")")
        return False



        # REVERT move

    def get_this_piece_moves(self, piece):
        move_key = piece.get_move_key()
        all_moves = self.get_moves()
        if move_key in all_moves:
            piece_moves = all_moves[move_key]
            return piece_moves
        return False


    def piece_is_selected(self, piece, window):
        print("hi")
        moves_for_piece = self.get_this_piece_moves(piece)
        remove_list = []
        for move in moves_for_piece:
            print(move)
            if self.move_places_player_in_check(piece, move, self.get_player_turn(), window):
                print("Uh OH", moves_for_piece, move)

                remove_list.append(move)
                # moves_for_piece.remove(move)
                # self.get_moves()[piece.get_move_key()].remove(move)
                # Remove this move from move list

        for move in remove_list:
            moves_for_piece.remove(move)
            print(piece.get_move_key())
            self.get_moves()[piece.get_move_key()].remove(move)
        while self.get_selected():
            # get possible moves of piece selected

            print("PIECE IS SELECTED")


            self.draw_possible_moves(piece, moves_for_piece, window)
            for event_ in pygame.event.get():
                if event_.type == pygame.MOUSEBUTTONDOWN:
                    new_mouse_pos = pygame.mouse.get_pos()
                    print("new_pos", new_mouse_pos)
                    move_to_row, move_to_col = self.get_mouse_on_board_position(new_mouse_pos)
                    board_position = (move_to_row, move_to_col)
                    print("inside piece_is_selected", moves_for_piece)
                    #TODO
                    # If the possible move puts you in check dont move.
                    # Skipping turn by placing piece in original spot.
                    if board_position == (piece.get_row(), piece.get_col()):
                        if self.is_in_check(self.get_player_turn(), window) is True:
                            print("No skipping if you are in check")
                            self.set_selected(None)
                            # self.swap_player_turn(self.get_player_turn())
                            continue
                        print("SKIP TURN")

                        self.swap_player_turn(self.get_player_turn())
                        self.set_selected(None)
                        continue
                    elif board_position in moves_for_piece:
                        # if self.move_places_player_in_check(piece, board_position,
                        #                                     self.get_player_turn(), window):
                        #     print("CANT MAKE THAT MOVE")
                        #     self.set_selected(None)
                        #     #TODO remove the move that will put the general in check.
                        #     continue
                        self.move(piece, move_to_row, move_to_col, window)
                        self.set_selected(None)
                        # self.swap_player_turn(self.get_player_turn())
                        return True
                        # self.update_pieces(self.get_board())
                        # self.update_moves(self.get_board(), self.get_pieces())

                    else:
                        print("not a valid move")
                        self.set_selected(None)
                        return False



    def swap_player_turn(self, player_to_swap):
        """This will swap players and return true if the are swapped."""
        if player_to_swap == "RED":
            self.set_player_turn("BLUE")
            return True
        elif player_to_swap == "BLUE":
            self.set_player_turn("RED")
            return True
        else:
            # Something went wrong swapping players
            return False


    def cannon_moves(self, key, piece_owned_by, moves, piece_curr_placement, board):
        """
        This method will return the dictionary with all moves for the elephant.

        The key parameter is the key for the dictionary which will have be what is displayed on the
        board. For example rCN(2, 7) is the red players general that is at the 3rd row, 8th column.

        PLayer turn is used to determine if the player moves a piece to a space with a piece that is
        their own piece.

        moves is the current moves dictionary that is being built that will contain all of the moves for
        every move.

        piece_curr_placement is just the current placement of the piece we are trying to find all of the moves for.

        The board parameter is used to find the next possible moves.
        """

        moves[key] = []

        row = piece_curr_placement[0]
        col = piece_curr_placement[1]

        key_key = next(iter(board[row][col].keys()))
        if ('diag_left' in key_key or 'diag_right' in key_key) and 'center_fortress' not in key_key:
            for _row in range(-1, 2):
                for _col in range(-1, 2):
                    if self.map_move_in_bounds((row + _row, col + _col)) is False:
                        continue
                    key_key = next(iter(board[row + _row][col + _col].keys()))
                    if _row == 0 and _col == 0:
                        continue
                    elif (_row == _col or _row == -_col) and "fortress" in key_key and board[row + _row][col + _col][
                        key_key] != "    ":
                        jump_this = (row + _row, col + _col)
                        row = jump_this[0]
                        col = jump_this[1]
                        if self.help_cannon_after_jump((row + _row, col + _col), board, piece_owned_by):
                            successful_jump = self.help_cannon_after_jump((row + _row, col + _col), board,
                                                                          piece_owned_by)
                            if successful_jump not in moves[key]:
                                moves[key].append(successful_jump)
                        else:
                            continue
                    # Piece that is being checked is not in the fortress, so no diagonal jump can be made.
                    else:
                        pass

        moves[key] = self.cannon_helper(piece_curr_placement, board, piece_owned_by, 1, 0, moves[key])
        moves[key] = self.cannon_helper(piece_curr_placement, board, piece_owned_by, -1, 0, moves[key])
        moves[key] = self.cannon_helper(piece_curr_placement, board, piece_owned_by, 0, -1, moves[key])
        moves[key] = self.cannon_helper(piece_curr_placement, board, piece_owned_by, 0, 1, moves[key])

        return moves[key]

    def cannon_helper(self, piece_curr_placement, board, piece_owned_by, _row, _col, list_of_moves):
        """
        This method was created to remove break statements that where in my code.

        This method is called inside the cannon_moves method and returns the possible moves of a cannon
        piece in the direction given.
        """
        row = piece_curr_placement[0]
        col = piece_curr_placement[1]
        jump_found = False

        iterator = 1

        while row in range(10) and col in range(9):
            space = (row + (_row * iterator), col + (_col * iterator))
            # Move is out of range
            if not self.map_move_in_bounds(space):
                return list_of_moves
            key_key = next(iter(board[space[0]][space[1]].keys()))
            if not jump_found:
                # Empty space need continue to find a piece to jump
                if board[row + (_row * iterator)][col + (_col * iterator)][key_key] == "    ":
                    iterator += 1
                    continue
                # A space with a piece is found
                elif board[row + (_row * iterator)][col + (_col * iterator)][key_key] != "    ":
                    # The piece is a cannon no jump can occur for this move.
                    if board[row + (_row * iterator)][col + (_col * iterator)][key_key].get_piece_type() == "cannon":
                        return list_of_moves
                    # The piece is not a cannon. We found a jump.
                    elif board[row + (_row * iterator)][col + (_col * iterator)][key_key].get_piece_type() != "cannon":
                        jump_found = True
                        iterator += 1
            else:
                # An eligible jump has been found
                if self.map_move_in_bounds(space):
                    if self.help_cannon_after_jump(space, board, piece_owned_by) is None:
                        return list_of_moves
                    if self.help_cannon_after_jump(space, board, piece_owned_by) is not None:
                        possible_move = self.help_cannon_after_jump(space, board, piece_owned_by)
                        row_possible_move = possible_move[0]
                        col_possible_move = possible_move[1]
                        key_key = next(iter(board[row_possible_move][col_possible_move].keys()))
                        if board[row_possible_move][col_possible_move][key_key] != "    " and \
                                board[row_possible_move][col_possible_move][key_key].get_player() != piece_owned_by:
                            if possible_move not in list_of_moves:
                                list_of_moves.append(possible_move)
                            return list_of_moves
                        elif board[row_possible_move][col_possible_move][key_key] != "    " and \
                                (board[row_possible_move][col_possible_move][key_key].get_player() == piece_owned_by or
                                 board[row_possible_move][col_possible_move][key_key].get_piece_type() == 'cannon'):
                            return list_of_moves
                        else:
                            if possible_move not in list_of_moves:
                                list_of_moves.append(possible_move)
                                iterator += 1
                            else:
                                iterator += 1

        return list_of_moves

    def help_cannon_after_jump(self, space, board, piece_owned_by):
        """
        The cannon has made a successful jump iver a piece that is not another cannon.
        The next step is to
        """
        row = space[0]
        col = space[1]
        key_key = next(iter(board[row][col].keys()))
        # A Space is an acceptable move.
        # If the next move is out of bounds break. No need to continue
        if self.map_move_in_bounds(space):
            if board[row][col][key_key] == "    ":
                # We can move to this spot.
                return row, col

            # A piece has been found. Check for cannon and piece owner.
            elif board[row][col][key_key] != "    ":
                # The piece is a cannon. You can not capture a cannon.
                if board[row][col][key_key].get_piece_type() == "cannon":
                    return
                # The piece is not a cannon and the piece is owned by the same cannon being moved.
                elif board[row][col][key_key].get_piece_type() != "cannon" and board[row][col][
                    key_key].get_player() == piece_owned_by:
                    # Cant take this spot
                    return row, col
                # The piece is not a cannon and the piece is an enemy piece.
                elif board[row][col][key_key].get_piece_type() != "cannon" and board[row][col][
                    key_key].get_player() != piece_owned_by:
                    # The piece can be taken
                    return row, col
                    # No more moves can be added.

    def map_move_in_bounds(self, possible_move):
        """
        This method will check if a possible move has been made in bounds.
        returns True if a move is in bounds
        returns False if a move has been made out of bounds.
        """
        row = possible_move[0]
        col = possible_move[1]

        if row not in range(0, 10):
            return False
        if col not in range(0, 9):
            return False

        return True

    def elephant_moves(self, key, piece_owned_by, moves, piece_curr_placement, board):
        """
        This method will return the dictionary with all moves for the elephant.

        The key parameter is the key for the dictionary which will have be what is displayed on the
        board. For example bEL(9, 6) is the red players general that is at the 10th row, 6th column.

        PLayer turn is used to determine if the player moves a piece to a space with a piece that is
        their own piece.

        moves is the current moves dictionary that is being built that will contain all of the moves for
        every move.

        piece_curr_placement is just the current placement of the piece we are trying to find all of the moves for.

        The board parameter is used to find the next possible moves.
        """

        row = piece_curr_placement[0]
        col = piece_curr_placement[1]
        moves[key] = []

        # Advance row (row + 1, col) then diagonal (row + 1 + 1, col +- 1) and then again (row + 1 + 1 + 1, col +-1 +- 1)
        # Must be an empty space
        if self.help_horse_move((row + 1, col), board, piece_owned_by) is not None:
            # Must also be an empty space
            # Increment the columns
            if self.helper_elephant((row + 1 + 1, col + 1), board, piece_owned_by) is not None:
                # Can be an empty space, but must also check if it is an opponent piece.
                if self.helper_elephant((row + 1 + 1 + 1, col + 1 + 1), board, piece_owned_by) is not None:
                    key_key = next(iter(board[row + 1 + 1 + 1][col + 1 + 1].keys()))
                    # If we passed the check to get here the next check is if the piece is an opponent piece.
                    if board[row + 1 + 1 + 1][col + 1 + 1][key_key] != "    ":
                        key_key = next(iter(board[row + 1 + 1 + 1][col + 1 + 1].keys()))
                        if board[row + 1 + 1 + 1][col + 1 + 1][key_key].get_player() != piece_owned_by:
                            if (row + 1 + 1 + 1, col + 1 + 1) not in moves[key]:
                                moves[key].append((row + 1 + 1 + 1, col + 1 + 1))
                    # If the second diag is blank it is an acceptable move.
                    else:
                        if (row + 1 + 1 + 1, col + 1 + 1) not in moves[key]:
                            moves[key].append((row + 1 + 1 + 1, col + 1 + 1))
            # Decrement the columns
            if self.helper_elephant((row + 1 + 1, col - 1), board, piece_owned_by) is not None:
                # Can be an empty space, but must also check if it is an opponent piece.
                if self.helper_elephant((row + 1 + 1 + 1, col - 1 - 1), board, piece_owned_by) is not None:
                    key_key = next(iter(board[row + 1 + 1 + 1][col - 1 - 1].keys()))
                    # If we passed the check to get here the next check is if the piece is an opponent piece.
                    if board[row + 1 + 1 + 1][col - 1 - 1][key_key] != "    ":
                        key_key = next(iter(board[row + 1 + 1 + 1][col - 1 - 1].keys()))
                        if board[row + 1 + 1 + 1][col - 1 - 1][key_key].get_player() != piece_owned_by:
                            if (row + 1 + 1 + 1, col - 1 - 1) not in moves[key]:
                                moves[key].append((row + 1 + 1 + 1, col - 1 - 1))
                    # If the second diag is blank it is an acceptable move.
                    else:
                        if (row + 1 + 1 + 1, col - 1 - 1) not in moves[key]:
                            moves[key].append((row + 1 + 1 + 1, col - 1 - 1))

        # Decrement row (row - 1, col) then diagonal (row - 1 - 1, col +- 1) and then again (row - 1 - 1 - 1, col +-1 +- 1)
        # Must be an empty space
        if self.help_horse_move((row - 1, col), board, piece_owned_by) is not None:
            key_key = next(iter(board[row - 1][col].keys()))
            # Must also be an empty space
            # Increment the columns
            if self.helper_elephant((row - 1 - 1, col + 1), board, piece_owned_by) is not None:
                # Can be an empty space, but must also check if it is an opponent piece.
                if self.helper_elephant((row - 1 - 1 - 1, col + 1 + 1), board, piece_owned_by) is not None:
                    key_key = next(iter(board[row - 1 - 1 - 1][col + 1 + 1].keys()))
                    # If we passed the check to get here the next check is if the piece is an opponent piece.
                    if board[row - 1 - 1 - 1][col + 1 + 1][key_key] != "    ":
                        key_key = next(iter(board[row - 1 - 1 - 1][col + 1 + 1].keys()))
                        if board[row - 1 - 1 - 1][col + 1 + 1][key_key].get_player() != piece_owned_by:
                            if (row - 1 - 1 - 1, col + 1 + 1) not in moves[key]:
                                moves[key].append((row - 1 - 1 - 1, col + 1 + 1))
                    # If the second diag is blank it is an acceptable move.
                    else:
                        if (row - 1 - 1 - 1, col + 1 + 1) not in moves[key]:
                            moves[key].append((row - 1 - 1 - 1, col + 1 + 1))
            # Decrement the columns
            if self.helper_elephant((row - 1 - 1, col - 1), board, piece_owned_by) is not None:
                # Can be an empty space, but must also check if it is an opponent piece.
                if self.helper_elephant((row - 1 - 1 - 1, col - 1 - 1), board, piece_owned_by) is not None:
                    key_key = next(iter(board[row - 1 - 1 - 1][col - 1 - 1].keys()))
                    # If we passed the check to get here the next check is if the piece is an opponent piece.
                    if board[row - 1 - 1 - 1][col - 1 - 1][key_key] != "    ":
                        key_key = next(iter(board[row - 1 - 1 - 1][col - 1 - 1].keys()))
                        if board[row - 1 - 1 - 1][col - 1 - 1][key_key].get_player() != piece_owned_by:
                            if (row - 1 - 1 - 1, col - 1 - 1) not in moves[key]:
                                moves[key].append((row - 1 - 1 - 1, col - 1 - 1))
                    # If the second diag is blank it is an acceptable move.
                    else:
                        if (row - 1 - 1 - 1, col - 1 - 1) not in moves[key]:
                            moves[key].append((row - 1 - 1 - 1, col - 1 - 1))

        # Increment column (row, col + 1) then diagonal (row +- 1, col - 1 - 1)
        # and then again (row +- 1 +- 1, col - 1 - 1 - 1)
        # Must be an empty space
        if self.help_horse_move((row, col + 1), board, piece_owned_by) is not None:
            key_key = next(iter(board[row][col + 1].keys()))
            # Must also be an empty space
            # Increment the rows
            if self.helper_elephant((row + 1, col + 1 + 1), board, piece_owned_by) is not None:
                # Can be an empty space, but must also check if it is an opponent piece.
                if self.helper_elephant((row + 1 + 1, col + 1 + 1 + 1), board, piece_owned_by) is not None:
                    key_key = next(iter(board[row + 1 + 1][col + 1 + 1 + 1].keys()))
                    # If we passed the check to get here the next check is if the piece is an opponent piece.
                    if board[row + 1 + 1][col + 1 + 1 + 1][key_key] != "    ":
                        key_key = next(iter(board[row + 1 + 1][col + 1 + 1 + 1].keys()))
                        if board[row + 1 + 1][col + 1 + 1 + 1][key_key].get_player() != piece_owned_by:
                            if (row + 1 + 1, col + 1 + 1 + 1) not in moves[key]:
                                moves[key].append((row + 1 + 1, col + 1 + 1 + 1))
                    # If the second diag is blank it is an acceptable move.
                    else:
                        if (row + 1 + 1, col + 1 + 1 + 1) not in moves[key]:
                            moves[key].append((row + 1 + 1, col + 1 + 1 + 1))
            # Decrement the rows
            if self.helper_elephant((row - 1, col + 1 + 1), board, piece_owned_by) is not None:
                # Can be an empty space, but must also check if it is an opponent piece.
                if self.helper_elephant((row - 1 - 1, col + 1 + 1 + 1), board, piece_owned_by) is not None:
                    key_key = next(iter(board[row - 1 - 1][col + 1 + 1 + 1].keys()))
                    # If we passed the check to get here the next check is if the piece is an opponent piece.
                    if board[row - 1 - 1][col + 1 + 1 + 1][key_key] != "    ":
                        key_key = next(iter(board[row - 1 - 1][col + 1 + 1 + 1].keys()))
                        if board[row - 1 - 1][col + 1 + 1 + 1][key_key].get_player() != piece_owned_by:
                            if (row - 1 - 1, col + 1 + 1 + 1) not in moves[key]:
                                moves[key].append((row - 1 - 1, col + 1 + 1 + 1))
                    # If the second diag is blank it is an acceptable move.
                    else:
                        if (row - 1 - 1, col + 1 + 1 + 1) not in moves[key]:
                            moves[key].append((row - 1 - 1, col + 1 + 1 + 1))

        # Decrement column (row, col - 1) then diagonal (row +- 1, col - 1 - 1)
        # and then again (row +- 1 +- 1, col - 1 - 1 - 1)
        if self.help_horse_move((row, col - 1), board, piece_owned_by) is not None:
            key_key = next(iter(board[row][col - 1].keys()))
            # Must also be an empty space
            # Increment the rows
            if self.helper_elephant((row + 1, col - 1 - 1), board, piece_owned_by) is not None:
                # Can be an empty space, but must also check if it is an opponent piece.
                if self.helper_elephant((row + 1 + 1, col - 1 - 1 - 1), board, piece_owned_by) is not None:
                    key_key = next(iter(board[row + 1 + 1][col - 1 - 1 - 1].keys()))
                    # If we passed the check to get here the next check is if the piece is an opponent piece.
                    if board[row + 1 + 1][col - 1 - 1 - 1][key_key] != "    ":
                        key_key = next(iter(board[row + 1 + 1][col - 1 - 1 - 1].keys()))
                        if board[row + 1 + 1][col - 1 - 1 - 1][key_key].get_player() != piece_owned_by:
                            if (row + 1 + 1, col - 1 - 1 - 1) not in moves[key]:
                                moves[key].append((row + 1 + 1, col - 1 - 1 - 1))
                    # If the second diag is blank it is an acceptable move.
                    else:
                        if (row + 1 + 1, col - 1 - 1 - 1) not in moves[key]:
                            moves[key].append((row + 1 + 1, col - 1 - 1 - 1))
            # Decrement the rows
            if self.helper_elephant((row - 1, col - 1 - 1), board, piece_owned_by) is not None:
                # Can be an empty space, but must also check if it is an opponent piece.
                if self.helper_elephant((row - 1 - 1, col - 1 - 1 - 1), board, piece_owned_by) is not None:
                    key_key = next(iter(board[row - 1 - 1][col - 1 - 1 - 1].keys()))
                    # If we passed the check to get here the next check is if the piece is an opponent piece.
                    if board[row - 1 - 1][col - 1 - 1 - 1][key_key] != "    ":
                        key_key = next(iter(board[row - 1 - 1][col - 1 - 1 - 1].keys()))
                        if board[row - 1 - 1][col - 1 - 1 - 1][key_key].get_player() != piece_owned_by:
                            if (row - 1 - 1, col - 1 - 1 - 1) not in moves[key]:
                                moves[key].append((row - 1 - 1, col - 1 - 1 - 1))
                    # If the second diag is blank it is an acceptable move.
                    else:
                        if (row - 1 - 1, col - 1 - 1 - 1) not in moves[key]:
                            moves[key].append((row - 1 - 1, col - 1 - 1 - 1))

        return moves[key]

    def helper_elephant(self, possible_move, board, piece_owned_by):
        """
        Takes a possible move and check if the possible move is occupied
        by a piece that the player owns.

        It will only return a possible move if the possible move is within
        the confines of the board and the possible move is on an empty or enemy
        piece spaces
        """

        row = possible_move[0]
        col = possible_move[1]
        if self.map_move_in_bounds(possible_move) is False:
            return None
        key = next(iter(board[row][col].keys()))
        # check if the space is occupied by your own piece.
        if board[row][col][key] != "    ":
            if board[row][col][key].get_player() == piece_owned_by:
                # Can not make a move on your own piece.
                return None
        else:
            return not None
        return possible_move

    def horse_moves(self, key, piece_owned_by, moves, piece_curr_placement, board):
        """
        This method will return the dictionary with all moves for the horse.

        The key parameter is the key for the dictionary which will have be what is displayed on the
        board. For example bHR(9, 2) is the red players general that is at the 10th row, 3rd column.

        PLayer turn is used to determine if the player moves a piece to a space with a piece that is
        their own piece.

        moves is the current moves dictionary that is being built that will contain all of the moves for
        every move.

        piece_curr_placement is just the current placement of the piece we are trying to find all of the moves for.

        The board parameter is used to find the next possible moves.
        """
        row = piece_curr_placement[0]
        col = piece_curr_placement[1]
        moves[key] = []

        # Advance row (row+1, col) then diagonal (row + 1 + 1, col +- 1)
        if self.help_horse_move((row + 1, col), board, piece_owned_by) is not None:
            key_key = next(iter(board[row + 1][col].keys()))
            # First move must be to an open space.
            if board[row + 1][col][key_key] == "    ":
                if self.help_horse_move((row + 1 + 1, col + 1), board, piece_owned_by) is not None:
                    moves[key].append((row + 1 + 1, col + 1))
                if self.help_horse_move((row + 1 + 1, col - 1), board, piece_owned_by) is not None:
                    moves[key].append((row + 1 + 1, col - 1))
        # Decrement row (row-1, col) then diagonal (row - 1 - 1, col +- 1)
        if self.help_horse_move((row - 1, col), board, piece_owned_by) is not None:
            key_key = next(iter(board[row - 1][col].keys()))
            # First move must be to an open space.
            if board[row - 1][col][key_key] == "    ":
                if self.help_horse_move((row - 1 - 1, col + 1), board, piece_owned_by) is not None:
                    moves[key].append((row - 1 - 1, col + 1))
                if self.help_horse_move((row - 1 - 1, col - 1), board, piece_owned_by) is not None:
                    moves[key].append((row - 1 - 1, col - 1))

        # Advance column (row, col + 1) then diagonal (row +- 1, col + 1 + 1)
        if self.help_horse_move((row, col + 1), board, piece_owned_by) is not None:
            key_key = next(iter(board[row][col + 1].keys()))
            # First move must be to an open space.
            if board[row][col + 1][key_key] == "    ":
                if self.help_horse_move((row + 1, col + 1 + 1), board, piece_owned_by) is not None:
                    moves[key].append((row + 1, col + 1 + 1))
                if self.help_horse_move((row - 1, col + 1 + 1), board, piece_owned_by) is not None:
                    moves[key].append((row - 1, col + 1 + 1))
        # Decrement column (row, col - 1) then diagonal (row +- 1, col - 1 - 1)
        if self.help_horse_move((row, col - 1), board, piece_owned_by) is not None:
            key_key = next(iter(board[row][col - 1].keys()))
            # First move must be to an open space.
            if board[row][col - 1][key_key] == "    ":
                if self.help_horse_move((row + 1, col - 1 - 1), board, piece_owned_by) is not None:
                    moves[key].append((row + 1, col - 1 - 1))
                if self.help_horse_move((row - 1, col - 1 - 1), board, piece_owned_by) is not None:
                    moves[key].append((row - 1, col - 1 - 1))

        return moves[key]

    def help_horse_move(self, possible_move, board, piece_owned_by):
        """
        Takes a possible move and check if the possible move is occupied
        by a piece that the player owns.

        It will only return a possible move if the possible move is within
        the confines of the board and the possible move is on an empty or enemy
        piece spaces.
        """

        row = possible_move[0]
        col = possible_move[1]
        if self.map_move_in_bounds(possible_move) is False:
            return None
        key = next(iter(board[row][col].keys()))
        # check if the space is occupied by your own piece.
        if board[row][col][key] != "    ":
            if board[row][col][key].get_player() == piece_owned_by:
                return None
        return possible_move

    def general_moves(self, key, piece_owned_by, moves, piece_curr_placement, board):
        """
        This method will return the dictionary with all moves for the general and guard.

        The key parameter is the key for the dictionary which will have be what is displayed on the
        board. For example rGN(1, 4) is the red players general that is at the 2nd row, 5th column.

        PLayer turn is used to determine if the player moves a piece to a space with a piece that is
        their own piece.

        moves is the current moves dictionary that is being built that will contain all of the moves for
        every move.

        piece_curr_placement is just the current placement of the piece we are trying to find all of the moves for.

        The board parameter is used to find the next possible moves.
        """
        row = piece_curr_placement[0]
        col = piece_curr_placement[1]
        moves[key] = []
        key_key = next(iter(board[row][col].keys()))
        if "center_fortress" in key_key or "diag_left" in key_key or "diag_right" == key_key:
            for _row in range(-1, 2):
                for _col in range(-1, 2):
                    if self.helper_general_moves((row + _row, col + _col), board, piece_owned_by) is not None:
                        if (row + _row, col + _col) not in moves[key]:
                            moves[key].append((row + _row, col + _col))
        elif "diag_left" not in key_key and "diag_right" not in key_key and "center_fortress" not in key_key:
            for _row in range(-1, 2):
                for _col in range(-1, 2):
                    # No diag check
                    if _row == _col or _row == -_col:
                        continue
                    if _row == 0 and _col == 1:
                        if self.helper_general_moves((row + _row, col + _col), board, piece_owned_by):
                            if (row + _row, col + _col) not in moves[key]:
                                moves[key].append((row + _row, col + _col))
                    if _row == 0 and _col == -1:
                        if self.helper_general_moves((row + _row, col + _col), board, piece_owned_by):
                            if (row + _row, col + _col) not in moves[key]:
                                moves[key].append((row + _row, col + _col))
                    if _row == 1 and _col == 0:
                        if self.helper_general_moves((row + _row, col + _col), board, piece_owned_by):
                            if (row + _row, col + _col) not in moves[key]:
                                moves[key].append((row + _row, col + _col))
                    if _row == -1 and _col == 0:
                        if self.helper_general_moves((row + _row, col + _col), board, piece_owned_by):
                            if (row + _row, col + _col) not in moves[key]:
                                moves[key].append((row + _row, col + _col))

        return moves[key]

    def helper_general_moves(self, possible_move, board, piece_owned_by):
        """
        Takes a possible move and check if the possible move is occupied
        by a piece that the player owns.

        Also takes the board and the players turn as parameters.

        It will only return a possible move if the possible move is within
        the confines of the board and the possible move is on an empty or enemy
        piece spaces.
        """
        row = possible_move[0]
        col = possible_move[1]
        if self.map_move_in_bounds(possible_move) is False:
            return None
        key = list(board[row][col].keys())
        # The general must move on the fortress
        if "fortress" not in key:
            return None
        # check if the space is occupied by your own piece.
        key = next(iter(board[row][col].keys()))
        if board[row][col][key] != "    ":
            if board[row][col][key].get_player() == piece_owned_by:
                return None

        return possible_move

    def chariot_moves(self, key, piece_owned_by, moves, curr_placement, board):
        """
        This will go through all the possible legal moves for the chariot.
        For example. All moves to the left or right, the advancing position,and if the
        Chariot piece is in the fortress regardless
        of if any piece is in the way or not.

        The key parameter is the key for the dictionary which will have be what is displayed on the
        board. For example bCH(0, 8) is the blue players chariot that is at the 1st row, 9th column.

        PLayer turn is used to determine if the player moves a piece to a space with a piece that is
        their own piece.

        moves is the current moves dictionary that is being built that will contain all of the moves for
        every move.

        piece_curr_placement is just the current placement of the piece we are trying to find all of the moves for.

        The board parameter is used to find the next possible moves.
        """
        row = curr_placement[0]
        col = curr_placement[1]
        moves[key] = []
        # Check if chariot is in the fortress.
        key_key = next(iter(board[row][col]))
        # If the piece is on one of these spaces it can move diagonally
        if 'diag_left' in key_key or 'diag_right' in key_key or 'center_fortress' in key_key:
            # check all spaces around the current space.
            for _row in range(-1, 2):
                for _col in range(-1, 2):
                    # Skip over the current placement
                    if _row == 0 and _col == 0:
                        continue
                    # Check if next possible move is in the board or not on a piece owned by the same player.
                    if self.helper_chariot_moves((row + _row, col + _col), board, piece_owned_by) is True:
                        if (row + _row, col + _col) not in moves[key]:
                            # Add initial diagonal move to moves list
                            moves[key].append((row + _row, col + _col))
                        continue
                    if self.helper_chariot_moves((row + _row, col + _col), board, piece_owned_by) is not None:
                        # This will be the key of the space.
                        key_key = next(iter(board[row + _row][col + _col]))
                        # Only these spaces can accept and move from a diagonal space.
                        if 'diag_left' in key_key or 'diag_right' in key_key or 'center_fortress' in key_key:
                            if (row + _row, col + _col) not in moves[key]:
                                # Add initial diagonal move to moves list
                                moves[key].append((row + _row, col + _col))
                                # If we get here we can possibly move another diagonal space
                                # Lets check if the next available diagonal space is available.
                                if self.helper_chariot_moves((row + _row + _row, col + _col + _col), board,
                                                             piece_owned_by):
                                    key_key = next(iter(board[row + _row + _row][col + _col + _col]))
                                    if 'diag_left' in key_key or 'diag_right' in key_key or 'center_fortress' in key_key:
                                        moves[key].append((row + _row + _row, col + _col + _col))

        moves[key] = self.chariot_checker(key, piece_owned_by, curr_placement, moves[key], self.get_board(), 1, 0)
        moves[key] = self.chariot_checker(key, piece_owned_by, curr_placement, moves[key], self.get_board(), -1, 0)
        moves[key] = self.chariot_checker(key, piece_owned_by, curr_placement, moves[key], self.get_board(), 0, 1)
        moves[key] = self.chariot_checker(key, piece_owned_by, curr_placement, moves[key], self.get_board(), 0, -1)

        return moves[key]

    def chariot_checker(self, key, piece_owned_by, curr_placement, list_of_moves, board, _row_, _col_):
        row = curr_placement[0]
        col = curr_placement[1]
        piece_found = False
        for num in range(1, 10):
            if self.map_move_in_bounds((row + (num * _row_), col + (num * _col_))) is False:
                return list_of_moves
            # Move increasing rows (row + num, col)
            if not piece_found:
                # If this returns True then an enemy piece has been found. Add to list and swap move_inc and pass
                if self.helper_chariot_moves((row + (num * _row_), col + (num * _col_)), board,
                                             piece_owned_by) is True:
                    if (row + (num * _row_), col + (num * _col_)) not in list_of_moves:
                        list_of_moves.append((row + (num * _row_), col + (num * _col_)))
                    return list_of_moves
                elif self.helper_chariot_moves((row + (num * _row_), col + (num * _col_)), board,
                                               piece_owned_by) is not None:
                    if (row + (num * _row_), col + (num * _col_)) not in list_of_moves:
                        list_of_moves.append((row + (num * _row_), col + (num * _col_)))
                else:
                    # Set move_inc to false so we dont skip over pieces and keep adding to list.
                    piece_found = True
            else:
                return list_of_moves
        return list_of_moves

    def helper_chariot_moves(self, possible_move, board, piece_owned_by):
        """
        Takes a possible move and check if the possible move is occupied
        by a piece that the player owns.

        Also takes the board and the players turn as parameters.

        It will only return a possible move if the possible move is within
        the confines of the board and the possible move is on an empty or enemy
        piece spaces.
        """
        row = possible_move[0]
        col = possible_move[1]

        if self.map_move_in_bounds(possible_move) is False:
            return None
        key = next(iter(board[row][col].keys()))
        # check if the space is occupied by your own piece.
        if board[row][col][key] != "    ":
            if board[row][col][key].get_player() == piece_owned_by:
                return None
            elif board[row][col][key].get_player() != piece_owned_by:
                return True

        return possible_move

    def soldier_moves(self, key, piece_owned_by, moves, curr_placement, board):
        """
        This will go through all the possible legal moves for the soldier.
        For example. all moves to the left or right, the advancing position,and if the
        Soldier piece is in the fortress regardless
        of if any piece is in the way or not.

        The key parameter is the key for the dictionary which will have be what is displayed on the
        board. For example rSO(0, 3) is the red players soldier that is at the 1st row, 3rd column.

        PLayer turn is used to determine if the player moves a piece to a space with a piece that is
        their own piece.

        moves is the current moves dictionary that is being built that will contain all of the moves for
        every move.

        piece_curr_placement is just the current placement of the piece we are trying to find all of the moves for.

        The board parameter is used to find the next possible moves.
        """
        row = curr_placement[0]
        col = curr_placement[1]
        moves[key] = []
        # Add moves if piece is currently in fortress.
        key_key = next(iter(board[row][col].keys()))
        if piece_owned_by == 'r':
            if self.help_soldier_moves((row + 1, col), board, piece_owned_by) is not None:
                if (row + 1, col) not in moves[key]:
                    moves[key].append((row + 1, col))
            if 'diag_left' in key_key or 'center' in key_key:
                if self.help_soldier_moves((row + 1, col - 1), board, piece_owned_by) is not None:
                    if (row + 1, col - 1) not in moves[key]:
                        moves[key].append((row + 1, col - 1))
            if 'diag_right' in key_key or 'center' in key_key:
                if self.help_soldier_moves((row + 1, col + 1), board, piece_owned_by) is not None:
                    if (row + 1, col + 1) not in moves[key]:
                        moves[key].append((row + 1, col + 1))
        elif piece_owned_by == 'b':
            if self.help_soldier_moves((row - 1, col), board, piece_owned_by) is not None:
                if (row - 1, col) not in moves[key]:
                    moves[key].append((row - 1, col))
            if 'diag_right' in key_key or 'center' in key_key:
                if self.help_soldier_moves((row - 1, col - 1), board, piece_owned_by) is not None:
                    if (row - 1, col + 1) not in moves[key]:
                        moves[key].append((row - 1, col - 1))
            if 'diag_left' in key_key or 'center' in key_key:
                if self.help_soldier_moves((row - 1, col + 1), board, piece_owned_by) is not None:
                    if (row - 1, col - 1) not in moves[key]:
                        moves[key].append((row - 1, col + 1))

        if self.help_soldier_moves((row, col - 1), board, piece_owned_by) is not None:
            if (row, col - 1) not in moves[key]:
                moves[key].append((row, col - 1))
        if self.help_soldier_moves((row, col + 1), board, piece_owned_by) is not None:
            if (row, col + 1) not in moves[key]:
                moves[key].append((row, col + 1))

        return moves[key]

    def help_soldier_moves(self, possible_move, board, piece_owned_by):
        """
        Takes a possible move and check if the possible move is occupied
        by a piece that the player owns.

        It will only return a possible move if the possible move is within
        the confines of the board and the possible move is on an empty or enemy
        piece spaces.
        """

        row = possible_move[0]
        col = possible_move[1]
        if self.map_move_in_bounds(possible_move) is False:
            return None
        key = next(iter(board[row][col].keys()))
        # check if the space is occupied by your own piece.
        if board[row][col][key] != "    ":
            if board[row][col][key].get_player() == piece_owned_by:
                return None

        return possible_move

    def possible_moves(self, board, list_of_pieces):
        """
        This will create a dictionary of all pieces from the list of pieces.

        It will first set the moves dictionary to an empty dictionary.
        Then it will go through all of the pieces and return the possible
        moves for each piece.
        """
        # TODO make moves their own separate dictionaries. Maybe in there respective Piece class.
        moves = {}
        for piece in list_of_pieces:
            piece_owned_by = piece.get_player()
            type = piece.get_piece_type()
            display = piece.get_piece_display()
            row = piece.get_row()
            col = piece.get_col()
            key = str(piece_owned_by) + str(display) + "(" + str(row) + "," + str(col) + ")"
            piece_curr_placement = (row, col)

            # Set up all possible soldier moves.
            if type == 'soldier':
                moves[key] = self.soldier_moves(key, piece_owned_by, moves, piece_curr_placement, board)
            if type == 'chariot':
                moves[key] = self.chariot_moves(key, piece_owned_by, moves, piece_curr_placement, board)
            if type == 'horse':
                moves[key] = self.horse_moves(key, piece_owned_by, moves, piece_curr_placement, board)
            if type == 'cannon':
                moves[key] = self.cannon_moves(key, piece_owned_by, moves, piece_curr_placement, board)
            if type == 'elephant':
                moves[key] = self.elephant_moves(key, piece_owned_by, moves, piece_curr_placement, board)
            # Can use the general because it uses the same moves.
            if type == 'guard':
                moves[key] = self.general_moves(key, piece_owned_by, moves, piece_curr_placement, board)
            if type == 'general':
                moves[key] = self.general_moves(key, piece_owned_by, moves, piece_curr_placement, board)

        return moves

    def get_piece_from_board(self, row, col):
        board = self.get_board()
        key = next(iter(board[row][col].keys()))
        if board[row][col][key] != '    ':
            return board[row][col][key]
        else:
            return False

    def move(self, piece, row, col, window):
        move_key = str(piece.get_board_display()) + "(" + str(piece.get_row()) + "," + str(piece.get_col()) + ")"
        curr_key = next(iter(self.get_board()[piece.get_row()][piece.get_col()].keys()))
        next_key = next(iter(self.get_board()[row][col].keys()))

        if move_key in self.get_moves():
            if (row, col) not in self.get_moves()[move_key]:
                print("NOT A VALID MOVE")
                return False

        self.get_board()[row][col][next_key] = self.get_board()[piece.get_row()][piece.get_col()][curr_key]
        self.get_board()[piece.get_row()][piece.get_col()][curr_key] = "    "

        piece.move(row, col)
        if piece.get_player() == 'r':
            pygame.draw.circle(window, RED, (piece.get_x_coord(), piece.get_y_coord()), RADIUS)
        elif piece.get_player() == 'b':
            pygame.draw.circle(window, BLUE, (piece.get_x_coord(), piece.get_y_coord()), RADIUS)

        self.update_pieces(self.get_board())
        self.update_moves(self.get_board(), self.get_pieces())
        ####
        piece.set_move_key(piece.get_board_display() + "(" + str(piece.get_row()) + "," + str(piece.get_col()) + ")")
        # self.swap_player_turn(self.get_player_turn())
        return True

    def move_in_check(self, piece, row, col, window):
        move_key = str(piece.get_board_display()) + "(" + str(piece.get_row()) + "," + str(piece.get_col()) + ")"
        curr_key = next(iter(self.get_board()[piece.get_row()][piece.get_col()].keys()))
        next_key = next(iter(self.get_board()[row][col].keys()))

        if move_key in self.get_moves():
            if (row, col) not in self.get_moves()[move_key]:
                print("NOT A VALID MOVE")
                return False

        self.get_board()[row][col][next_key] = self.get_board()[piece.get_row()][piece.get_col()][curr_key]
        self.get_board()[piece.get_row()][piece.get_col()][curr_key] = "    "

        piece.move_in_check(row, col)

        self.update_pieces(self.get_board())
        self.update_moves(self.get_board(), self.get_pieces())
        ####
        # piece.set_move_key(piece.get_board_display() + "(" + str(piece.get_row()) + "," + str(piece.get_col()) + ")")
        # self.swap_player_turn(self.get_player_turn())
        return True

    def place_on_board(self, window, pieces):
        for piece in pieces:
            piece.draw_piece(window, piece, RADIUS, font)

    def new_board(self, row, col):
        """This will create a blank game board."""
        board = []
        for x in range(col):
            board.append([])
        for y in board:
            for z in range(row):
                y.append(dict([(" space  ", "    ")]))
        return board

    def new_pieces(self):
        """
        This will create and return a list of all the pieces for their initial placements.
        Also initializes all children of the Piece class.
        """

        pieces = [
            General('r', 1, 4),
            General('b', 8, 4),
            Soldier('r', 3, 0), Soldier('r', 3, 2), Soldier('r', 3, 4), Soldier('r', 3, 6), Soldier('r', 3, 8),
            Cannon('r', 2, 1), Cannon('r', 2, 7),
            Chariot('r', 0, 0), Chariot('r', 0, 8),
            Elephant('r', 0, 1), Elephant('r', 0, 6),
            Horse('r', 0, 2), Horse('r', 0, 7),
            Guard('r', 0, 3), Guard('r', 0, 5),
            Soldier('b', 6, 0), Soldier('b', 6, 2), Soldier('b', 6, 4), Soldier('b', 6, 6), Soldier('b', 6, 8),
            Cannon('b', 7, 1), Cannon('b', 7, 7),
            Chariot('b', 9, 0), Chariot('b', 9, 8),
            Elephant('b', 9, 1), Elephant('b', 9, 6),
            Horse('b', 9, 2), Horse('b', 9, 7),
            Guard('b', 9, 3), Guard('b', 9, 5)
        ]

        return pieces

    def initial_placements(self, board, list_of_pieces):
        """
        This will make the initial placements on the board for all pieces.

        This will take the board as a parameter, but it will be from the new_board method
        to allow for initial placements to an empty board.

        There is also the list_of_pieces parameter which is the new_pieces
        method which has all of the initializations of all of the pieces and
        their placements.
        """
        # For every piece in the list of pieces
        for piece in list_of_pieces:
            piece_type = piece.get_piece_type()
            piece_row = piece.get_row()
            piece_col = piece.get_col()
            if piece_type == 'general':
                for col in range(-1, 2):
                    for row in range(-1, 2):
                        if (col == -1 and row == -1) or (col == 1 and row == 1) or (col == 0 and row == 0):
                            board[piece_row + row][piece_col + col].update(diag_right="    ")
                            board[piece_row + row][piece_col + col].pop(" space  ", None)
                            board[piece_row + row][piece_col + col].update(fortress="    ")
                            # board[piece_row + row][piece_col + col].pop(" space  ", None)
                        elif (col == -1 and row == 1) or (col == 1 and row == -1):
                            board[piece_row + row][piece_col + col].update(diag_left="    ")
                            board[piece_row + row][piece_col + col].pop(" space  ", None)
                            board[piece_row + row][piece_col + col].update(fortress="    ")
                        elif col == 0 and row == 0:
                            board[piece_row + row][piece_col + col].update(center_fortress="    ")
                            board[piece_row + row][piece_col + col].pop(" space  ", None)
                            board[piece_row + row][piece_col + col].update(fortress="    ")
                        board[piece_row + row][piece_col + col].pop(" space  ", None)
                        board[piece_row + row][piece_col + col].update(fortress="    ")
                    # places generals in there places
                    board[piece_row][piece_col]['center_fortress'] = piece
                    board[piece_row][piece_col].pop("", None)
            # Places guards within the fortress.
            elif piece_type == "guard":
                key = list(board[piece_row][piece_col].keys())
                if 'diag_right' in key:
                    board[piece_row][piece_col]['diag_right'] = piece
                    board[piece_row][piece_col].pop("space", None)
                if 'diag_left' in key:
                    board[piece_row][piece_col]['diag_left'] = piece
                    board[piece_row][piece_col].pop("space", None)
            else:
                board[piece_row][piece_col][' space  '] = piece
                board[piece_row][piece_col].pop("space", None)

        return board

    def update_pieces(self, board):
        """
        This will set update pieces and the possible moves for all pieces.

        This method takes the board as a parameter and goes through the entire board
        and if it finds a piece on the board it will add it to the update_piece_list.

        We then set the update_piece_list as the new self._pieces with the set_pieces setter.

        Then the self.possible_moves method is called to update the moves for the pieces
        and their new placements on the board, and then call the set_moves method
        to set the new possible moves.
        """
        # Update pieces and moves list
        # get a list of all pieces.
        update_piece_list = []
        for _row in range(9):
            for _col in range(10):
                update_key = next(iter(board[_col][_row].keys()))
                if board[_col][_row][update_key] != "    ":
                    update_piece_list.append(board[_col][_row][update_key])
        self.set_pieces(update_piece_list)
        # [print(i.get_player() + i.get_piece_display(), i.get_row(), "," , i.get_col()) for i in self.get_pieces()]
        # new_moves = self.possible_moves(board, update_piece_list)
        # [print(i, new_moves[i]) for i in new_moves]
        return update_piece_list

    def draw_board(self, window):
        """This will help draw the Janggi board"""
        board_surface = pygame.display.set_mode((WIDTH, HEIGHT))
        board_surface.fill(JANGGI_BOARD_COLOR)

        # This will make the A-I and 1-10 for the rows and labels
        col_letters = ['A', 'B',
                       'C', 'D',
                       'E', 'F',
                       'G', 'H',
                       'I'
                       ]

        # Horizontal Lines
        for col in range(COLS):
            start_x = PADDING_ON_LEFT
            start_y = (col * self.get_space_height()) + PADDING_ON_TOP
            end_x = PADDING_ON_LEFT + ((COLS - 2) * self.get_space_width())
            end_y = (col * self.get_space_height()) + PADDING_ON_TOP
            # print((start_x, start_y), (end_x, end_x))
            pygame.draw.line(board_surface, BLACK, (start_x, start_y), (end_x, end_y))

        # Display numbers for the rows
        for num in range(COLS):
            num_str = str(num + 1)
            text = font.render(num_str, True, BLACK)
            y_coord = (PADDING_ON_TOP - (PADDING_ON_TOP * .03) // 1) + self.get_space_height() * num
            window.blit(text, (PADDING_ON_TOP // 2, y_coord))

        # Vertical lines
        for row in range(ROWS):
            start_x = (row * self.get_space_width()) + PADDING_ON_LEFT
            start_y = PADDING_ON_TOP
            end_x_vert = (row * self.get_space_width()) + PADDING_ON_LEFT
            end_y = PADDING_ON_TOP + (ROWS * self.get_space_height())
            pygame.draw.line(board_surface, BLACK, (start_x, start_y), (end_x_vert, end_y))

        # Display letters in the columns
        for letter in range(len(col_letters)):
            text = font.render(col_letters[letter], True, BLACK)
            x_coord = (PADDING_ON_LEFT - (PADDING_ON_LEFT * .03) // 1) + self.get_space_width() * letter
            window.blit(text, (x_coord, PADDING_ON_TOP // 2))

        # Diagonal lines for fortress
        pygame.draw.line(board_surface, BLACK,
                         (PADDING_ON_LEFT + 3 * self.get_space_width(), PADDING_ON_TOP),
                         (PADDING_ON_LEFT + 5 * self.get_space_width(), PADDING_ON_TOP + 2 * self.get_space_height()))
        pygame.draw.line(board_surface, BLACK,
                         (PADDING_ON_LEFT + 3 * self.get_space_width(), PADDING_ON_TOP + 2 * self.get_space_height()),
                         (PADDING_ON_LEFT + 5 * self.get_space_width(), PADDING_ON_TOP))
        pygame.draw.line(board_surface, BLACK,
                         (PADDING_ON_LEFT + 3 * self.get_space_width(), PADDING_ON_TOP + 7 * self.get_space_height()),
                         (PADDING_ON_LEFT + 5 * self.get_space_width(), PADDING_ON_TOP + 9 * self.get_space_height()))
        pygame.draw.line(board_surface, BLACK,
                         (PADDING_ON_LEFT + 3 * self.get_space_width(), PADDING_ON_TOP + 9 * self.get_space_height()),
                         (PADDING_ON_LEFT + 5 * self.get_space_width(), PADDING_ON_TOP + 7 * self.get_space_height()))

        if self.check(window) is True:
            if self.get_player_in_check() == "RED":
                check_str = "RED IS IN CHECK"
                text = font.render(check_str, True, BLACK)
                window.blit(text, (WIDTH - text.get_width() - (text.get_width() // 4), PADDING_ON_TOP))

            else:
                check_str = "BLUE IS IN CHECK"
                text = font.render(check_str, True, BLACK)
                window.blit(text,
                            (WIDTH - text.get_width() - (text.get_width() // 4),
                             HEIGHT - PADDING_ON_TOP))




        self.place_on_board(window, self.get_pieces())

        if self.get_game_state() == "UNFINISHED":
            self.draw_player_turn(window)
        else:
            self.draw_winner(window, self.get_game_state())

        return board_surface

    def draw_winner(self, window, game_state):
        if game_state == "BLUE_WON":
            text = font.render(game_state, True, BLACK)
            window.blit(text,
                        (WIDTH - text.get_width() - (text.get_width() // 4),
                         HEIGHT - PADDING_ON_TOP))
        elif game_state == "RED_WON":
            text = font.render(game_state, True, BLACK)
            window.blit(text, (WIDTH - text.get_width() - (text.get_width() // 4), PADDING_ON_TOP))
        else:
            text = font.render(game_state, True, BLACK)
            window.blit(text, (WIDTH - text.get_width() - (text.get_width() // 4), PADDING_ON_TOP))
            window.blit(text,
                        (WIDTH - text.get_width() - (text.get_width() // 4),
                         HEIGHT - PADDING_ON_TOP))
            print("Draw??")

    def get_space_height(self):
        return self._spaceHeight

    def get_space_width(self):
        return self._spaceWidth

    def get_selected(self):
        return self._selected

    def set_selected(self, piece_or_None):
        self._selected = piece_or_None

    def get_board(self):
        """This will return the board"""
        return self._board

    def set_board(self, new_board):
        """This will set a new board"""
        self._board = new_board

    def get_player_turn(self):
        """This will return whose turn it is"""
        return self._player_turn

    def set_player_turn(self, next_player_turn):
        """This will set player_turn to the next player turn."""
        self._player_turn = next_player_turn

    def get_moves(self):
        """This will return the moves for any given Piece object."""
        return self._moves

    def update_moves(self, board, piece_list):
        """This method will set the new possible moves."""
        new_moves = self.possible_moves(board, piece_list)
        self.set_moves(new_moves)

    def set_moves(self, possible_moves):
        """This will set the moves of any given Piece object"""
        self._moves = possible_moves

    def set_game_state(self, state_to_add):
        """Sets the game state."""
        self._game_state = state_to_add

    def get_game_state(self):
        """this wil return the current game state"""
        return self._game_state

    def get_pieces(self):
        """This will return the list of pieces"""
        return self._pieces

    def set_pieces(self, list_of_pieces):
        self._pieces = list_of_pieces

    def get_player_in_check(self):
        return self._player_in_check

    def set_player_in_check(self, player_in_check):
        self._player_in_check = player_in_check

    def display_board(self):
        """
        This will display the board with letters for the columns,
        and numbers for the rows.
        Mostly for testing purposes.
        """
        board = self.get_board()
        col_letters = ['   A   ', '   B   ',
                       '   C   ', '   D   ',
                       '   E   ', '   F   ',
                       '   G   ', '   H   ',
                       '   I   '
                       ]
        row_count = 1
        print("-  |", end="")  # Print out column letters
        [print(" " + i + " |", end="") for i in col_letters]
        print()
        print("-" * 94)  # make divider
        for row in range(10):
            if row_count == 10:
                print(row_count, "|", end="")
                row_count += 1
            else:
                print(row_count, " |", end="")
                row_count += 1

            for col in range(9):
                key = next(iter(board[row][col].keys()))
                if board[row][col][key] != "    ":
                    player = board[row][col][key].get_player()
                    display = board[row][col][key].get_piece_display()
                    display_on_board = player + display
                    # player = piece.get_player()
                    # display = piece.get_piece_display()
                    print("   " + display_on_board + "   |", end="")
                elif key == "center_fortress":
                    print("   ===   " + "|", end="")
                elif key == " space  ":
                    print("   ---   " + "|", end="")
                elif key == "fortress":
                    print("   ===   " + "|", end="")
                elif key == "diag_right":
                    print("   \ \   " + "|", end="")
                elif key == "diag_left":
                    print("   / /   " + "|", end="")

            print()
            print("-" * 94)  # make divider
