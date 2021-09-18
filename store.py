class Store():
    def __init__(self):
        self.grid = []
        self.start = None 
        self.end = None 
        self.heuristic_toggled = True 
        self.count = 0