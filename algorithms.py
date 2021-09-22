
import pygame
import queue 
import main
import store


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
nodes_searched = ""
nodes_seen = ""
def h_score(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def draw_heuristic(win, node, store):
    if store.heuristic_toggled:
        pygame.draw.line(win, "#F2007C", (store.start.x,
                         store.start.y), (node.x, node.y))
        pygame.draw.line(win, "#9900F2", (node.x, node.y),
                         (store.end.x, store.end.y))
        pygame.display.update()


def A_star(win, draw, grid, start, end, store):
    global nodes_searched,nodes_seen
    count = 0
    open_set = queue.PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = h_score(start.get_pos(), end.get_pos())
    nodes_searched = 0
    nodes_seen = 0

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw, start)
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
                    draw_heuristic(win,neighbor, store)
                    nodes_searched += 1

        draw()

        if current != start:
            current.type = CLOSED
            nodes_seen += 1

    return False
    
def Best_FS(win, draw, grid, start, end, store):
    global nodes_searched,nodes_seen
    count = 0
    open_set = queue.PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = h_score(start.get_pos(), end.get_pos())
    nodes_searched = 0
    nodes_seen = 0

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw, start)
            end.type = END
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = h_score(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    came_from[neighbor] = current
                    count += 1
                    f_score[neighbor] = h_score(neighbor.get_pos(), end.get_pos())
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.type = OPEN
                    draw_heuristic(win, neighbor, store)
                    nodes_searched += 1

        draw()

        if current != start:
            current.type = CLOSED
            nodes_seen += 1

    return False


def BFS(win, draw, grid, start, end, store):
    global nodes_searched,nodes_seen
    count = 0
    open_set = queue.Queue()
    open_set.put((count, start))
    came_from = {}
    nodes_searched = 0
    nodes_seen = 0

    open_set_hash = {start}

    while open_set:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[1]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw, start)
            end.type = END

            return True

        for neighbor in current.neighbors:

            if neighbor.type is not OPEN and neighbor.type is not CLOSED and neighbor is not start:
                came_from[neighbor] = current
                count += 1
                open_set.put((count, neighbor))
                open_set_hash.add(neighbor)
                neighbor.type = OPEN
                nodes_searched += 1

        draw()

        if current != start:
            current.type = CLOSED
            nodes_seen += 1


    return False



def reconstruct_path(came_from, current, draw, start):
    global nodes_searched, nodes_seen
    while current in came_from:
        current = came_from[current]
        if current is not start:
            current.type = PATH
        draw()
    print(nodes_searched)
    print(nodes_seen)
    nodes_searched = nodes_searched

