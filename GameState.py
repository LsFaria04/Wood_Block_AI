from collections import deque

class GameState:
    def __init__(self, boardSize) :
        self.board = [[1 if i % 2 else 0 for i in range(boardSize)] for j in range(boardSize)]
        self.Q = deque() #where the pieces will be stored by order
        self.L = [] # where the pieces that the player can choose are stored
    
    def generatePieces(self):
        return None

    def drawBoard(self, gui):
        for y in range(len(self.board)):
            for x in range(len(self.board[0])):
                if self.board[y][x]:
                    gui.drawRectangle(10 * x,10 * y, 10,10,(0,0,255))
        


    

