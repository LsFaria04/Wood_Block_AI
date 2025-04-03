class Piece:
    def __init__(self, type, isRev, xlen, ylen, matrix, x, y, isPlaced = False):
        self.type = type
        self.xlen = xlen
        self.ylen = ylen
        self.isRev = isRev
        self.matrix = matrix
        self.x = x
        self.y = y
        self.isPlaced = isPlaced

    def getOccupiedCells(self):
        '''
        Gets the Piece matrix cells that are occupied (that represent a wood block)
        '''
        occupiedCells = [(x, y) for y in range(self.ylen) for x in range(self.xlen) if self.matrix[y][x] == 1]
        return occupiedCells    
    
    def set_position(self, x, y):
        '''
        Sets a new position to the piece
        '''
        self.x = x 
        self.y = y
        self.isPlaced = True