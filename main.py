import main
import queue 
import pygame

from thorpy.elements.background import Background
from node import Node
import thorpy
#from A_Star import A_star
from store import Store


CLOSED = "#00F2DE"
OPEN = "#C1F200"  # (64,224,208)
BLUE = (64, 206, 227)
YELLOW = (255, 255, 0)
EMPTY = (255, 255, 255)
WALL = "#103444"
PATH = "#9900F2"
START = "#F25400"
LINE = (70, 102, 255)
GRID_LINE = (176, 220, 252)
END = "#F2007C"

pygame.init()

GUI_HEIGHT = 75
WIDTH = 600
ROWS = 30
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding A_star")

rect_painter = thorpy.painters.roundrect.RoundRect(size=(50, 50),
                                                   color=(255, 255, 55),
                                                   radius=0.3)


store = Store()


def start_button_pressed(draw, grid, start, end):
    print('start pressed')
    if start and end:
        for row in grid:
            for node in row:
                node.update_neighbors(grid)

        BFS(draw,
            grid, start, end)
        # BFS(draw,
        #         grid, start, end)


CLOSED = "#00F2DE"
OPEN = "#C1F200"  # (64,224,208)
BLUE = (64, 206, 227)
YELLOW = (255, 255, 0)
EMPTY = (255, 255, 255)
WALL = "#103444"
PATH = "#9900F2"
START = "#F25400"
LINE = (70, 102, 255)
GRID_LINE = (176, 220, 252)
END = "#F2007C"


def BFS(draw, grid, start, end):
    count = 0
    open_set = queue.Queue()
    open_set.put((count, start))
    came_from = {}

    open_set_hash = {start}

    while open_set:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[1]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.type = END
            return True

        for neighbor in current.neighbors:

            if neighbor.type is not OPEN and neighbor.type is not CLOSED and neighbor is not start:
                came_from[neighbor] = current
                count += 1
                open_set.put((count, neighbor))
                open_set_hash.add(neighbor)
                neighbor.type = OPEN

        draw()

        if current != start:
            current.type = CLOSED

    return False


start_button = thorpy.make_button("START")
reset_button = thorpy.make_button("RESET")

heuristic_button = [thorpy.Togglable("Heuristic"+str(i)) for i in range(2)]
heuristic_button_pool = thorpy.TogglablePool(heuristic_button, first_value=heuristic_button[0],
                                             always_value=False)

heuristic_checkbox = thorpy.CheckBox(
    "Visualize Heuristic", type_="checkbox", value=True)
start_button.set_painter(rect_painter)
heuristic_checkbox.set_painter(rect_painter)
reset_button.set_painter(rect_painter)
heuristic_checkbox.finish()
start_button.finish()
reset_button.finish()
box = thorpy.Box(elements=[start_button, reset_button, heuristic_checkbox])
#box2 = thorpy.Box(elements=[heuristic_checkbox])
thorpy.store(box, mode="h")
box.fit_children()
background = thorpy.Background()

# we regroup all elements on a menu, even if we do not launch the menu
menu = thorpy.Menu([box])


def h_score(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        if current.type is not START and current.type is not END:
            current.type = PATH
        draw()


def draw_heuristic(node):
    if store.heuristic_toggled:
        pygame.draw.line(WIN, "#F2007C", (store.start.x,
                         store.start.y), (node.x, node.y))
        pygame.draw.line(WIN, "#9900F2", (node.x, node.y),
                         (store.end.x, store.end.y))
        pygame.display.update()


def heuristic_checkbox_toggled():
    print('heuristic funciton called')
    store.count = store.count + 1
    if (store.count % 2) == 1:  # count is odd
        store.heuristic_toggled = False
    if (store.count % 2) == 0:  # count is even
        store.heuristic_toggled = True


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)

    return grid


def draw_buttons():
    # important : set the screen as surface for all elements
    for element in menu.get_population():
        element.surface = WIN
        # use the elements normally...
        box.center(None, -260)

        box.blit()
        box.update()
        # heuristic_button_pool.center(100,-260)
        # heuristic_button_pool.blit()
        # heuristic_button_pool.update()


def draw_grid(win, rows, width):
    gap = width // rows

    for i in range(rows):
        pygame.draw.line(win, LINE, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, LINE, (j * gap, 0), (j * gap, width))
    draw_buttons()


def draw(win, grid, rows, width):
    win.fill(EMPTY)

    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


def draw_gui(grid):

    for row in grid:
        for node in row:
            if node.y < GUI_HEIGHT:
                node.type = WALL
    pygame.display.update()


def reset():
    store.start = None
    store.end = None
    main(WIN, WIDTH)


def main(win, width):
    grid = store.grid
    grid = make_grid(ROWS, width)
    end = store.end

    run = True
    draw_gui(grid)

    while run:

        draw(win, grid, ROWS, width)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:  # LEFT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                if not store.start and node != store.end and node.y > GUI_HEIGHT:
                    store.start = node
                    store.start.type = START

                elif not store.end and node != store.start and node.y > GUI_HEIGHT:
                    store.end = node
                    store.end.type = END
                elif node != store.end and node != store.start and node.y > GUI_HEIGHT:
                    node.type = WALL

            elif pygame.mouse.get_pressed()[2]:  # RIGHT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                if node.y > GUI_HEIGHT:
                    node.type = EMPTY
                    if node == store.start:
                        store.start = None
                    elif node == store.end:
                        store.end = None

            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_c:
            #         store.start = None
            #         store.end = None
            #         grid = reset()

        start_button.user_func = start_button_pressed
        def draw_func(): return draw(win, grid, ROWS, width)
        start_button.user_params = {"draw": draw_func,
                                    "grid": grid, "start": store.start, "end": store.end}
        reset_button.user_func = reset
        heuristic_checkbox.user_func = heuristic_checkbox_toggled
        # heuristic_checkbox.user_params = heuristic_checkbox.get_state()
        menu.react(event)

    pygame.quit()


main(WIN, WIDTH)
