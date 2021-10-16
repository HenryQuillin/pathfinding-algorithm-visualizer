import pygame
from queue import PriorityQueue
from store import Store


CLOSED = "#00F2DE"
OPEN =  "#C1F200"
EMPTY = "#FFFFFF"
WALL = "#103444"
PATH = "#9900F2"
START = "#F25400"
END = "#F2007C"         

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
