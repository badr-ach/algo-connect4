from board import Board
from ai import AI, RandomPlayer

def main():
    i = 100
    count = [0, 0, 0]
    while i > 0:
        player1 = RandomPlayer("1")
        player2 = AI("2")
        gameBoard = Board(player1, player2, turn=0, bitboards=[0,0])
        
        isDone = False

        while not isDone:
            isDone = gameBoard.play()

        if isDone == 1:
            message_text = str(gameBoard.PLAYERS[gameBoard.TURN]) + " Wins!"
            count[gameBoard.TURN] += 1
        else:
            count[2] += 1
            message_text = "Draw!"
        i-=1

        print(message_text)

        player1 = RandomPlayer("1")
        player2 = AI("2")
        gameBoard = Board(player1, player2)

    print("Player 1: ", count[0])
    print("Player 2: ", count[1])
    print("Draw: ", count[2])

    # print(message_text)

    # print("\n ======================")

    # customBoard = Board(player1, player2, turn=0, bitboards=[144783458459,15231064178724])
    # col = player1.play(customBoard)

    # print("Column: ", col)

if __name__ == "__main__":
    main()