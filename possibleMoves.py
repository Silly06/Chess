import checkBoard
import copy
import piece

columnToNumber = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']


# function finds positions a knight on the board can move to
def knightMovePositions(chessBoard, initialX, initialY, currentTurn):
    positions = []
    # creates binary for loops that test for all 8 positions the knight can move to
    for xPlusMinus in ["+", "-"]:
        for yPlusMinus in ["+", "-"]:
            for length in [[1, 2], [2, 1]]:
                # adds lengths to the x and y, either 2 or 1, creating L shapes to move in
                if xPlusMinus == "+":
                    targetX = initialX + length[0]
                else:
                    targetX = initialX - length[0]
                if yPlusMinus == "+":
                    targetY = initialY + length[1]
                else:
                    targetY = initialY - length[1]
                # try except used so that it only detects tiles within board
                try:
                    targetPiece = piece.Piece(chessBoard[targetY][targetX])
                    if targetPiece.colour != currentTurn and targetY >= 0 and targetX >= 0:
                        positions.append([targetX, targetY])
                except IndexError:
                    pass
    return positions


# functions find all tiles a pawn can move to
def pawnMovePositions(chessboard, initialX, initialY, currentTurn, lastMoveDouble):
    # function checks 3 tiles ahead and the tile 2 ahead, if the pawn hasn't moved yet
    positions = []
    # sets the direction and row that a pawn can move double to, based on the colour
    pawnDirection = 1
    doublePawnMoveRow = 1
    enPassantRow = 4
    if currentTurn == "white":
        pawnDirection = -1
        doublePawnMoveRow = 6
        enPassantRow = 3
    # checks the tile directly in front of it, if the tile is empty

    try:
        # checks the piece in front of it, by adding the piece's y value and adding the direction
        if chessboard[initialY + pawnDirection][initialX] == " " and initialY + pawnDirection >= 0:
            positions.append([initialX, initialY + pawnDirection])
    except IndexError:
        pass
    try:
        # checks the piece 2 pieces ahead, checks if it's in the row it can double move to
        targetPiece = piece.Piece(chessboard[initialY + 2 * pawnDirection][initialX])
        if doublePawnMoveRow == initialY and initialY + pawnDirection >= 0 and\
                not targetPiece.colour:
            positions.append([initialX, initialY + 2 * pawnDirection])
    except IndexError:
        pass
    # loops twice, checks the 2 pieces diagonally ahead
    for leftRight in [-1, 1]:
        try:
            diagonalPiece = piece.Piece(chessboard[initialY + pawnDirection][initialX + leftRight])
            if diagonalPiece.colour and diagonalPiece.colour != currentTurn and initialX + leftRight >= 0 and\
                    initialY + pawnDirection >= 0:
                positions.append([initialX + leftRight, initialY + pawnDirection])
            elif lastMoveDouble and initialX + leftRight >= 0 and initialY == enPassantRow and not diagonalPiece.colour:

                if lastMoveDouble == initialX + leftRight:
                    positions.append([initialX + leftRight, initialY + pawnDirection])
        except IndexError:
            pass
    return positions


# function checks a certain direction for valid moves
# used to check the directions of the bishop, rook and queen
def checkSurrounding(chessboard, initialX, initialY, currentTurn, xDirection, yDirection, xEnd, yEnd):
    positions = []
    pieceNotFound = True
    # moves the starting point by 1, so that it begins on the adjacent tile
    xTarget = initialX + xDirection
    yTarget = initialY + yDirection
    # loops till a piece is found or if it hits the end of the board in x or y direction
    while pieceNotFound and xTarget != xEnd and yTarget != yEnd:
        targetPiece = piece.Piece(chessboard[yTarget][xTarget])
        # checks if tile is empty, adds position as a valid move
        if not targetPiece.colour:
            positions.append([xTarget, yTarget])
        # checks if the tile is the same colour, causes a break in the loop
        elif targetPiece.colour == currentTurn:
            pieceNotFound = False
        # runs if the tile is the other colour, adds as a valid move, but also breaks the loop
        else:
            positions.append([xTarget, yTarget])
            pieceNotFound = False
        # iterates the direction
        xTarget = xTarget + xDirection
        yTarget = yTarget + yDirection
    return positions


