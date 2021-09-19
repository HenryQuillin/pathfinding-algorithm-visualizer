from pygame.event import clear
import main
import queue
import pygame
import algorithms
import pygame_gui

from node import Node
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

manager = pygame_gui.UIManager((800, 600))
clock = pygame.time.Clock()

start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH/2 -100, 15), (100, 50)),
                                             text='START',
                                             manager=manager)
clear_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH/2, 15), (100, 50)),
                                             text='END',
                                             manager=manager)

store = Store()


def start_button_pressed(draw, grid, store):
    print('start pressed')
    if store.start and store.end:
        for row in grid:
            for node in row:
                node.update_neighbors(grid)

        algorithms.BFS(WIN, draw,
            grid, store.start, store.end, store)



CLOSED = "#00F2DE"
OPEN = "#C1F200"  
BLUE = (64, 206, 227)
YELLOW = (255, 255, 0)
EMPTY = (255, 255, 255)
WALL = "#103444"
PATH = "#9900F2"
START = "#F25400"
LINE = (70, 102, 255)
GRID_LINE = (176, 220, 252)
END = "#F2007C"

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
    pass


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
    manager.draw_ui(WIN)

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
    def draw_func(): return draw(win, grid, ROWS, width)
    run = True
    draw_gui(grid)

    while run:
        time_delta = clock.tick(60)/1000.0


        draw(win, grid, ROWS, width)
        
        for event in pygame.event.get():
            time_delta = clock.tick(60)/1000.0

            if event.type == pygame.QUIT:
                run = False 
                pygame.quit()

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

            if pygame.mouse.get_pressed()[2]:  # RIGHT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                if node.y > GUI_HEIGHT:
                    node.type = EMPTY
                    if node == store.start:
                        store.start = None
                    elif node == store.end:
                        store.end = None
                        
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED: #START BUTTON 
                    if event.ui_element == start_button:
                        start_button_pressed(draw_func, grid, store)
                    if event.ui_element == clear_button:
                        reset()
                if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED: 
                    if event.ui_element == algorithm_dropdown:
                        if event.text == "A Star":
                            pass 
                        if event.text == "Best First Search":
                            pass 
                    if event.ui_element == heuristic_dropdown:
                        pass

                
                


            manager.process_events(event)

        manager.update(time_delta)
        # start_button.user_func = start_button_pressed
        # def draw_func(): return draw(win, grid, ROWS, width)
        # start_button.user_params = {"draw": draw_func,
        #                             "grid": grid, "start": store.start, "end": store.end}
        # reset_button.user_func = reset
        # heuristic_checkbox.user_func = heuristic_checkbox_toggled
        # # heuristic_checkbox.user_params = heuristic_checkbox.get_state()
        # menu.react(event)



    pygame.quit()


main(WIN, WIDTH)
