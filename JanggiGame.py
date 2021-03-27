import pygame
from Janggi.constants import *
from Janggi.board import Board
from Janggi.button import Button

pygame.display.set_caption('Janggi')
pygame.font.init()
font = pygame.font.SysFont(None, 24)

FPS = 60

# clock = pygame.time.Clock()
# WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
# board = Board()
# game_state = board.get_game_state()


def get_mouse_on_board_position(mouse_position):
    x, y = mouse_position
    col = (x // ((WIDTH - PADDING_ON_LEFT - PADDING_ON_TOP) // COLS)) - 1
    row = (y // ((HEIGHT - PADDING_ON_LEFT - PADDING_ON_TOP) // ROWS)) - 1
    return row, col

def game_loop():
    clock = pygame.time.Clock()
    WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
    board = Board()
    game_state = board.get_game_state()

    reset_image = pygame.image.load("Janggi/assets/refresh-64x64.png")
    reset_image = pygame.transform.scale(reset_image, ((SQUARE_SIZE // 2), (SQUARE_SIZE // 2)))
    # reset_button = Button(BLACK, (PADDING_ON_LEFT + ROWS * 2), HEIGHT, reset_image.get_width(), reset_image.get_height())
    reset_button = Button(JANGGI_BOARD_COLOR, (WIDTH - reset_image.get_width()), HEIGHT - reset_image.get_height(),
                          (reset_image.get_width()), (reset_image.get_height()))
    while game_state == 'UNFINISHED':
        # Sets a constant frame rate for the game, and lets the game run at a consistent speed
        clock.tick(FPS)
        for event in pygame.event.get():

            # Pressed the red X to close the game
            if event.type == pygame.QUIT:
                run = False
            # If a button is pressed down on the mouse
            if event.type == pygame.MOUSEBUTTONDOWN:

                mouse_position = pygame.mouse.get_pos()
                if reset_button.is_over(mouse_position):
                    board.reset()
                row, col = get_mouse_on_board_position(mouse_position)
                if row not in range(0, 10) or col not in range(0, 9):
                    continue
                if board.get_piece_from_board(row, col) is False:
                    continue
                # key = next(iter(board.get_board()[row][col].keys()))
                piece = board.get_piece_from_board(row, col)
                # Button is right-click
                if event.button == 3:
                    # TODO make right click view all possible moves for the player_turn or other player.
                    pass
                if event.button == 1:
                    # If a piece is not selected continue
                    if not board.select_piece(row, col, WINDOW):
                        continue
                    board.select_piece(row, col, WINDOW)
                    # attempt to find a move
                    if not board.piece_is_selected(piece, WINDOW):
                        continue
                    board.piece_is_selected(piece, WINDOW)

                    board.set_pieces(board.update_pieces(board.get_board()))
                    board.place_on_board(WINDOW, board.get_pieces())
                    board.swap_player_turn(board.get_player_turn())

                    # print(board.get_player_turn())
        board.draw_board(WINDOW)
        reset_button.draw_button(WINDOW, "Janggi/assets/refresh-64x64.png")
        pygame.display.update()
        if board.get_game_state() == "UNFINISHED":
            pass
        else:
            print("GAME_OVER")
            reset_loop(WINDOW, board)
    pygame.quit()

def reset_loop(window, board):

    reset_image = pygame.image.load("Janggi/assets/refresh-64x64.png")
    reset_image_big = pygame.transform.rotozoom(reset_image, 0, 2)
    # reset_button = Button(BLACK, (PADDING_ON_LEFT + ROWS * 2), HEIGHT, reset_image.get_width(), reset_image.get_height())

    game_over_button = Button(JANGGI_BOARD_COLOR, (WIDTH - SQUARE_SIZE), HEIGHT//2, reset_image_big.get_height()//4, reset_image_big.get_width()//4)
    reset_image_big = reset_image_big.get_rect()
    reset_image_big.width, reset_image_big.height = WIDTH - game_over_button.get_width(), HEIGHT//2 - game_over_button.get_height()
    game_over = True
    while game_over:

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:

                mouse_position = pygame.mouse.get_pos()
                if game_over_button.is_over(mouse_position):
                    board.reset()
                    game_loop()


        board.draw_board(window)

        # reset_button.draw_button(window, "Janggi/assets/refresh-64x64.png")
        game_over_button.draw_button(window, "Janggi/assets/refresh-64x64.png")
        pygame.display.update()

def main():
    # board.place_on_board(WINDOW, board.get_pieces())
    game_loop()

if __name__ == '__main__':
    main()
