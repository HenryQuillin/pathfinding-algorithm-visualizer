import pygame
from queue import PriorityQueue


CLOSED = (255, 0, 0)
OPEN = (0, 255, 0)
BLUE = (64, 206, 227)
YELLOW = (255, 255, 0)
EMPTY = (255, 255, 255)
WALL = (0, 0, 0)
PATH = (128, 0, 128)
START = (255, 165, 0)
GREY = (128, 128, 128)
GRID_LINE = (37, 150, 190)
END = (64, 224, 208)


class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.type = EMPTY
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def draw(self, win):
        pygame.draw.rect(
            win, self.type, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        # DOWN
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].type == WALL:
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].type == WALL:  # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        # RIGHT
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].type == WALL:
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].type == WALL:  # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

    def get_pos(self): return self.row, self.col

    def __lt__(self, other):
        return False
