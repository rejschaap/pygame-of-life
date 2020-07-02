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


def main():
    """Your basic game loop"""
    state = {}
    clock = pygame.time.Clock()
    screen = create_screen()
    board = add_gliders([], 10)

    while True:
        state = handle_events(state)
        board = update(board, state)
        draw(screen, board, state["pause"])
        pygame.display.update()
        clock.tick(FRAME_RATE)


def add_gliders(current_board, count):
    """Place the specified amount of gliders on the board"""
    GLIDER = [(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
    next_board = current_board.copy()

    for i in range(count):
        dx, dy = int(random() * WIDTH), int(random() * HEIGHT)
        translated_glider = [(x + dx, y + dy) for (x, y) in GLIDER]
        next_board.extend(translated_glider)

    return next_board


def update(current_board, state):
    """Update the game board based on the control state"""
    board = [] if state["clear"] else current_board.copy()

    if not(state["pause"] or state["selecting"]) or state["step"]:
        board = step(board)

    if "select" in state:
        for pos in state["select"]:
            if pos not in board:
                board.append(pos)

    board = add_gliders(board, state["gliders"])

    return board


def step(current_board):
    """Update the cells in the board according to the Game of Life rules"""
    next_board = []

    for y in range(HEIGHT):
        for x in range(WIDTH):
            count = count_neighbours(current_board, x, y)

            if (x, y) in current_board and (count == 2 or count == 3):
                next_board.append((x, y))
            elif (x, y) not in current_board and count == 3:
                next_board.append((x, y))

    return next_board


def count_neighbours(state, x, y):
    """Returns the number of neighbours that are live"""
    count = 0

    for j in range(y - 1, y + 2):
        for i in range(x - 1, x + 2):
            is_neighbour_alive = (i % WIDTH, j % HEIGHT) in state
            is_self = (i, j) == (x, y)
            if not is_self and is_neighbour_alive:
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
    """Handle keyboard and mouse events and update state accordingly"""
    pause = state.get("pause", False)
    selecting = state.get("selecting", False)
    select = set()
    clear = False
    gliders = 0
    step = False

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            pause = not pause
        elif (
            event.type == pygame.KEYDOWN
            and event.key >= pygame.K_0
            and event.key <= pygame.K_9
        ):
            gliders = event.key - pygame.K_0
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
            clear = True
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_n:
            step = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            selecting = True
            select.add(get_position(event))
        elif event.type == pygame.MOUSEBUTTONUP:
            selecting = False
        elif event.type == pygame.MOUSEMOTION and selecting:
            select.add(get_position(event))
        elif (
            event.type == pygame.QUIT
            or event.type == pygame.KEYDOWN and event.key == pygame.K_q
            or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        ):
            pygame.quit()
            sys.exit()

    return dict(
        pause=pause,
        selecting=selecting,
        select=select,
        step=step,
        clear=clear,
        gliders=gliders,
    )


def get_position(event):
    """Get cell for mouse position"""
    return (event.pos[0] // ZOOM, event.pos[1] // ZOOM)


def create_screen():
    """Initialize pygame window"""
    pygame.init()
    pygame.display.set_caption("Game of Life")
    screen = pygame.display.set_mode((WIDTH * ZOOM, HEIGHT * ZOOM), pygame.DOUBLEBUF)
    screen.fill(BACK_COLOR)

    return screen


if __name__ == "__main__":
    main()
