class Store():
    def __init__(self):
        self.grid = []
        self.start = None
        self.end = None
        self.heuristic_toggled = True
        self.count = 0
        self.algorithm_selected = "A Star"
        self.analytics = ""
        self.run = True
        self.step_mode_toggled = False
        self.slider_val = 0
        self.finish = False 
        self.nodes_searched = 0
        self.nodes_seen = 0
        self.open_nodes = 0
        self.closed_nodes = 0
        self.shortest_path_length = 0




