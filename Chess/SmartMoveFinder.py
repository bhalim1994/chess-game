import random

# If positive value, winning for white. If negative value, winning for black.
pieceScore = {"K": 0, "Q": 10, "R": 5, "B": 3, "N": 3, "p": 1}
CHECKMATE = 1000
STALEMATE = 0

'''
Picks and returns a random move.
'''
def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]

'''
Finds the best move based on pieces alone.
'''
def findBestMove(gs, validMoves):
    turnMultiplier = 1 if gs.whiteToMove else -1

    maxScore = -CHECKMATE   # Initialize worst possible score for white
    bestMove = None
    for playerMove in validMoves:
        gs.makeMove(playerMove)
        if gs.checkmate:
            score = CHECKMATE
        elif gs.stalemate:
            score = STALEMATE
        else:
            score = turnMultiplier * scoreMaterial(gs.board)
        if maxScore < score:
            maxScore = score
            bestMove = playerMove
        gs.undoMove()  # Need to undo the move so it doesn't make all the moves it's evaluating
    return bestMove

'''
Score board based on material.
'''
def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            elif square[0] == 'b':
                score -= pieceScore[square[1]]
    return score