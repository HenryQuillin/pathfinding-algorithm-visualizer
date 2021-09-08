# Henry Quillin
# Pathfinding Algorithm Visualizer
# 5 - 19 - 2021
import pygame
from queue import PriorityQueue


rows = 50

width = rows * 20
height = rows * 12

# Initialize colors that will represent node states
CLOSED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (64, 206, 227)
YELLOW = (255, 255, 0)
EMPTY = (255, 255, 255)
WALL = (0, 0, 0)
PATH = (128, 0, 128)
START = (255, 165, 0)
GREY = (128, 128, 128)
GRID_LINE = (37, 150, 190)
END = (64, 224, 208)


# Initialize PyGame environmet
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pathfinding Algorithm Visualizer")


class Node:
    def __init__(self, row, col, node_width, total_rows):
        self.row = row
        self.col = col
        self.x = row * node_width
        self.y = col * node_width
        self.color = EMPTY
        self.neighbors = []
        self.width = node_width
        self.total_rows = total_rows
        self.total_cols = height / self.width

    def draw(self):  # draw node method
        pygame.draw.rect(
            win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        # Check that bottom node is empty node
        if self.row < self.total_rows - 1 and (grid[self.row + 1][self.col].color != WALL):
            self.neighbors.append(grid[self.row + 1][self.col])

        # Check that top node is empty node
        if self.row > 0 and (grid[self.row - 1][self.col].color != WALL):
            self.neighbors.append(grid[self.row - 1][self.col])

        # Check that right node is empty node
        if self.col < self.total_cols - 1 and (grid[self.row][self.col + 1].color != WALL):
            self.neighbors.append(grid[self.row][self.col + 1])
        # Check that left node is empty node
        if self.col > 0 and (grid[self.row][self.col - 1].color != WALL):
            self.neighbors.append(grid[self.row][self.col - 1])


def make_grid():  # Creates an array the size of the grid that contains node objects
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)

    return grid


def draw_grid():  # Draws grid lines
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GRID_LINE, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GRID_LINE, (j * gap, 0), (j * gap, width))


def draw(grid_arr):  # Draws nodes on the grid
    win.fill(EMPTY)

    for row in grid_arr:
        for node in row:
            node.draw()

    draw_grid()
    pygame.display.update()


def get_clicked_pos(pos):  # Gets the current position of the mouse
    gap = width // rows
    y = pos[0]
    x = pos[1]

    row = y // gap
    col = x // gap
    return row, col


def h(p1, p2):  # calculates the distance of a given node to the end node
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def aStar(draw, grid, start, end):
    draw()
    count = 0  # used in the case that two nodes have the same F score
    open_set = PriorityQueue()  # queue that stores the f_score, count, and node
    open_set.put((0, count, start))  # add the start node
    came_from = {}
    for row in grid:
        for node in row:
            g_score = {node: float("inf")}
    g_score[start] = 0
    for row in grid:
        for node in row:
            f_score = {node: float("inf")}
    f_score[start] = h(start.get_pos(), end.get_pos())

    # need to have an open set hash to check if an Item is in the priority queue
    open_set_hash = {start}

    while open_set.empty() == False:
        for event in pygame.event.get():  # Allows the user to quit
            if event.type == pygame.QUIT:
                pygame.quit()

        current_node = open_set.get()[2]  # gets the node from the open set


def main():  # Main loop function
    grid = make_grid()
    start = None
    end = None
    run = True
    started = False
    while run:
        draw(grid)  # passes the grid array into the draw function
        for event in pygame.event.get():  # check if the user exits the application
            if event.type == pygame.QUIT:
                run = False

            if started:  # When the simulation is started, don't allow the user to draw walls
                continue

            if pygame.mouse.get_pressed()[0]:  # If the user left clicks
                pos = pygame.mouse.get_pos()   # get the postion of the mouse
                row, col = get_clicked_pos(pos)
                node = grid[row][col]
                if not start and node != end:   # if the start and end node have not been placed
                    start = node
                    start.color = START       # place start node

                elif not end and node != start:  # if the end node has not been placed
                    end = node
                    end.color = END         # place end node

                elif node != end and node != start:   # if both the start and end node have been placed
                    node.color = WALL        # place a wall node
            if pygame.mouse.get_pressed()[2]:  # If the user right clicks
                pos = pygame.mouse.get_pos()   # get the postion of the mouse
                row, col = get_clicked_pos(pos)
                node = grid[row][col]
                node.color = EMPTY
                if node == start:
                    node = None
                elif node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started:
                    for row in grid:
                        for node in row:
                            node.update_neighbors()

                    aStar(Lambda: draw(win, grid, rows, width), grid, start, end)

    pygame.quit()


main()
