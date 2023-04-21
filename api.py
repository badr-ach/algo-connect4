from flask import Flask, request, jsonify
import numpy as np
from board import Board
from ai import AI

app = Flask(__name__)

@app.route('/move',methods=['GET'])
def move():
    board = request.args.get('b')
    return get_move(board)
    
def get_move(board):
    if not board or len(board) != 42 or not set(board).issubset({'0', 'h', 'm'}):
        return jsonify({'detail': 'Invalid board format'}), 400

    h_count = board.count('h')
    m_count = board.count('m')

    if h_count != m_count + 1:
        return jsonify({'detail': 'Invalid board configuration'}), 400

    encounteredEmpty = True
    for i in range(len(board)):
        if(i%6 == 0 and board[i] != '0'):
            encounteredEmpty = False
            continue
        if(i%6 != 0 and board[i] == '0'):
            encounteredEmpty = True
            continue
        if(board[i] != '0' and encounteredEmpty):
            return jsonify({'detail': 'Invalid board configuration'}), 400
        
        if(board[i] == '0'):
            encounteredEmpty = True
            continue
        if(board[i] != '0'):
            encounteredEmpty = False
            continue
            
    [m_board,h_board]=transform_board(board)
    
    player1 = AI()
    player2 = AI()

    customBoard = Board(player1, player2, turn=0, bitboards=[m_board,h_board])
    
    if(customBoard.hasWon(customBoard.BITBOARDS[0])):
        return jsonify({'detail': 'Game is Over'}), 422
    
    if(customBoard.hasWon(customBoard.BITBOARDS[1])):
        return jsonify({'detail': 'Game is Over'}), 422
    
    if(customBoard.hasDrawn(customBoard.BITBOARDS[0] & customBoard.BITBOARDS[1])):
        return jsonify({'detail': 'Board is full'}), 422

    next_move = player1.play(customBoard)

    if(next_move == -1):
        return jsonify({'detail': 'Board is full'}), 422

    return jsonify(next_move), 200

def transform_board(board):
    
    board = np.array(list(board)).reshape(7,6)
    board = np.hstack((board, np.array([[0]]).repeat(board.shape[0], axis=0)))
    board = board.flatten()
    board = np.flip(board)

    m_mask = board == 'm'
    h_mask = board == 'h'

    m_arr = np.char.array(['0'] * len(board))
    h_arr = np.char.array(['0'] * len(board))

    m_arr[m_mask] = '1'
    h_arr[h_mask] = '1'

    m_arr[h_mask] = '0'

    h_arr[m_mask] = '0'

    m_arr = np.array2string(m_arr, separator='')[1:-1].replace(' ', '').replace('\n', '').replace('\'','')
    h_arr = np.array2string(h_arr, separator='')[1:-1].replace(' ', '').replace('\n', '').replace('\'','')

    return int(m_arr, 2), int(h_arr, 2)


if __name__ == '__main__':
    app.run()
