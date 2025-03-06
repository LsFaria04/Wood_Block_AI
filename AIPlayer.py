class AIPlayer:
    def __init__(self, algorithm):
        self.algorithm = algorithm

    def play(self,gamestate):
        #deve retornar uma move
        if self.algorithm == 1:
            self.bfs()
        elif self.algorithm == 2:
            self.dfs()
        elif self.algorithm == 3:
            self.iteractive_deepening()
        elif self.algorithm == 4:
            self.uniform_cost()
        elif self.algorithm == 5:
            self.greedy()
        elif self.algorithm == 6:
            self.a_star()
        elif self.algorithm == 7:
            self.a_star_weighted()
        else:
            print("Algorithm is not available")
    
    def bfs(self):
        return None
    def dfs(self):
        return None
    def iteractive_deepening(self):
        return None
    def uniform_cost(self):
        return None
    def greedy(self):
        return None
    def a_star(self):
        return None
    def a_star_weighted(self):
        return None