
import pygame
import queue 
import main
import time 


CLOSED = "#00F2DE"
CURRENT_NODE = "#008DF2"

CLOSED = "#00F2DE"
OPEN =  "#C1F200"
EMPTY = "#FFFFFF"
WALL = "#103444"
PATH = "#9900F2"
START = "#F25400"
END = "#F2007C"


LINE = (70, 102, 255)
GRID_LINE = (176, 220, 252)
def h_score(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def draw_heuristic(win, node, store):
    if store.heuristic_toggled:
        if store.algorithm_selected == "A Star":
            pygame.draw.line(win, "#F2007C", (store.start.x,
                                store.start.y), (node.x, node.y))
            pygame.draw.line(win, "#9900F2", (node.x, node.y),
                                (store.end.x, store.end.y))
            pygame.display.update()
        if store.algorithm_selected == "Best FS":
            pygame.draw.line(win, "#F2007C", (node.x, node.y), (store.end.x, store.end.y))
            pygame.display.update()


def A_star(win, draw, grid, start, end, store):
    count = 0 # This will be used to prioritize the node that was added to the 
    # open set_first if two nodes have the same f_score
    open_set = queue.PriorityQueue() # the open_set will store:
    # the F score, count, and node object in a touple 
    came_from = {} # Dictionary to store which node lead to every other node
    open_set.put((0, count, start)) # add start node to open set

    inf = float("inf") 
    g_score = {node: inf for row in grid for node in row} # set g_score of all nodes to infinity 
    # ^ This is equivalent to 
        # g_score = {}
        # for row in grid:
        #     for node in row: 
        #         g_score[node] = inf
    f_score = {node: inf for row in grid for node in row} # set f_score of all nodes to infinity 
    g_score[start] = 0 # set g score of start node to 0
    f_score[start] = h_score(start.get_pos(), end.get_pos()) # calculate f_score of start node 

    open_set_hash = {start}

    while not open_set.empty():
        start.type = START
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: #allows the user to exit the program while the algorithm is running 
                pygame.quit()
            if event.type == pygame.KEYDOWN: #when the user presses space, reset the grid 
                if event.key == pygame.K_SPACE: 
                    main.reset()
            if store.step_mode_toggled == True or store.slider_val > 0: 
                if event.type == pygame.KEYDOWN:  
                    if event.key == pygame.K_RETURN: # Press enter to step 
                        store.run = True  
                if event.type == pygame.KEYDOWN:  
                    if event.key == pygame.K_RIGHT: # press -> to skip 
                        store.step_mode_toggled = False  
                        store.finish = True  
        if store.finish == False: 
           time.sleep(store.slider_val)  # used to slow down algorithm 
        if store.run == True or store.step_mode_toggled == False:
            current = open_set.get()[2] # get the node with the lowest F Score 
            open_set_hash.remove(current) # Remove this node from the open set 
            
            if current == end: # if this node is the end node, recontruct path and exit function 
                reconstruct_path(came_from, end, draw, start)
                start.type = START
                end.type = END
                return True
            if current is not start and current is not end: # 
                current.type = CURRENT_NODE # set the current node to the blue color 
                pygame.display.update()

            for neighbor in current.neighbors: # for every neighbor node 
                neighbor_g_score = g_score[current] + 1 #set the neighbor's g_score

                if neighbor_g_score < g_score[neighbor]: # check if that node allready has a lower g_score
                    came_from[neighbor] = current # set the neighbor's previous node to the current node 
                    g_score[neighbor] = neighbor_g_score # update the neighbor's g_score
                    f_score[neighbor] = neighbor_g_score + \
                        h_score(neighbor.get_pos(), end.get_pos()) # update the neighbor's f_score
                    if neighbor not in open_set_hash: #If the neighbor has not yet been added to the open set 
                        count += 1 # increment count (used to break f score ties)
                        open_set.put((f_score[neighbor], count, neighbor))  # add the neighbor to the open set 
                        open_set_hash.add(neighbor) # add it to the open set hash 
                        neighbor.type = OPEN # set the neighbor nodes color to green 
                        draw_heuristic(win,neighbor, store) # draw the heuristic line 
                        store.nodes_searched += 1 # update the analytics 

            draw() #calls the lambda function that re draws the grid 

            current.type = CLOSED # Make the node color blue to mark it as closed 
            store.nodes_seen += 1 # update analytics 
            store.run = False # set run to false (used for step mode)

    return False # exit the function. Good job computer 👌 
    
def Best_FS(win, draw, grid, start, end, store):
    count = 0
    open_set = queue.PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = h_score(start.get_pos(), end.get_pos())


    open_set_hash = {start}

    while not open_set.empty():

        start.type = START

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if store.step_mode_toggled == True or store.slider_val > 0: 
                if event.type == pygame.KEYDOWN:  
                    if event.key == pygame.K_RETURN:
                        store.run = True  
                if event.type == pygame.KEYDOWN:  
                    if event.key == pygame.K_RIGHT: 
                        print('right pressed')
                        store.step_mode_toggled = False  
                        store.finish = True  
        if store.finish == False:
           time.sleep(store.slider_val)

        if store.run == True or store.step_mode_toggled == False:
            current = open_set.get()[2]
            open_set_hash.remove(current)

            if current == end:
                reconstruct_path(came_from, end, draw, start)
                end.type = END
                return True

            for neighbor in current.neighbors:
                if current is not start and current is not end:
                    current.type = CURRENT_NODE                
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
                        store.nodes_searched += 1

            draw()

            if current != start:
                current.type = CLOSED
                store.nodes_seen += 1

            store.run = False 

    return False


def BFS(win, draw, grid, start, end, store):
    count = 0
    open_set = queue.Queue()
    open_set.put((count, start))
    came_from = {}

    open_set_hash = {start}

    while not open_set.empty():
        start.type = START
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if store.step_mode_toggled == True or store.slider_val > 0: 
                if event.type == pygame.KEYDOWN:  
                    if event.key == pygame.K_RETURN:
                        store.run = True  
                if event.type == pygame.KEYDOWN:  
                    if event.key == pygame.K_RIGHT: 
                        print('right pressed')
                        store.step_mode_toggled = False  
                        store.finish = True  
        if store.finish == False:
           time.sleep(store.slider_val) 

        if store.run == True or store.step_mode_toggled == False:
            current = open_set.get()[1]
            open_set_hash.remove(current)

            if current == end:
                reconstruct_path(came_from, end, draw, start)
                end.type = END

                return True

            for neighbor in current.neighbors:
                if current is not start and current is not end:
                    current.type = CURRENT_NODE
                if neighbor.type is not OPEN and neighbor.type is not CLOSED and neighbor is not start:
                    came_from[neighbor] = current
                    count += 1
                    open_set.put((count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.type = OPEN
                    store.nodes_searched += 1

            draw() #calls the lambda function that re draws the grid 

            current.type = CLOSED # Make the node color blue to mark it as closed 
            store.nodes_seen += 1 # update analytics 
            store.run = False # set run to false (used for step mode)

    return False # exit the function. Good job computer 👌 



def reconstruct_path(came_from, current, draw, start):
    while current in came_from:
        current = came_from[current]
        if current is not start:
            current.type = PATH
        draw()

