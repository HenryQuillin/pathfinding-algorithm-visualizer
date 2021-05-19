# Henry Quillin 
# Pathfinding Algorithm Visualizer 
# 5 - 19 - 2021 
import pygame


width = 800
height = 600
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
END = (64, 224, 208)

rows = 50

# Initialize PyGame environmet 
win = pygame.display.set_mode((width, height))
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

    def draw(self):  # draw node method 
        pygame.draw.rect(
            win, self.color, (self.x, self.y, self.width, self.width))


def make_grid(): # Creates an array the size of the grid that contains node objects 
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap)
            grid[i].append(node)

    return grid


def draw_grid():  # Draws grid lines 
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(grid_arr): # Draws nodes on the grid 
    win.fill(EMPTY)

    for row in grid_arr:
        for node in row:
            node.draw()

    draw_grid()
    pygame.display.update()


def get_clicked_pos(pos): # Gets the current position of the mouse 
    gap = width // rows
    y = pos[0]
    x = pos[1]

    row = y // gap
    col = x // gap
    return row, col


def main():  # Main loop function
    grid = make_grid()
    start = None
    end = None
    run = True
    started = False
    while run: 
        draw(grid) # passes the grid array into the draw function 
        for event in pygame.event.get(): # check if the user exits the application 
            if event.type == pygame.QUIT:
                run = False

            if started: # When the simulation is started, don't allow the user to draw walls 
                continue

            if pygame.mouse.get_pressed()[0]:  # If the user left clicks 
                pos = pygame.mouse.get_pos().   # get the postion of the mouse 
                row, col = get_clicked_pos(pos)
                node = grid[row][col]                         
                if not start and node != end   # if the start and end node have not been placed
                    start = node                 
                    start.color = START       # place start node

                elif not end and node != start:  # if the end node has not been placed
                    end = node
                    end.color = END         # place end node 

                elif node != end and node != start:   # if both the start and end node have been placed
                    node.color = WALL        # place a wall node
                

    pygame.quit()


main()
