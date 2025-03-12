from collections import deque
import numpy as np
from PieceFactory import PieceFactory
from Piece import Piece
from copy import deepcopy

class GameState:
    def __init__(self, board_size, board=[], move_history=None, Q=None, L=None, points = 0):
        if len(board) == 0:
            self.board = np.zeros((board_size, board_size))
            self.Q = deque() # where the pieces will be stored by order
            self.L = [] # where the pieces that the player can choose are stored
            self.piece = None  # Initialize self.piece
            self.piece_factory = PieceFactory()
            self.points = 0
            self.move_history = []
            for i in range(10):
                self.generate_pieces()
            self.L = [self.Q.popleft() for _ in range(3)]
            if self.L:
                self.piece = self.L[0]  # Initialize self.piece with the first piece in the list
            
        else:
            self.board = deepcopy(board)
            self.Q = deepcopy(Q) #where the pieces will be stored by order
            self.L = deepcopy(L) # where the pieces that the player can choose are stored
            self.piece = None  # Initialize self.piece
            self.piece_factory = PieceFactory()
            self.points = points
            self.move_history = deepcopy(move_history)
            if self.L:
                self.piece = self.L[0]  # Initialize self.piece with the first piece in the list


    def __hash__(self):
        return hash(( str([item for sublist in self.board for item in sublist]), len(self.Q), len(self.L), self.points))
    def __eq__(self, other) :
        return [item for sublist in self.board for item in sublist] == [item for sublist in other.board for item in sublist] and len(self.Q) == len(other.Q) and self.points == other.points

    def generate_pieces(self):
        tile_size = 30
        offset_x, offset_y = 60, len(self.board) * tile_size + 70
        spacing = 180

        for i in range(3):
            x, y = offset_x + i * spacing, offset_y
            piece = self.piece_factory.create_piece(x, y, 4, 2, 2, False)
            self.Q.append(piece)


    def draw_board(self, gui):
        offset_x, offset_y = 2, 1 # Offset to draw the board

        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                pos = (x + offset_x, y + offset_y)
                if cell == 1:
                    gui.drawRectangle(pos)
                else:
                    gui.draw_board_background(pos)

    def draw_current_pieces(self, gui):
        # Draws the three pieces available for the player below the game board
        tile_size = 30

        for i, piece in enumerate(self.L[:3]):
            gui.drawPiece(piece, tile_size)

    def children(self):
        '''
        Returns all the possible moves with the pieces for selection
        '''
        lin_size = len(self.board)
        col_size = len(self.board[0])

        children = []

        for piece_idx in range(len(self.L)):
            for y in range(lin_size):
                for x in range(col_size):
                    if self.board[y][x] != 0:
                        continue
                    if self.is_move_possible(piece_idx, (x,y)):
                        child = GameState(lin_size, self.board,self.move_history, self.Q, self.L, self.points)
                        child.move(piece_idx, (x,y))
                        children.append(child)

        return children
    
    def is_move_possible(self, piece_idx, cords):
        '''Checks if a move is possible for a given piece and board coordinates'''
        lin_size = len(self.board)
        col_size = len(self.board[0])

        if piece_idx > 2 or piece_idx < 0:
            # invalid index for the list of selection pieces
            return False
        
        piece = self.L[piece_idx]

        x,y = cords

        if y + piece.ylen >= lin_size + 1 :
            return False
        if x + piece.xlen >= col_size + 1:
            return False

        for y_offset in range(piece.ylen):
            for x_offset in range(piece.xlen):
                if self.board[y + y_offset][x + x_offset] == 1 and piece.matrix[y_offset][x_offset] == 1:
                    return False

        return True



    def move(self, piece_idx, cords):
        '''Executes a move updating the game board with the given piece in the given coordinates. Assumes that the move is possible !!!!'''
        x,y = cords
        piece = self.L[piece_idx]

        for y_offset in range(piece.ylen):
            for x_offset in range(piece.xlen):
                if piece.matrix[y_offset][x_offset] == 1:
                    self.board[y + y_offset][x + x_offset] = 1
        
        self.move_history.append(self)

        #inserts a new piece into the list of pieces that the player can play or removes it from the list if there aren't any more pieces
        if len(self.Q) > 0:
            self.L[piece_idx] = self.Q.popleft()
        else:
            self.L.pop(piece_idx)
        
        #checks and remove the lines and columns that are full after the move
        full_lin, full_col = self.full_lines_columns()
        self.remove_full_lines_columns(full_lin, full_col)
    
    def full_lines_columns(self):
        full_lines = []
        full_columns = []
        line_numb = len(self.board)
        col_numb = len(self.board[0])
        lines = np.zeros(line_numb)
        columns = np.zeros(col_numb)

        #find how many cells are occupied in each line and column
        for lin in range(line_numb):
            for col in range(col_numb):
                if self.board[lin][col] == 1:
                    lines[lin] += 1
                    columns[col] += 1
        
        #check what are the line that are full
        for lin in range(line_numb):
            if lines[lin] == col_numb:
                full_lines.append(lin)
        for col in range(col_numb):
            if columns[col] == line_numb:
                full_columns.append(col)

        return (full_lines,full_columns)
    
    def remove_full_lines_columns(self, full_lines, full_columns):
        lin_size = len(self.board)
        col_size = len(self.board[0])

        self.points += lin_size * (len(full_lines) + len(full_columns))

        #remove the lines
        for col in range(col_size):
            for lin in full_lines:
                self.board[lin][col] = 0
        
        #remove the columns
        for lin in range(lin_size):
            for col in full_columns:
                self.board[lin][col] = 0
    
    
    def game_over(self):
        # no pieces to play 
        return len(self.L) == 0 and len(self.Q) == 0
    
    def reconstruct_play(self, move_history, gui):
        '''
        Displays the moves made by the AI to win the game 
        '''
        for move in move_history:
            
            gui.draw_background()
            move.draw_board(gui)
            move.draw_current_pieces(gui)
            gui.refresh_screen()






    

