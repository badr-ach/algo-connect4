import random

class Tree:
    def __init__(self, aiBoard, humanBoard, maxDepth):
        rootNode = Node(aiBoard, humanBoard, 0, -1, -1)
        self.root = rootNode
        self.maxDepth = maxDepth  

    def computeBestColumn(self):
        bestvalue = self.root.value
        rootChildren = self.root.children
        print("Best   value :", bestvalue)
        print("Column values:", rootChildren)
        bestColumns = [c.col for c in rootChildren if c.value == bestvalue]
        print("Best Column :", bestColumns)
        if bestColumns:
            if len(bestColumns) > 1:
                return min(bestColumns, key=lambda x: 3-x)
            else:
                return bestColumns[0]
        raise Exception("Failed to find best value")

    def fork(self, ai, node):
        bMyTurn = node.depth % 2
        possibleBits = ai.getPossibleMoves(node.aiBoard | node.humanBoard)
        childrenNodes = []
        for colbitTuple in possibleBits:
            col = colbitTuple[0]
            if bMyTurn:
                tmpMyBoard = ai.setNthBit(node.aiBoard, colbitTuple[1])
                tmpOppBoard = node.humanBoard
            else:
                tmpMyBoard = node.aiBoard
                tmpOppBoard = ai.setNthBit(node.humanBoard, colbitTuple[1])
            childNode = Node(tmpMyBoard, tmpOppBoard, node.depth+1, node, col)
            childrenNodes.append(childNode)
        node.children = childrenNodes

    def alphabeta(self, b, ai, node, depth, alpha, beta):
        isTurn = node.depth % 2 == 0  
        if depth == 0 or node.depth == self.maxDepth:
            if node.value is None:
                node.value = ai.evaluateBoard(b, node.aiBoard, node.humanBoard, isTurn)
            return node.value

        self.fork(ai, node)
        if isTurn:
            v = float('-inf')
            for child in node.children:
                v = max(v, self.alphabeta(b, ai, child, depth-1, alpha, beta))
                alpha = max(alpha, v)
                if node.value is None or alpha > node.value:
                    node.value = alpha
                if beta <= alpha:
                    node.value = None
                    break
            return v
        else:
            v = float('inf')
            for child in node.children:
                v = min(v, self.alphabeta(b, ai, child, depth-1, alpha, beta))
                beta = min(beta, v)
                if node.value is None or beta < node.value:
                    node.value = beta
                if beta <= alpha:
                    node.value = None
                    break
            return v


class Node:
    def __init__(self, aiBoard, humanBoard, depth, parentNode, col, value=None):
        self.aiBoard = aiBoard
        self.humanBoard = humanBoard
        self.value = value
        self.depth = depth
        if depth == 0: 
            self.parent = self 
        else:
            self.parent = parentNode
        self.children = []
        self.col = col

    def computeValue(self):
        if self.children and self.value is None:
            if self.depth % 2:
                self.value = min(c.value for c in self.children)
            else:
                self.value = max(c.value for c in self.children)
            return self.value

    def __repr__(self):
        return str(self.value)

    def __eq__(self, node):
        return self.value == node.value

    def __lt___(self, node):
        return self.value < node.value

    def __gt__(self, node):
        return self.value > node.value

class AI:
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

    def getPossibleMoves(self, overall_bitboard):
        listOfCoords = []
        for i in range(7):  
            for x in range(i*7, i*7+6):  
                if not self.getNthBit(overall_bitboard, x):  
                    listOfCoords.append((i, x))
                    break
        return listOfCoords

    def getLegalBoard(self, overall_bitboard):
        board = 0
        for i in range(7):
            for x in range(i*7, i*7+6):
                if not self.getNthBit(overall_bitboard, x):
                    board |= (1 << x)
                    break
        return board
    
    def countAlignmentsOfThree(self, oppBoard, myBoard):
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

    def countAlignmentsOfTwo(self, oppBoard, myBoard):
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

    def countAlignmentsOfOne(self, oppBoard, myBoard):
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

    def evaluateBoard(self, b, oppBoard, myBoard, bMyTurn):
        winReward = 9999999
        OppCost3Row = 1000
        MyCost3Row = 3000
        OppCost2Row = 500
        MyCost2Row = 500
        OppCost1Row = 100
        MyCost1Row = 100

        if b.hasWinner(oppBoard):
            return -winReward
        elif b.hasWinner(myBoard):
            return winReward

        get3Win = self.countAlignmentsOfThree(oppBoard, myBoard)
        winning3 = self.bitboardBits(get3Win) * MyCost3Row

        get3Block = self.countAlignmentsOfThree(myBoard, oppBoard)
        blocking3 = self.bitboardBits(get3Block) * -OppCost3Row

        get2Win = self.countAlignmentsOfTwo(oppBoard, myBoard)
        winning2 = self.bitboardBits(get2Win) * MyCost2Row

        get2Block = self.countAlignmentsOfTwo(myBoard, oppBoard)
        blocking2 = self.bitboardBits(get2Block) * -OppCost2Row

        get1Win = self.countAlignmentsOfOne(oppBoard, myBoard)
        winning1 = self.bitboardBits(get1Win) * MyCost1Row

        get1Block = self.countAlignmentsOfOne(myBoard, oppBoard)
        blocking1 = self.bitboardBits(get1Block) * -OppCost1Row

        return winning3 + blocking3 + winning2 + blocking2\
            + winning1 + blocking1

    def search(self, board):
        myBoard = board.BITBOARDS[board.TURN]
        oppBoard = board.BITBOARDS[(not board.TURN)]
        maxDepth = 7
        g = Tree(myBoard, oppBoard, maxDepth) 

        import time
        start = time.time()

        g.alphabeta(board, self, g.root, maxDepth,float('-inf'), float('inf'))

        end = time.time()
        print("duration : ",end - start)

        return g.computeBestColumn()

    def computeMustPlayCols(self, board):
        myBoard = board.BITBOARDS[board.TURN]
        oppBoard = board.BITBOARDS[(not board.TURN)]
        possibleBits = self.getPossibleMoves(myBoard | oppBoard)
        forcedCols = [] 
        for colbitTuple in possibleBits:
            tempMyBoard = self.setNthBit(myBoard, colbitTuple[1])
            tempOppBoard = self.setNthBit(oppBoard, colbitTuple[1])
            if board.hasWinner(tempMyBoard):
                return colbitTuple[0]
            elif board.hasWinner(tempOppBoard):
                forcedCols.append(colbitTuple[0])
        if forcedCols:
            return forcedCols[0]
        return -1

    def play(self, board):
        forcedColumn = self.computeMustPlayCols(board)  
        if forcedColumn > -1:
            return forcedColumn  
        return self.search(board) 

class RandomPlayer(AI):
    def play(self, board):
        myBoard = board.BITBOARDS[board.TURN]
        oppBoard = board.BITBOARDS[(not board.TURN)]
        col = random.choice([m[0] for m in super().getPossibleMoves(myBoard | oppBoard)])
        print("Random Column Chosen", col)
        return col