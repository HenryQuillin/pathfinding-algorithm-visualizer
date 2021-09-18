
import pygame
from queue import PriorityQueue
import main


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

def BFS(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((count, start))
    came_from = {}

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[1]
        open_set_hash.remove(current)

        if current == end:
            main.reconstruct_path(came_from, end, draw)
            end.type = END
            return True

        for neighbor in current.neighbors:
            came_from[neighbor] = current

            if neighbor not in open_set_hash:
                count += 1
                open_set.put((count, neighbor))
                open_set_hash.add(neighbor)
                neighbor.type = OPEN
                main.draw_heuristic(neighbor)

        draw()

        if current != start:
            current.type = CLOSED

    return False
