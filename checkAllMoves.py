import possibleMoves
import piece


# function iterates through board, creates a list of all possible moves, and checks if the player has no valid moves
# used to identify checkmate/stalemate
def checkNoMoves(gameData, inCheck):
    allMoves = []
    # iteration through board, y and x
    for findY in range(0, 8):
        for findX in range(0, 8):
            # grabs the colour of the selected tile, and runs if it belongs to the current player
            targetPiece = piece.Piece(gameData.chessboard[findY][findX])
            if targetPiece.colour == gameData.currentTurn:
                # calls function that looks for moves for that piece, then appends it to a lis
                targetMoves = possibleMoves.findMoves(gameData, findX, findY, inCheck)
                allMoves.extend(targetMoves)
    # checks if the list of possible moves is empty, and if so, returns true
    noMoves = False
    if len(allMoves) == 0:
        noMoves = True
    return noMoves
