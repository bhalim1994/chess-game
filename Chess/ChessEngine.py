"""
Responsible for storing all the information about the current state of a chess game.
Also responsible for determining the valid moves at the current state and keeping a move log.
"""
class GameState():
    def __init__(self):
        # Board is an 8x8 2D list and each element of the list has 2 characters.
        # First character represents the color, 'b' or 'w'.
        # Second character represents the type of the piece, 'K', 'Q', 'R', 'B', 'N', or 'p'.
        # The '--' represents an empty space with no piece.
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.whiteToMove = True
        self.moveLog = []