from board import Board
from ai import AI, RandomPlayer

def main():
    player1 = RandomPlayer("1")
    player2 = AI("2")
    gameBoard = Board(player1, player2)
    
    isDone = False

    while not isDone:
        isDone = gameBoard.play()

    if isDone == 1:
        message_text = str(gameBoard.PLAYERS[gameBoard.TURN]) + " Wins!"
    else:
        message_text = "Draw!"

    print(message_text)

    print("\n ======================")

    customBoard = Board(player1, player2, turn=0, bitboards=[144783458459,15231064178724])
    col = player1.play(customBoard)

    print("Column: ", col)

if __name__ == "__main__":
    main()