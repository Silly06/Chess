import json


# function takes the game data and saves it in a JSON file
def saveChessBoard(gameData):
    listToExport = [gameData.chessboard, gameData.currentTurn, gameData.castlingStates, gameData.lastDouble]
    jsonSave = json.dumps(listToExport, indent=4)
    print("Saving your game...")
    # Writing to savedChessGame.json
    with open("savedChessGame.json", "w") as outfile:
        outfile.write(jsonSave)


# function takes the JSON file and sets the game data to the contents
def loadChessBoard():
    saveData = False
    inputLoad = input("Load saved game? (yes/no) ")
    if inputLoad.lower() == "yes" or inputLoad.lower() == "y":
        rawSaveData = open("savedChessGame.json")
        saveData = json.load(rawSaveData)
    return saveData
