# prints the board
def printChessBoard(chessboard):
    currentRow = 8
    # iterates through each row
    for row in chessboard:
        # prints seperator
        print("———————————————————————————————————————————————————")
        # prints out the row number, the actual row, separated by a space and a pipe
        if currentRow % 2 == 0:
            print(f"{currentRow} ⎟  {row[0]}  ⎟[|{row[1]}|]⎟  {row[2]}  ⎟[|{row[3]}|]⎟  {row[4]}  ⎟[|{row[5]}|]⎟  "
                  f"{row[6]}  ⎟[|{row[7]}|]⎟")
        else:
            print(f"{currentRow} ⎟[|{row[0]}|]⎟  {row[1]}  ⎟[|{row[2]}|]⎟  {row[3]}  ⎟[|{row[4]}|]⎟  {row[5]}  "
                  f"⎟[|{row[6]}|]⎟  {row[7]}  ⎟")
        currentRow = currentRow - 1
    # bottom of the chessboard, with column names
    print("———————————————————————————————————————————————————")
    print("  |  a  |  b  |  c  |  d  |  e  |  f  |  g  |  h  |")
