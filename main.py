import pygame
from random import random
import sys

WIDTH = 32
HEIGHT = 20

BACK_COLOR = (38, 82, 153)
FRONT_COLOR = (112, 147, 204)
GRID_COLOR = (42, 88, 164)

ZOOM = 32
FRAME_RATE = 15

GLIDER = [(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)]


def main():
    clock = pygame.time.Clock()
    screen = create_screen()
    board = init_with_gliders(10)

    while True:
        handle_events()
        board = update(board)
        draw(screen, board)
        pygame.display.update()
        clock.tick(FRAME_RATE)


def init_with_gliders(count):
    """Place the specified amount of gliders on the board"""
    board = []

    for i in range(count):
        dx, dy = int(random() * WIDTH), int(random() * HEIGHT)
        translated_glider = [(x + dx, y + dy) for (x, y) in GLIDER]
        board.extend(translated_glider)

    return board


def update(board):
    """Update the cells in the board according to the Game of Life rules"""
    next_board = []

    for y in range(HEIGHT):
        for x in range(WIDTH):
            count = count_neighbours(board, x, y)

            if (x, y) in board and (count == 2 or count == 3):
                next_board.append((x, y))
            elif (x, y) not in board and count == 3:
                next_board.append((x, y))

    return next_board


def count_neighbours(state, x, y):
    """Returns the number of neighbours that are live"""
    count = 0

    for j in range(y - 1, y + 2):
        for i in range(x - 1, x + 2):
            isNeighbourAlive = (i%WIDTH, j%HEIGHT) in state 
            isSelf = (i, j) == (x, y) 
            if not isSelf and isNeighbourAlive:
                count += 1

    return count


def draw(screen, board):
    """Draw the board on the screen"""
    draw_fade(screen, 0.25)
    draw_live_cells(screen, board)
    draw_grid(screen)


def draw_fade(screen, percentage):
    """Fade screen with specified percentage"""
    s = pygame.Surface((WIDTH * ZOOM, HEIGHT * ZOOM))
    s.set_alpha(int(255 * percentage))
    s.fill(BACK_COLOR)
    screen.blit(s, (0, 0))


def draw_live_cells(screen, board):
    """Draw all cells currently live"""
    for (x, y) in board:
        rect = pygame.Rect(x * ZOOM, y * ZOOM, ZOOM, ZOOM)
        pygame.draw.rect(screen, FRONT_COLOR, rect, 0)


def draw_grid(screen):
    """Draw grid lines on top of everything"""
    for y in range(HEIGHT):
        for x in range(WIDTH):
            rect = pygame.Rect(x * ZOOM, y * ZOOM, ZOOM, ZOOM)
            pygame.draw.rect(screen, GRID_COLOR, rect, 1)


def handle_events():
    """Quit on keypress"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
            pygame.quit()
            sys.exit()


def create_screen():
    """Initialize pygame window"""
    pygame.init()
    pygame.display.set_caption("Game of Life")
    screen = pygame.display.set_mode((WIDTH * ZOOM, HEIGHT * ZOOM), pygame.DOUBLEBUF)
    screen.fill(BACK_COLOR)

    return screen


if __name__ == "__main__":
    main()
