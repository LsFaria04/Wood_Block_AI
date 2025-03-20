from Piece import Piece

class PieceFactory:
    #Pieces are layout is stored into a matrix (NXN but the default is 4X4)
    #Pieces can be of different types and have reverse variants
    #type 1 -> square (doesn't have reverse)
    #type 2 -> rectangle (doesn't have reverse, Lenx != LenY)
    #type 3 -> L shape
    #type 4 -> inverted L shape
    #type 5 -> T shape
    #type 6 -> rotated T shape

    def create_piece(self, x, y, XLen, YLen, piece_type, rev): 
        piece = None    
        if piece_type == 1:
            piece = self.type1(x, y, XLen, YLen)
        elif piece_type == 2:
            piece = self.type2(x, y, XLen, YLen)
        elif piece_type == 3:
            piece = self.type3(x, y, XLen, YLen, rev)
        elif piece_type == 4:
            piece = self.type4(x, y, XLen, YLen, rev)
        elif piece_type == 5:
            piece = self.type5(x, y, XLen, YLen, rev)
        elif piece_type == 6:
            piece = self.type6(x, y, XLen, YLen, rev)

        return piece
    
    def type1(self, x, y, XLen,YLen):
        if XLen != YLen:
            raise ValueError("Square must have the same size for the height and length.")
        pieceMatrix = []
        for _ in range(YLen):
            line = []
            for _ in range(XLen):
                line.append(1)
            pieceMatrix.append(line)
        return Piece(1, False, XLen, YLen,pieceMatrix , x, y)
    
    def type2(self, x, y, XLen, YLen):
            if XLen == YLen:
                raise ValueError("Rectangle cannot have the same size for the height and length.")
            pieceMatrix = [[1 for _ in range(XLen)] for _ in range(YLen)]
            return Piece(2, False, XLen, YLen, pieceMatrix, x, y )
    
    def type3(self, x1, y1, XLen,YLen, rev):
        pieceMatrix = []
        for y in range(YLen):
            line = []
            for x in range(XLen):
                #reversed L (mirror is the Y axis)
                if (x == (XLen - 1) or y == (YLen -1)) and rev:
                    line.append(1)
                #normal L
                elif (x == 0 or y == (YLen - 1)) and not rev:
                    line.append(1)
                else:
                    line.append(0)
            pieceMatrix.append(line)
        return Piece(3, rev, XLen, YLen, pieceMatrix, x1, y1)
    
    def type4(self, x1, y1, XLen,YLen,rev):
        pieceMatrix = []
        for y in range(YLen):
            line = []
            for x in range(XLen):
                #reversed L (mirror is the Y axis)
                if (x == (XLen - 1) or y == 0) and rev:
                    line.append(1)
                #normal L
                elif (x == 0 or y == 0) and not rev:
                    line.append(1)
                else:
                    line.append(0)
            pieceMatrix.append(line)
        return Piece(4, rev, XLen, YLen, pieceMatrix, x1, y1)
        
    def type5(self, x1, y1, XLen,YLen,rev):
        pieceMatrix = []
        idx_leg = round(XLen / 2)
        idx_leg = XLen // 2
        for y in range(YLen):
            line = []
            for x in range(XLen):
                #reversed T (mirror is the Y axis)
                if (x == idx_leg or y == (YLen - 1)) and rev:
                    line.append(1)
                #normal T
                elif (x == idx_leg or y == (YLen - 1)) and not rev:
                    line.append(1)
                else:
                    line.append(0)
            pieceMatrix.append(line)
        return Piece(5, rev, XLen, YLen, pieceMatrix, x1, y1)

    def type6(self, x1, y1, XLen,YLen, rev):
        pieceMatrix = []
        idx_leg = YLen // 2
        idx_leg = YLen // 2
        for y in range(YLen):
            line = []
            for x in range(XLen):
                #reversed T (mirror is the Y axis)
                if (x == 0 or y == idx_leg) and rev:
                    line.append(1)
                #normal T
                elif (x == (XLen - 1) or y == idx_leg) and not rev:
                    line.append(1)
                else:
                    line.append(0)
            pieceMatrix.append(line)
        return Piece(6, rev, XLen, YLen, pieceMatrix, x1, y1)