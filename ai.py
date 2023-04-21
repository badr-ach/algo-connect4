import tree

class AI ():
    def __init__(self, name="CPU"):
        self.name = name

    def __repr__(self):
        return str(self.name)

    def flipBit(self, board, p, x, y):
        board.BITBOARDS[p] |= (1 << (x*7 + y))

    def getNthBit(self, num, n):
        return (num >> n) & 1

    def setNthBit(self, num, n):
        return num | (1 << n)

    def get_legal_locations(self, overall_bitboard):
        listOfCoords = []
        for i in range(7):  
            for x in range(i*7, i*7+6):  
                if not self.getNthBit(overall_bitboard, x):  
                    listOfCoords.append((i, x))
                    break
        return listOfCoords

    def get_legal_board(self, overall_bitboard):
        board = 0
        for i in range(7):
            for x in range(i*7, i*7+6):
                if not self.getNthBit(overall_bitboard, x):
                    board |= (1 << x)
                    break
        return board
    def evaluate3(self, oppBoard, myBoard):
        inverseBoard = ~(myBoard | oppBoard)
        rShift7MyBoard = myBoard >> 7
        lShift7MyBoard = myBoard << 7
        rShift14MyBoard = myBoard >> 14
        lShit14MyBoard = myBoard << 14
        rShift16MyBoard = myBoard >> 16
        lShift16MyBoard = myBoard << 16
        rShift8MyBoard = myBoard >> 8
        lShift8MyBoard = myBoard << 8
        rShift6MyBoard = myBoard >> 6
        lShift6MyBoard = myBoard << 6
        rShift12MyBoard = myBoard >> 12
        lShift12MyBoard = myBoard << 12

        result = inverseBoard & rShift7MyBoard & rShift14MyBoard\
            & (myBoard >> 21)

        result |= inverseBoard & rShift7MyBoard & rShift14MyBoard\
            & lShift7MyBoard

        result |= inverseBoard & rShift7MyBoard & lShift7MyBoard\
            & lShit14MyBoard

        result |= inverseBoard & lShift7MyBoard & lShit14MyBoard\
            & (myBoard << 21)

        result |= inverseBoard & rShift8MyBoard & rShift16MyBoard\
            & (myBoard >> 24)

        result |= inverseBoard & rShift8MyBoard & rShift16MyBoard\
            & lShift8MyBoard

        result |= inverseBoard & rShift8MyBoard & lShift8MyBoard\
            & lShift16MyBoard

        result |= inverseBoard & lShift8MyBoard & lShift16MyBoard\
            & (myBoard << 24)

        result |= inverseBoard & rShift6MyBoard & rShift12MyBoard\
            & (myBoard >> 18)

        result |= inverseBoard & rShift6MyBoard & rShift12MyBoard\
            & lShift6MyBoard

        result |= inverseBoard & rShift6MyBoard & lShift6MyBoard\
            & lShift12MyBoard

        result |= inverseBoard & lShift6MyBoard & lShift12MyBoard\
            & (myBoard << 18)

        result |= inverseBoard & (myBoard << 1) & (myBoard << 2)\
            & (myBoard << 3)

        return result

    def evaluate2(self, oppBoard, myBoard):
        inverseBoard = ~(myBoard | oppBoard)
        rShift7MyBoard = myBoard >> 7
        rShift14MyBoard = myBoard >> 14
        lShift7MyBoard = myBoard << 7
        lShift14MyBoard = myBoard << 14
        rShift8MyBoard = myBoard >> 8
        lShift8MyBoard = myBoard << 8
        lShift16MyBoard = myBoard << 16
        rShift16MyBoard = myBoard >> 16
        rShift6MyBoard = myBoard >> 6
        lShift6MyBoard = myBoard << 6
        rShift12MyBoard = myBoard >> 12
        lShift12MyBoard = myBoard << 12

        result = inverseBoard & rShift7MyBoard & rShift14MyBoard
        result |= inverseBoard & rShift7MyBoard & rShift14MyBoard
        result |= inverseBoard & rShift7MyBoard & lShift7MyBoard

        result |= inverseBoard & lShift7MyBoard & lShift14MyBoard

        result |= inverseBoard & lShift8MyBoard & lShift16MyBoard

        result |= inverseBoard & rShift8MyBoard & rShift16MyBoard
        result |= inverseBoard & rShift8MyBoard & rShift16MyBoard
        result |= inverseBoard & rShift8MyBoard & lShift8MyBoard

        result |= inverseBoard & rShift6MyBoard & rShift12MyBoard
        result |= inverseBoard & rShift6MyBoard & rShift12MyBoard
        result |= inverseBoard & rShift6MyBoard & lShift6MyBoard
        result |= inverseBoard & lShift6MyBoard & lShift12MyBoard

        result |= inverseBoard & (myBoard << 1) & (myBoard << 2) \
            & (myBoard << 2)

        return result

    def evaluate1(self, oppBoard, myBoard):
        inverseBoard = ~(myBoard | oppBoard)
        result = inverseBoard & (myBoard >> 7)
        result |= inverseBoard & (myBoard << 7)
        result |= inverseBoard & (myBoard << 1)
        return result

    def bitboardBits(self, i):
        i = i & 0xFDFBF7EFDFBF  
        i = (i & 0x5555555555555555) + ((i & 0xAAAAAAAAAAAAAAAA) >> 1)
        i = (i & 0x3333333333333333) + ((i & 0xCCCCCCCCCCCCCCCC) >> 2)
        i = (i & 0x0F0F0F0F0F0F0F0F) + ((i & 0xF0F0F0F0F0F0F0F0) >> 4)
        i = (i & 0x00FF00FF00FF00FF) + ((i & 0xFF00FF00FF00FF00) >> 8)
        i = (i & 0x0000FFFF0000FFFF) + ((i & 0xFFFF0000FFFF0000) >> 16)
        i = (i & 0x00000000FFFFFFFF) + ((i & 0xFFFFFFFF00000000) >> 32)

        return i

    def evalCost(self, b, oppBoard, myBoard, bMyTurn):
        winReward = 9999999
        OppCost3Row = 1000
        MyCost3Row = 3000
        OppCost2Row = 500
        MyCost2Row = 500
        OppCost1Row = 100
        MyCost1Row = 100

        if b.hasWon(oppBoard):
            return -winReward
        elif b.hasWon(myBoard):
            return winReward

        get3Win = self.evaluate3(oppBoard, myBoard)
        winning3 = self.bitboardBits(get3Win) * MyCost3Row

        get3Block = self.evaluate3(myBoard, oppBoard)
        blocking3 = self.bitboardBits(get3Block) * -OppCost3Row

        get2Win = self.evaluate2(oppBoard, myBoard)
        winning2 = self.bitboardBits(get2Win) * MyCost2Row

        get2Block = self.evaluate2(myBoard, oppBoard)
        blocking2 = self.bitboardBits(get2Block) * -OppCost2Row

        get1Win = self.evaluate1(oppBoard, myBoard)
        winning1 = self.bitboardBits(get1Win) * MyCost1Row

        get1Block = self.evaluate1(myBoard, oppBoard)
        blocking1 = self.bitboardBits(get1Block) * -OppCost1Row

        return winning3 + blocking3 + winning2 + blocking2\
            + winning1 + blocking1

    def search(self, board):
        myBoard = board.BITBOARDS[board.TURN]
        oppBoard = board.BITBOARDS[(not board.TURN)]
        maxDepth = 5

        g = tree.graph(myBoard, oppBoard, maxDepth) 

        import time
        start = time.time()

        g.alphabeta(board, self, g.root, maxDepth,float('-inf'), float('inf'))

        end = time.time()
        print("duration : ",end - start)
        return g.getMove()

    def forced_moves(self, board):
        myBoard = board.BITBOARDS[board.TURN]
        oppBoard = board.BITBOARDS[(not board.TURN)]
        possibleBits = self.get_legal_locations(myBoard | oppBoard)

        forcedCols = [] 
        for colbitTuple in possibleBits:
            tempMyBoard = self.setNthBit(myBoard, colbitTuple[1])
            tempOppBoard = self.setNthBit(oppBoard, colbitTuple[1])

            if board.hasWon(tempMyBoard):
                return colbitTuple[0]
            elif board.hasWon(tempOppBoard):
                forcedCols.append(colbitTuple[0])

        if forcedCols:
            return forcedCols[0]
        return -1

    def play(self, board):
        forcedColumn = self.forced_moves(board)  
        if forcedColumn > -1:
            return forcedColumn  
        return self.search(board) 
