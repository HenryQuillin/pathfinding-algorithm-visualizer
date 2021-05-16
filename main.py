import pygame
import math
from queue import PriorityQueue

width = 800
height = 600

CLOSED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (64, 206, 227)
YELLOW = (255, 255, 0)
EMPTY = (255, 255, 255)
WALL = (0, 0, 0)
PATH = (128, 0, 128)
START = (255, 165, 0)
GREY = (128, 128, 128)
END = (64, 224, 208)

ROWS = 50

WIN = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pathfinding Algorithm Visualizer")



class Node:
    def __init__(self, row, col, node_width):
        self.row = row
        self.col = col
        self.x = row * node_width
        self.y = col * node_width
        self.color = EMPTY
        self.neighbors = []
        self.width = node_width

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
            node = Node(i, j, gap)
            grid[i].append(node)

    return grid


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid_arr, rows, width):
    win.fill(EMPTY)

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
                row, col = get_clicked_pos(pos, rows, width)
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    start.make_start()

                elif not end and node != start:
                    end = node
                    end.make_end()

                elif node != end and node != start:
                    node.make_barrier()
                

    pygame.quit()


main(WIN, width)