def kingMovePositions(chessboard, initialX, initialY, currentTurn, inCheck, castlingStates):
    positions = []
    # loops through 3 ways the y can change, and 3 ways the x can change, giving 9 possibilities
    for yMovement in [-1, 0, 1]:
        for xMovement in [-1, 0, 1]:
            # checks if the king is actually moving, and not moving into negative index tiles
            if not (yMovement == 0 and xMovement == 0) and initialY + yMovement >= 0 and initialX + xMovement >= 0:
                # try except to prevent moving outside the board
                try:
                    # adds it as a valid move if the tile is empty or filled by opposing piece
                    targetPiece = piece.Piece(chessboard[initialY + yMovement][initialX + xMovement])
                    if targetPiece.colour != currentTurn:
                        positions.append([initialX + xMovement, initialY + yMovement])
                except IndexError:
                    pass
    for move in positions:
        # creates a temporary copy of the chessboard, makes the possible move, tests if the current player is in  check
        temporaryBoard = copy.deepcopy(chessboard)
        tileToMove = temporaryBoard[initialY][initialX]
        temporaryBoard[move[1]][move[0]] = tileToMove
        temporaryBoard[initialY][initialX] = " "
        # removes the illegal move in the main list, without breaking the loop
        if checkBoard.checkState(temporaryBoard, currentTurn):
            positions.remove(move)
    rowToCheck = 0
    castlingStatesToCheck = castlingStates[1]
    if currentTurn == "white":
        rowToCheck = 7
        castlingStatesToCheck = castlingStates[0]
    if castlingStatesToCheck[0] and not inCheck:
        if castlingStatesToCheck[1] and [3, rowToCheck] in positions:
            positions.append([2, rowToCheck])
        if castlingStatesToCheck[2] and [5, rowToCheck] in positions:
            positions.append([6, rowToCheck])

    return positions


# function checks right left down up to find spaces that a rook can move to
def rookMovePositions(chessboard, initialX, initialY, currentTurn):
    positions = []
    # Check directions up down left right
    positions.extend(checkSurrounding(chessboard, initialX, initialY, currentTurn, 1, 0, 8, 10))
    positions.extend(checkSurrounding(chessboard, initialX, initialY, currentTurn, -1, 0, -1, 10))
    positions.extend(checkSurrounding(chessboard, initialX, initialY, currentTurn, 0, 1, 10, 8))
    positions.extend(checkSurrounding(chessboard, initialX, initialY, currentTurn, 0, -1, 10, -1))

    return positions


def bishopMovePositions(chessboard, initialX, initialY, currentTurn):
    positions = []
    # checks directions in each of the 4 diagonal directions
    positions.extend(checkSurrounding(chessboard, initialX, initialY, currentTurn, 1, 1, 8, 8))
    positions.extend(checkSurrounding(chessboard, initialX, initialY, currentTurn, 1, -1, 8, -1))
    positions.extend(checkSurrounding(chessboard, initialX, initialY, currentTurn, -1, -1, -1, -1))
    positions.extend(checkSurrounding(chessboard, initialX, initialY, currentTurn, -1, 1, -1, 8))
    return positions


def queenMovePositions(chessboard, initialX, initialY, currentTurn):
    positions = []
    # uses the bishop and rook functions, since the queen can move anywhere that either of those pieces can
    positions.extend(rookMovePositions(chessboard, initialX, initialY, currentTurn))
    positions.extend(bishopMovePositions(chessboard, initialX, initialY, currentTurn))
    return positions


def findMoves(gameData, initialX, initialY, inCheck):
    # establishes game data variables for easier use
    chessboard = gameData.chessboard
    currentTurn = gameData.currentTurn
    lastMoveDouble = gameData.lastDouble
    castlingStates = gameData.castlingStates

    targetPiece = piece.Piece(chessboard[initialY][initialX])
    positions = []
    # gets the moves based on the type of piece is selected
    if targetPiece.type == "knight":
        positions = knightMovePositions(chessboard, initialX, initialY, currentTurn)
    elif targetPiece.type == "pawn":
        positions = pawnMovePositions(chessboard, initialX, initialY, currentTurn, lastMoveDouble)
    elif targetPiece.type == "rook":
        positions = rookMovePositions(chessboard, initialX, initialY, currentTurn)
    elif targetPiece.type == "queen":
        positions = queenMovePositions(chessboard, initialX, initialY, currentTurn)
    elif targetPiece.type == "bishop":
        positions = bishopMovePositions(chessboard, initialX, initialY, currentTurn)
    elif targetPiece.type == "king":
        positions = kingMovePositions(chessboard, initialX, initialY, currentTurn, inCheck, castlingStates)
    # creates a copy of the list of possible moves to loop through
    testMoves = copy.deepcopy(positions)
    for move in testMoves:
        # creates a temporary copy of the chessboard, makes the possible move, tests if the current player is in  check
        temporaryBoard = copy.deepcopy(chessboard)
        tileToMove = temporaryBoard[initialY][initialX]
        temporaryBoard[move[1]][move[0]] = tileToMove
        temporaryBoard[initialY][initialX] = " "
        # removes the illegal move in the main list, without breaking the
        illegalMove = checkBoard.checkState(temporaryBoard, currentTurn)
        if illegalMove:
            positions.remove(move)

    return positions
