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

    def create_piece(self, XLen,YLen, type, rev): 
        piece = None    
        if type == 1:
            piece = self.type1(XLen, YLen)
        elif type == 2:
            piece = self.type2(XLen, YLen)
        elif type == 3:
            piece = self.type3(XLen, YLen, rev)
        elif type == 4:
            piece = self.type4(XLen, YLen, rev)
        elif type == 5:
            piece = self.type5(XLen, YLen, rev)
        elif type == 6:
            piece = self.type6(XLen, YLen, rev)

        return piece
    
    def type1(self, XLen,YLen):
        pieceMatrix = []
        for _ in range(YLen):
            line = []
            for _ in range(XLen):
                line.append(1)
            pieceMatrix.append(line)
        return Piece(1, False, XLen, YLen,pieceMatrix)
    
    def type2(self, XLen,YLen):
        if XLen == YLen:
            print("Rectangle cannot have the same size for the height and length")
        pieceMatrix = []
        for y in range(YLen):
            line = []
            for x in range(XLen):
                line.append(1)
            pieceMatrix.append(line)
        return Piece(2, False, XLen, YLen, pieceMatrix)
    
    def type3(self, XLen,YLen, rev):
        pieceMatrix = []
        for y in range(YLen):
            line = []
            for x in range(XLen):
                #reversed L (mirror is the Y axis)
                if (x == (XLen - 1) or y == (YLen -1)) and rev:
                    line.append(1)
                #normal L
                elif (x == 1 or y == (YLen -1)) and not rev:
                    line.append(1)
                else:
                    line.append(0)
            pieceMatrix.append(line)
        return Piece(3, rev, XLen, YLen, pieceMatrix)
    
    def type4(self, XLen,YLen,rev):
        pieceMatrix = []
        for y in range(YLen):
            line = []
            for x in range(XLen):
                #reversed L (mirror is the Y axis)
                if (x == (XLen - 1) or y == 1) and rev:
                    line.append(1)
                #normal L
                elif (x == 1 or y == 1) and not rev:
                    line.append(1)
                else:
                    line.append(0)
            pieceMatrix.append(line)
        return Piece(4, rev, XLen, YLen, pieceMatrix)
        
    def type5(self, XLen,YLen,rev):
        idx_leg = round(XLen / 2)
        pieceMatrix = []
        for y in range(YLen):
            line = []
            for x in range(XLen):
                #reversed T (mirror is the Y axis)
                if (x == idx_leg or y == (YLen - 1)) and rev:
                    line.append(1)
                #normal T
                elif (x == idx_leg or y == 1 ) and not rev:
                    line.append(1)
                else:
                    line.append(0)
            pieceMatrix.append(line)
        return Piece(5, rev, XLen, YLen, pieceMatrix)

    def type6(self, XLen,YLen, rev):
        idx_leg = round(YLen / 2)
        pieceMatrix = []
        for y in range(YLen):
            line = []
            for x in range(XLen):
                #reversed T (mirror is the Y axis)
                if (x == (XLen - 1) or y == idx_leg) and rev:
                    line.append(1)
                #normal T
                elif (x == 1 or y == idx_leg ) and not rev:
                    line.append(1)
                else:
                    line.append(0)
            pieceMatrix.append(line)
        return Piece(6, rev, XLen, YLen, pieceMatrix)