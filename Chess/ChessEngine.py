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
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkMate = False  # When King has no valid moves and is in check
        self.staleMate = False  # When King has no valid moves and is not in check
        self.enpassantPossible = ()  # Coordinates for the square where en-passant capture is possible

    '''
    Takes a Move as a parameter and executes the move.
    Note: This does not work for castling, pawn promotion, and en-passant.
    '''
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)  # Log the move in case we want to undo it later
        self.whiteToMove = not self.whiteToMove  # Switch turns, swap to other player's turn
        # Update the king's location if moved
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)

        # Check for pawn promotion
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'

        # Check for en-passant
        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol] = '--'  # Capturing the pawn

        # Update enpassantPossible variable
        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:  # On 2-square pawn advances
            self.enpassantPossible = ((move.startRow + move.endRow)//2, move.startCol)
        else:
            self.enpassantPossible = ()

    '''
    Undo the last move made.
    '''
    def undoMove(self):
        if len(self.moveLog) != 0:  # Make sure that there is a move to undo
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove  # Switch turns back
            # Update the king's position if undoing a move
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)
            # Undo en-passant move
            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol] = '--'  # Leave landing square blank
                self.board[move.startRow][move.endCol] = move.pieceCaptured
                self.enpassantPossible = (move.endRow, move.endCol)
            # Undo a 2-square pawn advance
            if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
                self.enpassantPossible = ()


    '''
    All moves considering checks.
    '''
    def getValidMoves(self):
        tempEnpassantPossible = self.enpassantPossible
        # 1) Get all possible moves
        moves = self.getAllPossibleMoves()
        # 2) For each move, make the move
        for i in range(len(moves) -1, -1, -1):  # Need to remove from end so an element isn't skipped due to index shift
            self.makeMove(moves[i])  # When making a move, it swaps turns (Ie. If white, it swaps to black)
            self.whiteToMove = not self.whiteToMove  # Need to swap back since inCheck() swaps to see opponent's moves
            # 3) Generate all opponent's moves
            # 4) For each of your opponent's moves, see if they attack your king
            if self.inCheck():
                # 5) If they do attack your king, not a valid move and remove it
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove  # Cancel out the swap back
            self.undoMove()  # Cancel out the makeMove() since it's just checking
        if len(moves) == 0:  # Checkmated or stalemated
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        else:  # If we undid a move and checkmate/stalemate turned to true, need to turn back to False
            self.checkMate = False
            self.staleMate = False

        self.enpassantPossible = tempEnpassantPossible
        return moves

    '''
    Determines if the current player is in check.
    '''
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    '''
    Determines if the enemy can attack the square r,c.
    '''
    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove  # Need to switch to opponent's PoV to see their moves
        oppMoves = self.getAllPossibleMoves()  # Generate all opponent's moves
        self.whiteToMove = not self.whiteToMove  # Switch turns back to keep turns in correct order
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:  # If square is under attack
                return True
        return False

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
                elif (r-1, c-1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r-1, c-1), self.board, isEnPassantMove=True))
            if c+1 <= 7:  # Capturing to the right
                if self.board[r-1][c+1][0] == 'b':  # Enemy piece to capture
                    moves.append(Move((r, c), (r-1, c+1), self.board))
                elif (r-1, c+1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r-1, c+1), self.board, isEnPassantMove=True))

        else:  # Black pawn moves
            if self.board[r+1][c] == "--":  # 1 square pawn advance
                moves.append(Move((r, c), (r+1, c), self.board))
                if r == 1 and self.board[r+2][c] == "--":  # 2 square pawn advance
                    moves.append(Move((r, c), (r+2, c), self.board))
            if c-1 >= 0:  # Capturing to the left
                if self.board[r+1][c-1][0] == 'w':  # Enemy piece to capture
                    moves.append(Move((r, c), (r+1, c-1), self.board))
                elif (r+1, c-1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r+1, c-1), self.board, isEnPassantMove=True))
            if c+1 <= 7:  # Capturing to the right
                if self.board[r+1][c+1][0] == 'w':  # Enemy piece to capture
                    moves.append(Move((r, c), (r+1, c+1), self.board))
                elif (r+1, c+1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r+1, c+1), self.board, isEnPassantMove=True))

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

    def __init__(self, startSq, endSq, board, isEnPassantMove=False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        # Pawn promotion
        self.isPawnPromotion = False
        if (self.pieceMoved == 'wp' and self.endRow == 0) or (self.pieceMoved == 'bp' and self.endRow == 7):
            self.isPawnPromotion = True

        # En-passant
        self.isEnpassantMove = isEnPassantMove
        if self.isEnpassantMove:
            self.pieceCaptured = 'wp' if self.pieceMoved == 'bp' else 'bp'

        self.moveId = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

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