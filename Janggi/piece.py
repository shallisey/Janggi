import pygame
from .constants import *

class Piece:
    """
    This will represent a piece on the board

    The Piece class will keep track of a pieces owned_by (ie the player),
    the pieces row and column placement on the board.

    The Piece class will interact with its subsequent children classes and the
    board in the JanggiGame class.
    """


    def __init__(self, owned_by, row, col):
        """This will initialize piece object"""
        self._owned_by = owned_by
        self._row = row
        self._col = col
        self._x_coord = (((WIDTH - PADDING_ON_LEFT - PADDING_ON_TOP)//COLS) * self.get_col()) + PADDING_ON_LEFT
        self._y_coord = (((HEIGHT - PADDING_ON_TOP - PADDING_ON_LEFT)//ROWS) * self.get_row()) + PADDING_ON_TOP


    def set_x_coord(self, new_x_coord):
        self._x_coord = new_x_coord

    def set_y_coord(self, new_y_coord):
        self._y_coord = new_y_coord

    def move_in_check(self, new_row, new_col):
        self.set_row(new_row)
        self.set_col(new_col)

    def move(self, new_row, new_col):
        self.set_row(new_row)
        self.set_col(new_col)
        new_x_coord = (((WIDTH - PADDING_ON_LEFT - PADDING_ON_TOP)//COLS) * self.get_col()) + PADDING_ON_LEFT
        new_y_coord = (((HEIGHT - PADDING_ON_TOP - PADDING_ON_LEFT)//ROWS) * self.get_row()) + PADDING_ON_TOP
        self.set_x_coord(new_x_coord)
        self.set_y_coord(new_y_coord)
        new_board_position = self.calculate_board_pos()
        return new_board_position

    def calculate_board_pos(self):
        row = self.get_x_coord()
        col = self.get_y_coord()
        board_position = (row, col)
        return board_position

    def draw_piece(self, window, piece):
        # Display either a red or blue piece
        if piece.get_player() == 'r':
            piece_returned = self.return_piece(piece)
            piece_image = pygame.image.load(piece_returned.get_image())
            piece_image = pygame.transform.scale(piece_image, (piece_image.get_width()//2, piece_image.get_height()//2))
            piece_image.convert()
            img_rect = piece_image.get_rect()
            img_rect.center = (piece_returned.get_x_coord(), piece_returned.get_y_coord())
            window.blit(piece_image, img_rect)

        elif piece.get_player() == 'b':
            # pygame.draw.circle(window, BLUE, (piece.get_x_coord(), piece.get_y_coord()), radius)
            piece_returned = self.return_piece(piece)
            piece_image = pygame.image.load(piece_returned.get_image())
            piece_image = pygame.transform.scale(piece_image, (piece_image.get_width()//2, piece_image.get_height()//2))
            piece_image.convert()
            img_rect = piece_image.get_rect()
            img_rect.center = (piece_returned.get_x_coord(), piece_returned.get_y_coord())
            window.blit(piece_image, img_rect)
            # pygame.draw.rect(window, WHITE, img_rect)

    def return_piece(self, piece):
        if piece.get_piece_type() == 'general':
            return piece
        elif piece.get_piece_type() == 'guard':
            return piece
        elif piece.get_piece_type() == 'elephant':
            return piece
        elif piece.get_piece_type() == 'horse':
            return piece
        elif piece.get_piece_type() == 'cannon':
            return piece
        elif piece.get_piece_type() == 'chariot':
            return piece
        elif piece.get_piece_type() == 'soldier':
            return piece

    def get_x_coord(self):
        return self._x_coord

    def get_y_coord(self):
        return self._y_coord

    def get_player(self):
        """This will return the owner of the piece."""
        return self._owned_by

    def get_row(self):
        """This will return the row the piece is placed at."""
        return self._row

    def set_row(self, new_row):
        """This will set the row the piece will go to."""
        self._row = new_row

    def get_col(self):
        """This will return the column the piece is placed at."""
        return self._col

    def set_col(self, new_col):
        """This will set the column the piece will go to."""
        self._col = new_col







class Soldier(Piece):
    """
    This will represent the soldier piece. Child to the piece Class.
    """

    def __init__(self, owned_by, row, col):
        """
        Initialize the Soldier piece

        This Soldier inherits the Piece class and keeps track of the
        type of piece it is and how it is displayed in the show board method in
        the JanggiGame class.
        """
        super().__init__(owned_by, row, col)
        self._piece_type = "soldier"
        self._piece_display = "SO"
        self._board_display = self.get_player() + self.get_piece_display()
        self._move_key = self.get_board_display() + "(" + str(self.get_row()) + "," + str(self.get_col()) + ")"
        self._soldier_moves = {}
        if self.get_player() == 'r':
            self._image = "Janggi/assets/Red_Soldier.png"
        else:
            self._image = "Janggi/assets/Blue_Soldier.png"

    def get_image(self):
        return self._image

    def set_move_key(self, new_key):
        self._move_key = new_key

    def get_move_key(self):
        return self._move_key

    def get_piece_type(self):
        """This will return the piece type."""
        return self._piece_type

    def get_piece_display(self):
        """This will return what is to be displayed on the board as the soldier piece."""
        return self._piece_display

    def get_board_display(self):
        return self._board_display


class Cannon(Piece):
    """
    This will represent the cannon piece. Child to the piece Class.

    Initialize the Cannon piece

    This Cannon inherits the Piece class and keeps track of the
    type of piece it is and how it is displayed in the show board method in
    the JanggiGame class.
    """

    def __init__(self, owned_by, row, col):
        """Initialize the Cannon piece"""
        super().__init__(owned_by, row, col)
        self._piece_type = "cannon"
        self._piece_display = "CN"
        self._board_display = self.get_player() + self.get_piece_display()
        self._cannon_moves = {}
        self._move_key = self.get_board_display() + "(" + str(self.get_row()) + "," + str(self.get_col()) + ")"
        if self.get_player() == 'r':
            self._image = "Janggi/assets/Red_Cannon.png"
        else:
            self._image = "Janggi/assets/Blue_Cannon.png"

    def get_image(self):
        return self._image

    def set_move_key(self, new_key):
        self._move_key = new_key

    def get_move_key(self):
        return self._move_key

    def get_piece_type(self):
        """This will return the piece type."""
        return self._piece_type

    def get_piece_display(self):
        """This will return what is to be displayed on the board as the cannon piece."""
        return self._piece_display

    def get_board_display(self):
        return self._board_display


class Chariot(Piece):
    """
    This will represent the chariot piece. Child to the piece Class.

    Initialize the Chariot piece

    This Chariot inherits the Piece class and keeps track of the
    type of piece it is and how it is displayed in the show board method in
    the JanggiGame class.
    """

    def __init__(self, owned_by, row, col):
        """Initialize the Chariot piece"""
        super().__init__(owned_by, row, col)
        self._piece_type = "chariot"
        self._piece_display = "CH"
        self._board_display = self.get_player() + self.get_piece_display()
        self._chariot_moves = {}
        self._move_key = self.get_board_display() + "(" + str(self.get_row()) + "," + str(self.get_col()) + ")"
        if self.get_player() == 'r':
            self._image = "Janggi/assets/Red_Chariot.png"
        else:
            self._image = "Janggi/assets/Blue_Chariot.png"

    def get_image(self):
        return self._image

    def set_move_key(self, new_key):
        self._move_key = new_key

    def get_move_key(self):
        return self._move_key

    def get_piece_type(self):
        """This will return the piece type."""
        return self._piece_type

    def get_piece_display(self):
        """This will return what is to be displayed on the board as the chariot piece."""
        return self._piece_display

    def get_board_display(self):
        return self._board_display


class Elephant(Piece):
    """
    This will represent the elephant piece. Child to the piece Class.

    Initialize the Elephant piece

    This Elephant inherits the Piece class and keeps track of the
    type of piece it is and how it is displayed in the show board method in
    the JanggiGame class.
    """

    def __init__(self, owned_by, row, col):
        """Initialize the Elephant piece"""
        super().__init__(owned_by, row, col)
        self._piece_type = "elephant"
        self._piece_display = "EL"
        self._board_display = self.get_player() + self.get_piece_display()
        self._elephant_moves = {}
        self._move_key = self.get_board_display() + "(" + str(self.get_row()) + "," + str(self.get_col()) + ")"
        if self.get_player() == 'r':
            self._image = "Janggi/assets/Red_Elephant.png"
        else:
            self._image = "Janggi/assets/Blue_Elephant.png"

    def get_image(self):
        return self._image

    def set_move_key(self, new_key):
        self._move_key = new_key

    def get_move_key(self):
        return self._move_key

    def get_piece_type(self):
        """This will return the piece type."""
        return self._piece_type

    def get_piece_display(self):
        """This will return what is to be displayed on the board as the elephant piece."""
        return self._piece_display

    def get_board_display(self):
        return self._board_display


class Horse(Piece):
    """
    This will represent the horse piece. Child to the piece Class.

    Initialize the Horse piece

    This Horse inherits the Piece class and keeps track of the
    type of piece it is and how it is displayed in the show board method in
    the JanggiGame class.
    """

    def __init__(self, owned_by, row, col):
        """Initialize the Horse piece"""
        super().__init__(owned_by, row, col)
        self._piece_type = "horse"
        self._piece_display = "HR"
        self._board_display = self.get_player() + self.get_piece_display()
        self._soldier_moves = {}
        self._move_key = self.get_board_display() + "(" + str(self.get_row()) + "," + str(self.get_col()) + ")"
        if self.get_player() == 'r':
            self._image = "Janggi/assets/Red_Horse.png"
        else:
            self._image = "Janggi/assets/Blue_Horse.png"

    def get_image(self):
        return self._image

    def set_move_key(self, new_key):
        self._move_key = new_key

    def get_move_key(self):
        return self._move_key

    def get_piece_type(self):
        """This will return the piece type."""
        return self._piece_type

    def get_piece_display(self):
        """This will return what is to be displayed on the board as the horse piece."""
        return self._piece_display

    def get_board_display(self):
        return self._board_display


class Guard(Piece):
    """
    This will represent the guard piece. Child to the piece Class.

    Initialize the Guard piece

    This Guard inherits the Piece class and keeps track of the
    type of piece it is and how it is displayed in the show board method in
    the JanggiGame class.
    """

    def __init__(self, owned_by, row, col):
        """Initialize the Guard piece"""
        super().__init__(owned_by, row, col)
        self._piece_type = "guard"
        self._piece_display = "GR"
        self._board_display = self.get_player() + self.get_piece_display()
        self._guard_moves = {}
        self._move_key = self.get_board_display() + "(" + str(self.get_row()) + "," + str(self.get_col()) + ")"
        if self.get_player() == 'r':
            self._image = "Janggi/assets/Red_Guard.png"
        else:
            self._image = "Janggi/assets/Blue_Guard.png"

    def get_image(self):
        return self._image

    def set_move_key(self, new_key):
        self._move_key = new_key

    def get_move_key(self):
        return self._move_key

    def get_piece_type(self):
        """This will return the piece type."""
        return self._piece_type

    def get_piece_display(self):
        """This will return what is to be displayed on the board as the guard piece."""
        return self._piece_display

    def get_board_display(self):
        return self._board_display


class General(Piece):
    """
    This will represent the general piece. Child to the piece Class.

    Initialize the General piece

    This General inherits the Piece class and keeps track of the
    type of piece it is and how it is displayed in the show board method in
    the JanggiGame class.
    """

    def __init__(self, owned_by, row, col):
        """Initialize the General piece"""
        super().__init__(owned_by, row, col)
        self._piece_type = "general"
        self._piece_display = "GN"
        self._board_display = self.get_player() + self.get_piece_display()
        self._general_moves = {}
        self._move_key = self.get_board_display() + "(" + str(self.get_row()) + "," + str(self.get_col()) + ")"
        if self.get_player() == 'r':
            self._image = "Janggi/assets/Red_General.png"
        else:
            self._image = "Janggi/assets/Blue_General.png"

    def get_image(self):
        return self._image

    def set_move_key(self, new_key):
        self._move_key = new_key

    def get_move_key(self):
        return self._move_key

    def get_piece_type(self):
        """This will return the piece type."""
        return self._piece_type

    def get_piece_display(self):
        """This will return what is to be displayed on the board as the general piece."""
        return self._piece_display

    def get_board_display(self):
        return self._board_display