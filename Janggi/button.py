import pygame
from .constants import *


class Button:
    def __init__(self, background_color, x_coord, y_coord, width, height):
        self._background_color = background_color
        self._x_coord = x_coord
        self._y_coord = y_coord
        self._width = width
        self._height = height

    def draw_button(self, window, image_location=None):

        pygame.draw.rect(window, self.get_background_color(), (self.get_x_coord(), self.get_y_coord(), self.get_width(), self.get_height()), 0)
        if image_location:
            image = pygame.image.load(image_location)
            image = pygame.transform.scale(image, ((SQUARE_SIZE//4), (SQUARE_SIZE//4)))
            window.blit(image, (self.get_x_coord(), self.get_y_coord()))

    def is_over(self, mouse_pos):
        if self.get_x_coord() < mouse_pos[0] < self.get_x_coord() + self.get_width():
            if self.get_y_coord() < mouse_pos[1] < self.get_y_coord() + self.get_height():
                return True
        return False

    def get_background_color(self):
        return self._background_color

    def get_x_coord(self):
        return self._x_coord

    def get_y_coord(self):
        return self._y_coord

    def get_width(self):
        return self._width

    def get_height(self):
        return self._height
