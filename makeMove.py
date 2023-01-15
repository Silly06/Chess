import checkBoard
import checkAllMoves
import printBoard
import saveChessboard
import possibleMoves
import piece

# general reference lists
turns = ["black", "white"]
columnToNumber = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
validRowNumbers = ['8', '7', '6', '5', '4', '3', '2', '1']
colourPieceTypeToSymbol = {"white": {"rook": '♖', "knight": '♘', "bishop": '♗', "queen": '♕'},
                           "black": {"rook": '♜', "knight": '♞', "bishop": '♝', "queen": '♛'}}


# function changes a pawn to another piece upon reaching the end
def promotePawn(initialPiece, currentTurn):
    pawnPromoted = False
    while not pawnPromoted:
        inputChangedPiece = input(
            "What piece would you like to change to? ").lower()
        if inputChangedPiece in ["queen", "knight", "rook", "bishop"]:
            changedPiece = inputChangedPiece
            pawnPromoted = True
            initialPiece.piece = colourPieceTypeToSymbol[currentTurn][changedPiece]


# prints the list of valid functions for a piece
def validMovesOut(validMoves):
    movesOut = "Valid moves are "
    for move in validMoves:
        movesOut = movesOut + columnToNumber[move[0]] + validRowNumbers[move[1]] + " "
    print(movesOut)


# moves the rook when the king castles
def moveRookCastling(chessboard, castlingStatesToCheck, initialX, movedX, movedY):
    castlingStatesToCheck[0] = False
    if movedX == 2 and initialX == 4:
        castlingStatesToCheck[1] = False
        chessboard[movedY][3] = chessboard[movedY][0]
        chessboard[movedY][0] = " "
    elif movedX == 6:
        castlingStatesToCheck[2] = False
        chessboard[movedY][5] = chessboard[movedY][7]
        chessboard[movedY][7] = " "


# moves the piece at the end of a turn
def movePiece(gameData, initialX, initialY, movedX, movedY, initialPiece):
    chessboard = gameData.chessboard
    castlingStates = gameData.castlingStates
    movedPiece = piece.Piece(chessboard[movedY][movedX])
    # sets the castling states variable based on the whose turn it is
    castlingStatesToCheck = castlingStates[1]
    if gameData.currentTurn == "white":
        castlingStatesToCheck = castlingStates[0]

    # moves the rook if the king castles
    if initialPiece.type == "king":
        moveRookCastling(chessboard, castlingStatesToCheck, initialX, movedX, movedY)

    # updates a variable if the rook moves
    if initialPiece.type == "rook":
        if initialX == 0:
            castlingStatesToCheck[1] = False
        elif movedX == 7:
            castlingStatesToCheck[2] = False

    # changes the pawn to another piece if it reaches the end
    if initialPiece.type == "pawn" and (movedY == 7 or movedY == 0):
        promotePawn(initialPiece, gameData.currentTurn)

    # checks if the move is the pawn moving 2 spaces ahead
    gameData.lastDouble = False
    if initialPiece.type == "pawn" and (initialY == 1 and movedY == 3) or (
            initialY == 6 and movedY == 4):
        gameData.lastDouble = movedX

    # takes away other pawn if move is en passant
    if initialPiece.type == "pawn" and not movedPiece.colour and initialX != movedX:
        chessboard[initialY][movedX] = " "

    # moves the piece on the board
    chessboard[initialY][initialX] = " "
    chessboard[movedY][movedX] = initialPiece.piece


# checks for a game end and outputs if so
def continueGameCheck(gameData, inCheck):
    gameRunning = True
    noMoves = checkAllMoves.checkNoMoves(gameData, inCheck)
    if inCheck and noMoves:
        print("Checkmate!")
        print(f"Winner is {str(turns[abs(turns.index(gameData.currentTurn) - 1)])}!")
        gameRunning = False
    elif noMoves:
        print("Stalemate!")
        print("Game is a tie!")
        gameRunning = False
    return gameRunning


# makes the move of a player
def makeMove(gameData):
    chessboard = gameData.chessboard
    inCheck = checkBoard.checkState(chessboard, gameData.currentTurn)
    gameRunning = continueGameCheck(gameData, inCheck)
    if gameRunning:
        if inCheck:
            print("Check!")
        # takes the input move a piece
        moveMade = False
        inputInitialPosition = input("Move what piece? ")
        if len(inputInitialPosition) == 2:
            if inputInitialPosition[0] in columnToNumber and inputInitialPosition[1] in validRowNumbers:
                initialX = int(columnToNumber.index(inputInitialPosition[0]))
                initialY = abs(int(inputInitialPosition[1]) - 8)
                validMoves = possibleMoves.findMoves(gameData, initialX, initialY, inCheck)
                initialPiece = piece.Piece(chessboard[initialY][initialX])
                if initialPiece.colour == gameData.currentTurn and len(validMoves) != 0:
                    # outputs a list of valid moves if there are any
                    validMovesOut(validMoves)
                    inputMovedPosition = input("Move to where? ")
                    if len(inputMovedPosition) == 2:
                        if inputMovedPosition[0] in columnToNumber and inputMovedPosition[1] in validRowNumbers:
                            # declares the index of the x and y coordinates of where the piece is moving from and to
                            movedX = int(columnToNumber.index(inputMovedPosition[0]))
                            movedY = abs(int(inputMovedPosition[1]) - 8)
                            if [movedX, movedY] in validMoves:
                                movePiece(gameData, initialX, initialY, movedX, movedY, initialPiece)
                                moveMade = True
                            # output messages for invalid inputs
                            else:
                                print("That's not one of the valid moves")
                        else:
                            print("That's not a tile!")
                    else:
                        print("That's not a tile!")
                else:
                    print("That's not a piece your can move!")
            else:
                print("That's not a tile!")
        # saves the game's state to a JSON file if the user requests
        elif inputInitialPosition.lower() == "save":
            saveChessboard.saveChessBoard(gameData)
        # last output message for an invalid inputs
        else:
            print("That's not a tile!")
        # rotates turn
        if moveMade:
            printBoard.printChessBoard(chessboard)
            gameData.currentTurn = turns[abs(turns.index(gameData.currentTurn) - 1)]
            print(gameData.currentTurn + "'s turn")
    return gameRunning
