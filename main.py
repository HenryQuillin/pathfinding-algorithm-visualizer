import pygame
from queue import PriorityQueue
from store import Store

from thorpy.elements.background import Background
from node import Node
import thorpy

CLOSED = "#00F2DE"
OPEN =  "#C1F200"#(64,224,208)
BLUE = (64, 206, 227)
YELLOW = (255, 255, 0)
EMPTY = (255, 255, 255)
WALL = "#103444"
PATH = "#9900F2"
START = "#F25400"
LINE = (70, 102, 255)
GRID_LINE = (176,220,252)
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

        A_star(draw,
                grid, start, end)




start_button = thorpy.make_button("START")
reset_button = thorpy.make_button("RESET")
start_button.set_painter(rect_painter)
reset_button.set_painter(rect_painter)
start_button.finish()
reset_button.finish()
box = thorpy.Box(elements=[start_button, reset_button])
thorpy.store(box, mode="h")
box.fit_children()
background = thorpy.Background()

# we regroup all elements on a menu, even if we do not launch the menu
menu = thorpy.Menu(box)




def h_score(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.type = PATH
        draw()


def A_star(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = h_score(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.type = END
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + \
                    h_score(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.type = OPEN

        draw()

        if current != start:
            current.type = CLOSED

    return False


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
        box.center(None,-260)
        box.blit()
        box.update()


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
    grid = store.grid 
    grid = []
    gap = WIDTH // ROWS
    for i in range(ROWS):
        grid.append([])
        for j in range(ROWS):
            node = Node(i, j, gap, ROWS)
            grid[i].append(node)

    draw_gui(grid)

    return grid
    # store.start = None 
    # store.end = None 
    # print('reset') 
    # for row in grid:
    #     for node in row:
    #        if node.y > GUI_HEIGHT:
    #         node.type = EMPTY   
    # store.grid = grid 
    #return store.grid 


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
                if not store.start and node != end and node.y > GUI_HEIGHT:
                    store.start = node
                    store.start.type = START

                elif not end and node != store.start:
                    end = node
                    end.type = END
                elif node != end and node != store.start:
                    node.type = WALL

            elif pygame.mouse.get_pressed()[2]:  # RIGHT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                if node.y > GUI_HEIGHT:
                    node.type = EMPTY
                    if node == store.start:
                        store.start = None
                    elif node == end:
                        end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    store.start = None
                    end = None
                    grid = reset()
            

        start_button.user_func = start_button_pressed
        draw_func = lambda: draw(win, grid, ROWS, width)
        start_button.user_params = {"draw": draw_func,
                        "grid": grid, "start": store.start, "end":end}
        reset_button.user_func = reset
        #reset_button.user_params =
        menu.react(event)


    pygame.quit()


main(WIN, WIDTH)
