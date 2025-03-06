class Piece:
    def __init__(self, type, isRev, xlen, ylen, matrix):
        self.type = type
        self.xlen = xlen
        self.ylen = ylen
        self.isRev = isRev
        self.matrix = matrix

    def getOccupiedCells(self):
        occupiedCells = [(x, y) for y in range(self.ylen) for x in range(self.xlen) if self.matrix[y][x] == 1]
        return occupiedCells    