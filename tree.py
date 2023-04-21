class graph:
    def __init__(self, myBoard, oppBoard, maxDepth):
        rootNode = Node(myBoard, oppBoard, 0, -1, -1)
        self.root = rootNode
        self.maxDepth = maxDepth  

    def getMove(self):

        bestvalue = self.root.value
        rootChildren = self.root.children

        print("Best   value :", bestvalue)
        print("Column values:", rootChildren)

        bestColumns = [c.col for c in rootChildren if c.value == bestvalue]

        print("COLS", bestColumns)

        if bestColumns:
            if len(bestColumns) > 1:
                return min(bestColumns, key=lambda x: 3-x)
            else:
                return bestColumns[0]
        raise Exception("Failed to find best value")

    def createNodeChildren(self, ai, node):
        bMyTurn = node.depth % 2
        possibleBits = ai.get_legal_locations(node.myBoard | node.oppBoard)
        childrenNodes = []
        for colbitTuple in possibleBits:
            col = colbitTuple[0]
            if bMyTurn:
                tmpMyBoard = ai.setNthBit(node.myBoard, colbitTuple[1])
                tmpOppBoard = node.oppBoard
            else:
                tmpMyBoard = node.myBoard
                tmpOppBoard = ai.setNthBit(node.oppBoard, colbitTuple[1])
            childNode = Node(tmpMyBoard, tmpOppBoard, node.depth+1, node, col)
            childrenNodes.append(childNode)
        node.children = childrenNodes

    def alphabeta(self, b, ai, node, depth, alpha, beta):
        isTurn = node.depth % 2 == 0  
        if depth == 0 or node.depth == self.maxDepth:
            if node.value is None:
                node.value = ai.evalCost(b, node.myBoard, node.oppBoard, isTurn)
            return node.value

        self.createNodeChildren(ai, node)
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
    def __init__(self, myBoard, oppBoard, depth, parentNode, col, value=None):
        self.myBoard = myBoard
        self.oppBoard = oppBoard
        self.value = value
        self.depth = depth
        if depth == 0: 
            self.parent = self 
        else:
            self.parent = parentNode
        self.children = []
        self.col = col

    def setValueFromChildren(self):
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
