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
    state = dict(pause=False, selecting=False, clear=False, init=False, gliders=0)
    clock = pygame.time.Clock()
    screen = create_screen()
    board = add_gliders([], 10)

    while True:
        state = handle_events(state)

        if state["gliders"]:
            board = add_gliders(board, state["gliders"])

        if state["clear"]:
            board = []

        if not state["pause"] and not state["selecting"]:
            board = update(board)
        elif "step" in state:
            board = update(board)

        if "select" in state:
            for pos in state["select"]:
                if pos not in board:
                    board.append(pos)

        draw(screen, board, state["pause"])
        pygame.display.update()
        clock.tick(FRAME_RATE)


def add_gliders(board, count):
    new_board = board.copy()

    """Place the specified amount of gliders on the board"""
    for i in range(count):
        dx, dy = int(random() * WIDTH), int(random() * HEIGHT)
        translated_glider = [(x + dx, y + dy) for (x, y) in GLIDER]
        new_board.extend(translated_glider)

    return new_board


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


def draw(screen, board, paused):
    """Draw the board on the screen"""
    draw_fade(screen, 0.25)
    draw_live_cells(screen, board)
    draw_grid(screen, paused)


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


def draw_grid(screen, paused):
    """Draw grid lines on top of everything"""
    color = GRID_COLOR if paused else BACK_COLOR
    for y in range(HEIGHT):
        for x in range(WIDTH):
            rect = pygame.Rect(x * ZOOM, y * ZOOM, ZOOM, ZOOM)
            pygame.draw.rect(screen, color, rect, 1)


def handle_events(state):
    """Quit on keypress"""
    new_state = dict(pause=state["pause"], selecting=state["selecting"], select=[], clear=False, gliders=0)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            new_state["pause"] = not state["pause"]
        elif event.type == pygame.KEYDOWN and event.key >= pygame.K_0 and event.key <= pygame.K_9:
            new_state["gliders"] = event.key - pygame.K_0
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
            new_state["clear"] = True
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_n:
            new_state["step"] = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            new_state["selecting"] = True
            pos = (event.pos[0] // ZOOM, event.pos[1] // ZOOM)
            new_state["select"].append(pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            new_state["selecting"] = False
        elif event.type == pygame.MOUSEMOTION and new_state["selecting"]:
            pos = (event.pos[0] // ZOOM, event.pos[1] // ZOOM)
            if pos not in new_state["select"]:
                new_state["select"].append(pos)
        elif event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and (event.key == pygame.K_q or event.key == pygame.K_ESCAPE)):
            pygame.quit()
            sys.exit()

    return new_state


def create_screen():
    """Initialize pygame window"""
    pygame.init()
    pygame.display.set_caption("Game of Life")
    screen = pygame.display.set_mode((WIDTH * ZOOM, HEIGHT * ZOOM), pygame.DOUBLEBUF)
    screen.fill(BACK_COLOR)

    return screen


if __name__ == "__main__":
    main()
