from collections import deque

class GameState:
    def __init__(self, boardSize) :
        self.board = [0 for i in range(boardSize) for j in range(boardSize)]
        self.Q = deque() #where the pieces will be stored by order
        self.L = [] # where the pieces that the player can choose are stored
    
    def generatePieces(self):
        return None

    

