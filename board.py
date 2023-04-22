class Board:
    def __init__(self, p1, p2, turn=0, bitboards=[0, 0]):
        self.WIDTH = 7
        self.HEIGHT = 6
        self.TURN = turn
        self.PLAYERS = (p1, p2)
        self.BITBOARDS = bitboards
        self.PIECES = [[ 0 for i in range(6)] for i in range(7)]

    def play(self):
            chosenCol = -1
            player = self.PLAYERS[self.TURN]
            chosenCol = player.play(self)
            if chosenCol >= 0:
                return self.dropPiece(chosenCol)
            return False

    def dropPiece(self, col):
        if col < 0:  
            return False

        pieceCol = self.PIECES[col]
        y = 0
        for i in range(len(pieceCol)):
            if pieceCol[i] == 0: 
                self.PIECES[col][i] = self.TURN + 1
                self.PLAYERS[self.TURN].flipBit(self, self.TURN, col, y)
                return self.endTurn()
            y += 1
        return False 

    def hasWinner(self, bitboard):
        y = bitboard & (bitboard >> 6)
        if (y & (y >> 2 * 6)):  
            return True
        y = bitboard & (bitboard >> 7)
        if (y & (y >> 2 * 7)):  
            return True
        y = bitboard & (bitboard >> 8)
        if (y & (y >> 2 * 8)):  
            return True
        y = bitboard & (bitboard >> 1)
        if (y & (y >> 2)):  
            return True
        return False

    def isADraw(self, overall_bitboard):
        return (overall_bitboard & 0xFDFBF7EFDFBF) == 0xFDFBF7EFDFBF

    def endTurn(self):
        if self.hasWinner(self.BITBOARDS[self.TURN]):
            return 1
        if self.isADraw(self.BITBOARDS[0] | self.BITBOARDS[1]):
            return 2
        self.TURN = not self.TURN
        return False
