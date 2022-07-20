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
        self.moveFunctions = {'p' : self.getPawnMoves, 'R' : self.getRookMoves, 'N' : self.getKnightMoves,
                              'B' : self.getBishopMoves, 'Q' : self.getQueenMoves, 'K' : self.getKingMoves}
        self.whiteToMove = True
        self.moveLog = []

    '''
    Takes a Move as a parameter and executes the move.
    Note: This does not work for castling, pawn promotion, and en-passant.
    '''
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)  # Log the move in case we want to undo it later
        self.whiteToMove = not self.whiteToMove  # Switch turns, swap to other player's turn

    '''
    Undo the last move made.
    '''
    def undoMove(self):
        if len(self.moveLog) != 0:  # Make sure that there is a move to undo
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove  # Switch turns back

    '''
    All moves considering checks.
    '''
    def getValidMoves(self):
        return self.getAllPossibleMoves()  # For now, we won't worry about checks

    '''
    All moves without considering checks.
    '''
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):  # Number of rows
            for c in range(len(self.board[r])):  # Number of columns in a given row
                turn = self.board[r][c][0]  # Get the first character (Ie. color)
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)  # Calls the appropriate move functions using dictionary
        return moves

    '''
    Get all the pawn moves for the pawn located at row, col and add these moves to the list.
    '''
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:  # White pawn moves
            if self.board[r-1][c] == "--":  # 1 square pawn advance
                moves.append(Move((r, c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == "--":  # 2 square pawn advance
                    moves.append(Move((r, c), (r-2, c), self.board))
            if c-1 >= 0:  # Capturing to the left
                if self.board[r-1][c-1][0] == 'b':  # Enemy piece to capture
                    moves.append(Move((r, c), (r-1, c-1), self.board))
            if c+1 <= 7:  # Capturing to the right
                if self.board[r-1][c+1][0] == 'b':  # Enemy piece to capture
                    moves.append(Move((r, c), (r-1, c+1), self.board))

        else:  # Black pawn moves
            if self.board[r+1][c] == "--":  # 1 square pawn advance
                moves.append(Move((r, c), (r+1, c), self.board))
                if r == 1 and self.board[r+2][c] == "--":  # 2 square pawn advance
                    moves.append(Move((r, c), (r+2, c), self.board))
            if c-1 >= 0:  # Capturing to the left
                if self.board[r+1][c-1][0] == 'w':  # Enemy piece to capture
                    moves.append(Move((r, c), (r+1, c-1), self.board))
            if c+1 <= 7:  # Capturing to the right
                if self.board[r+1][c+1][0] == 'w':  # Enemy piece to capture
                    moves.append(Move((r, c), (r+1, c+1), self.board))

    '''
    Get all the rook moves for the rook located at row, col and add these moves to the list.
    '''
    def getRookMoves(self, r, c, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))  # Up, left, down, right
        enemyColor = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:  # On the board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '--':  # Empty space
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece [0] == enemyColor:  # Enemy piece
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:  # Friendly piece
                        break
                else:  # Off the board
                    break

    '''
    Get all the knight moves for the knight located at row, col and add these moves to the list.
    '''
    def getKnightMoves(self, r, c, moves):
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        enemyColor = 'b' if self.whiteToMove else 'w'
        for km in knightMoves:
            endRow = r + km[0]
            endCol = c + km[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:  # On the board
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor or endPiece == '--':
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    '''
    Get all the bishop moves for the bishop located at row, col and add these moves to the list.
    '''
    def getBishopMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))  # Upper-left, Upper-right, Bottom-left, Bottom-right
        enemyColor = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:  # On the board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '--':  # Empty space
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece [0] == enemyColor:  # Enemy piece
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:  # Friendly piece
                        break
                else:  # Off the board
                    break

    '''
    Get all the queen moves for the queen located at row, col and add these moves to the list.
    '''
    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

    '''
    Get all the king moves for the king located at row, col and add these moves to the list.
    '''
    def getKingMoves(self, r, c, moves):
        kingMoves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        enemyColor = 'b' if self.whiteToMove else 'w'
        for i in range(8):
            endRow = r + kingMoves[i][0]
            endCol = c + kingMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor or endPiece == '--':
                    moves.append(Move((r, c), (endRow, endCol), self.board))


class Move():
    # Maps keys to values
    # Key : value
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    # Creates a dictionary by flipping the ranksToRows dictionary
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    # Creates a dictionary by flipping the filesToCols dictionary
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveId = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        print(self.moveId)

    '''
    Overriding the equals method.
    '''
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveId == other.moveId
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]