import pygame
import math
from queue import PriorityQueue

width = 800
height = 600

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (64, 206, 227)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

WIN = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pathfinding Algorithm Visualizer")


class Node:
    def __init__(self, row, col, node_width, total_rows):
        self.row = row
        self.col = col
        self.x = row * node_width
        self.y = col * node_width
        self.color = WHITE
        self.neighbors = []
        self.width = node_width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(
            win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        pass

    def __lt__(self, other):
        return False


def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)

    return grid


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid_arr, rows, width):
    win.fill(WHITE)

    for row in grid_arr:
        for node in row:
            node.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y = pos[0]
    x = pos[1]

    row = y // gap
    col = x // gap
    return row, col


def main(win, width):
    rows = 50
    grid = make_grid(rows, width)
    start = None
    end = None
    run = True
    started = False
    while run:
        draw(win, grid, rows, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if started:
                continue

                if pygame.mouse.get_pressed()[0]:  # LEFT
                    pos = pygame.mouse.get_pos()
                     row, col = get_clicked_pos(pos, ROWS, width)
                      spot = grid[row][col]
                       if not start and spot != end:
                            start = spot
                            start.make_start()

                        elif not end and spot != start:
                            end = spot
                            end.make_end()

                        elif spot != end and spot != start:
                            spot.make_barrier()

    pygame.quit()


main(WIN, width)
