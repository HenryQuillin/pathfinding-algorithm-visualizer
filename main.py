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


WIDTH = 800
ROWS = 40
BLACK_NODE_HEIGHT = 75
UI_HEIGHT = 90
UI_LENGTH = WIDTH + 7
UI_BUTTON_HEIGHT = 50
UI_PANEL_MIDPOINT = UI_LENGTH / 2
UI_BUTTON_Y_POS = UI_HEIGHT/2 - UI_BUTTON_HEIGHT/2
WIN = pygame.display.set_mode((WIDTH, WIDTH))
SMALL_BTN_LENGTH = 100
LARGE_BTN_LENGTH = 150
GAP = 0

pygame.display.set_caption("Pathfinding Algorithm Visualizer")

manager = pygame_gui.UIManager((800, 600))
clock = pygame.time.Clock()
store = Store()

ui_panel = pygame_gui.elements.ui_panel.UIPanel(relative_rect=pygame.Rect((-5, -5), (UI_LENGTH, UI_HEIGHT)),
                                                starting_layer_height=1,
                                                manager=manager)
analytics_panel = pygame_gui.elements.ui_panel.UIPanel(relative_rect=pygame.Rect((UI_PANEL_MIDPOINT-(LARGE_BTN_LENGTH/2)+300, UI_HEIGHT-12), (175, 300)),
                                                starting_layer_height=2,
                                                manager=manager)
start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((UI_PANEL_MIDPOINT-(SMALL_BTN_LENGTH/2)-50, UI_BUTTON_Y_POS), (SMALL_BTN_LENGTH, UI_BUTTON_HEIGHT)),
                                            text='START',
                                            manager=manager,
                                            container=ui_panel)
clear_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((UI_PANEL_MIDPOINT-(SMALL_BTN_LENGTH/2)+50, UI_BUTTON_Y_POS), (SMALL_BTN_LENGTH, UI_BUTTON_HEIGHT)),
                                            text='CLEAR',
                                            manager=manager,
                                            container=ui_panel)
algorithm_dropdown = pygame_gui.elements.UIDropDownMenu(relative_rect=pygame.Rect((UI_PANEL_MIDPOINT-(LARGE_BTN_LENGTH/2)-200, UI_BUTTON_Y_POS-2), (150, UI_BUTTON_HEIGHT)),
                                                        options_list=[
                                                            "A Star", "Breadth FS", "Best FS"],
                                                        starting_option="A Star",
                                                        manager=manager,
                                                        )
heuristic_dropdown = pygame_gui.elements.UIDropDownMenu(relative_rect=pygame.Rect((UI_PANEL_MIDPOINT-(LARGE_BTN_LENGTH/2)+200, UI_BUTTON_Y_POS-2), (150, UI_BUTTON_HEIGHT)),
                                                        options_list=[
                                                            "Show Heuristic", "Hide Heuristic"],
                                                        starting_option="Show Heuristic",
                                                        manager=manager,
                                                        )
analytics_text_box = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((0,0), (175, 300)),
                                                   manager=manager, container=analytics_panel,

                                                   html_text=""" <strong><u><font color=’#F25400’ size=3.5>Analytics</font></u></strong>"""
                                                   
                                                   )


def start_button_pressed(draw, grid, store):
    print('start pressed')
    # clear_path(WIN, grid, ROWS, WIDTH)
    if store.start and store.end:
        for row in grid:
            for node in row:
                node.update_neighbors(grid)
        if store.algorithm_selected == "A Star":
            algorithms.A_star(WIN, draw,
                              grid, store.start, store.end, store)
        if store.algorithm_selected == "BFS":
            algorithms.BFS(WIN, draw,
                           grid, store.start, store.end, store)
        if store.algorithm_selected == "Best FS":
            algorithms.Best_FS(WIN, draw,
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

# def clear_path(win, grid, rows, width):

#     for row in grid:
#         for node in row:
#             if node.type is not START and node.type is not END and node.type is not WALL:
#                 node.type = EMPTY
#                 node.draw(win)


#     pygame.display.update()


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


def draw_gui(grid):

    for row in grid:
        for node in row:
            if node.y < BLACK_NODE_HEIGHT:
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
    UI_button_hovered = False
    draw_gui(grid)

    while run:
        time_delta = clock.tick(60)/1000.0

        draw(win, grid, ROWS, width)

        for event in pygame.event.get():
            time_delta = clock.tick(60)/1000.0

            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            elif event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_ON_HOVERED:
                    UI_button_hovered = True
                if event.user_type == pygame_gui.UI_BUTTON_ON_UNHOVERED:
                    UI_button_hovered = False

                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:  
                    if event.ui_element == start_button: # START BUTTON
                        start_button_pressed(draw_func, grid, store)
                        analytics_text_box.html_text = analytics_text_box.html_text + '<font color=’#F25400’ size=3.5><br> {2} <br> Nodes Searched: {0} <br> Nodes Seen: {1}<br></font>'.format(algorithms.nodes_searched,algorithms.nodes_seen, store.algorithm_selected)
                        analytics_text_box.rebuild()
                    if event.ui_element == clear_button:   # Clear button
                        reset()
                if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:  # drop down
                    if event.ui_element == algorithm_dropdown:
                        if event.text == "A Star":
                            store.algorithm_selected = "A Star"
                            heuristic_dropdown.show()
                        if event.text == "Breadth FS":
                            store.algorithm_selected = "BFS"
                            heuristic_dropdown.hide()
                        if event.text == "Best FS":
                            store.algorithm_selected = "Best FS"
                            heuristic_dropdown.show()

                    elif event.ui_element == heuristic_dropdown:
                        if event.text == "Show Heuristic":
                            store.heuristic_toggled = True
                            print(store.algorithm_selected)
                        if event.text == "Hide Heuristic":
                            store.heuristic_toggled = False

            elif pygame.mouse.get_pressed()[0]:  # LEFT
                if UI_button_hovered == False:
                    pos = pygame.mouse.get_pos()
                    row, col = get_clicked_pos(pos, ROWS, width)
                    node = grid[row][col]
                    if not store.start and node != store.end and node.y > BLACK_NODE_HEIGHT:
                        store.start = node
                        store.start.type = START

                    elif not store.end and node != store.start and node.y > BLACK_NODE_HEIGHT:
                        store.end = node
                        store.end.type = END
                    elif node != store.end and node != store.start and node.y > BLACK_NODE_HEIGHT:
                        node.type = WALL

            elif pygame.mouse.get_pressed()[2]:  # RIGHT
                if UI_button_hovered == False:

                    pos = pygame.mouse.get_pos()
                    row, col = get_clicked_pos(pos, ROWS, width)
                    node = grid[row][col]
                    if node.y > BLACK_NODE_HEIGHT:
                        node.type = EMPTY
                        if node == store.start:
                            store.start = None
                        elif node == store.end:
                            store.end = None

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
