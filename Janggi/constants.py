import pygame


WIDTH, HEIGHT = 800, 800
ROWS = 9
COLS = 10
SQUARE_SIZE = WIDTH // COLS
PADDING_ON_LEFT = 80
PADDING_ON_TOP = 80
PADDING = (SQUARE_SIZE-(PADDING_ON_TOP//2)) // ROWS
RADIUS = SQUARE_SIZE//PADDING

JANGGI_BOARD_COLOR = (255, 174, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
POSSIBLE_MOVE = (40, 189, 189)
