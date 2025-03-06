from collections import deque
import numpy as np
from PieceFactory import PieceFactory
from Piece import Piece
class GameState:
    def __init__(self, boardSize) :
        self.board = np.fromfunction(lambda i, j: (i % 2), (boardSize, boardSize), dtype=int)
        self.Q = deque() #where the pieces will be stored by order
        self.L = [] # where the pieces that the player can choose are stored
        self.piece = None  # Initialize self.piece
        self.piece_factory = PieceFactory()
        self.generatePieces()
        if self.L:
            self.piece = self.L[0]  # Initialize self.piece with the first piece in the list

    def generatePieces(self):
        # Example of generating pieces and adding them to the queue
        for _ in range(3):  # Generate 10 pieces for example
            piece = self.piece_factory.create_piece(4, 4, 1, False)  # Example piece
            self.Q.append(piece)
        self.L = [self.Q.popleft() for _ in range(3)]  # Initial selection of pieces

    def drawBoard(self, gui):
        board_size = len(self.board)
        for y in range(len(self.board)):
            for x in range(len(self.board[0])):
                if self.board[y][x] == 1 and self.piece:
                    occupied_cells = self.piece.getOccupiedCells()  # Get the cells occupied by the piece
                    for (px, py) in occupied_cells:
                        # Draw the piece in the correct position on the board
                        if (x == px and y == py):
                            gui.drawPiece(self.piece, x * board_size, y * board_size, board_size)

        


    

