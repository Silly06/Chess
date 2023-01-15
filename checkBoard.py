import piece
# reference lists
blackSymbols = ['♜', '♞', '♝', '♛', '♚', '♟']
whiteSymbols = ['♖', '♘', '♗', '♕', '♔', '♙']
colours = ["white", "black"]


# function iterates through entire board, returns position of the king
def findKing(chessboard, currentTurn):
    kingPosition = False
    for searchY in range(0, 8):
        for searchX in range(0, 8):
            if (chessboard[searchY][searchX] == "♔" and currentTurn == "white") or \
                    (chessboard[searchY][searchX] == "♚" and currentTurn == "black"):
                kingPosition = [searchX, searchY]
    return kingPosition


# function that checks for a directional piece in a direction, i.e. bishop, rook, queen
def checkThreateningSurrounding(chessboard, initialX, initialY, pieceColour,
                                xDirection, yDirection, xEnd, yEnd, threateningPiece):
    kingThreatened = False
    pieceNotFound = True
    xTarget = initialX + xDirection
    yTarget = initialY + yDirection
    while pieceNotFound and xTarget != xEnd and yTarget != yEnd:
        targetPiece = piece.Piece(chessboard[yTarget][xTarget])
        if targetPiece.colour:
            if targetPiece.colour != pieceColour and targetPiece.type == threateningPiece:
                kingThreatened = True
            pieceNotFound = False
        xTarget = xTarget + xDirection
        yTarget = yTarget + yDirection
    return kingThreatened


# function looping through all directions, looking for rooks, bishops and queens threatening
def directionalCheck(chessboard, kingX, kingY, currentTurn):
    directionalThreatening = False
    # list with all the directions to check for, and what pieces to check for in those directions
    directionalPieces = [[-1, -1, -1, -1, "bishop"], [-1, 1, -1, 8, "bishop"], [1, -1, 8, -1, "bishop"],
                         [1, 1, 8, 8, "bishop"], [-1, 0, -1, 10, "rook"], [1, 0, 8, 10, "rook"],
                         [0, -1, 10, -1, "rook"], [0, 1, 10, 8, "rook"], [-1, -1, -1, -1, "queen"],
                         [-1, 1, -1, 8, "queen"], [1, -1, 8, -1, "queen"], [1, 1, 8, 8, "queen"],
                         [-1, 0, -1, 10, "queen"], [1, 0, 8, 10, "queen"], [0, -1, 10, -1, "queen"],
                         [0, 1, 10, 8, "queen"]]
    for directionToCheck in directionalPieces:
        xDirection = directionToCheck[0]
        yDirection = directionToCheck[1]
        xEnd = directionToCheck[2]
        yEnd = directionToCheck[3]
        threateningPiece = directionToCheck[4]
        if checkThreateningSurrounding(chessboard, kingX, kingY, currentTurn,
                                       xDirection, yDirection, xEnd, yEnd, threateningPiece):
            directionalThreatening = True
    return directionalThreatening


# checks if the other king is in the 8 tiles surrounding
def kingCheck(chessboard, kingX, kingY, currentTurn):
    kingThreatening = False
    for yMovement in [-1, 0, 1]:
        for xMovement in [-1, 0, 1]:
            if not (yMovement == 0 and xMovement == 0) and kingY + yMovement >= 0 and kingX + xMovement >= 0:
                try:
                    targetPiece = piece.Piece(chessboard[kingY + yMovement][kingX + xMovement])
                    if targetPiece.colour and targetPiece.type == "king" and targetPiece.colour != currentTurn:
                        kingThreatening = True
                except IndexError:
                    pass
    return kingThreatening


# checks the 2 diagonal pieces ahead for if they are enemy pawns
def pawnCheck(chessboard, kingX, kingY, currentTurn):
    pawnThreatening = False
    pawnCheckDirection = 1
    if currentTurn == "white":
        pawnCheckDirection = -1
    for leftRight in [-1, 1]:
        try:
            diagonalPiece = piece.Piece(chessboard[kingY + pawnCheckDirection][kingX + leftRight])

            if diagonalPiece.colour and diagonalPiece.colour != currentTurn and diagonalPiece.type == "pawn":
                pawnThreatening = True
        except IndexError:
            pass
    return pawnThreatening


# function checks for opposing knights in L shapes from the king
def knightCheck(chessboard, kingX, kingY, currentTurn):
    knightThreatening = False
    for xPlusMinus in ["+", "-"]:
        for yPlusMinus in ["+", "-"]:
            for length in [[1, 2], [2, 1]]:
                if xPlusMinus == "+":
                    targetX = kingX + length[0]
                else:
                    targetX = kingX - length[0]
                if yPlusMinus == "+":
                    targetY = kingY + length[1]
                else:
                    targetY = kingY - length[1]
                # try except used so that it only detects tiles within board
                try:
                    targetPiece = piece.Piece(chessboard[targetY][targetX])
                    if targetPiece.colour and targetPiece.colour != currentTurn and \
                            targetPiece.type == "knight" and targetY >= 0 \
                            and targetX >= 0:
                        knightThreatening = True
                except IndexError:
                    pass
    return knightThreatening


# checks the state of the game, whether the current king is under check
def checkState(chessboard, currentTurn):
    # gets the king's position
    kingPosition = findKing(chessboard, currentTurn)
    kingX = kingPosition[0]
    kingY = kingPosition[1]
    # calls all the check functions, combines them to return a boolean whether the king is under check
    directionalThreatening = directionalCheck(chessboard, kingX, kingY, currentTurn)
    kingThreatening = kingCheck(chessboard, kingX, kingY, currentTurn)
    pawnThreatening = pawnCheck(chessboard, kingX, kingY, currentTurn)
    knightThreatening = knightCheck(chessboard, kingX, kingY, currentTurn)
    inCheck = directionalThreatening or kingThreatening or pawnThreatening or knightThreatening

    return inCheck
