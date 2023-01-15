import printBoard
import makeMove
import saveChessboard
import gameData


gameData = gameData.GameData([
    ['♜', '♞', '♝', '♛', '♚', '♝', '♞', '♜'],
    ['♟', '♟', '♟', '♟', '♟', '♟', '♟', '♟'],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ['♙', '♙', '♙', '♙', '♙', '♙', '♙', '♙'],
    ['♖', '♘', '♗', '♕', '♔', '♗', '♘', '♖'],
    ], "white", [[True, True, True], [True, True, True]], False)
# set of variables contains game data that continually changes
# variable holds whose turn it is

# asks user if they want to load the saved JSON file, and sets the chessboard and current turn to it if so
saveData = saveChessboard.loadChessBoard()
if saveData:
    gameData.chessboard = saveData[0]
    gameData.currentTurn = saveData[1]
    gameData.castlingStates = saveData[2]
    gameData.lastDouble = saveData[3]

# prints the board and starting player
printBoard.printChessBoard(gameData.chessboard)
print(gameData.currentTurn + "'s turn")
gameRunning = True

# loop for a turn being processed, till game ends
while gameRunning:
    gameRunning = makeMove.makeMove(gameData)
