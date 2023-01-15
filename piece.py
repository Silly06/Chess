class Piece:
    def __init__(self, piece):
        blackSymbols = ['♜', '♞', '♝', '♛', '♚', '♟']
        whiteSymbols = ['♖', '♘', '♗', '♕', '♔', '♙']
        colour = False
        if piece in whiteSymbols:
            colour = "white"
        elif piece in blackSymbols:
            colour = "black"
        pieceType = False
        if piece == "♜" or piece == "♖":
            pieceType = "rook"
        if piece == "♞" or piece == "♘":
            pieceType = "knight"
        if piece == "♝" or piece == "♗":
            pieceType = "bishop"
        if piece == "♛" or piece == "♕":
            pieceType = "queen"
        if piece == "♚" or piece == "♔":
            pieceType = "king"
        if piece == "♟" or piece == "♙":
            pieceType = "pawn"
        self.piece = piece
        self.colour = colour
        self.type = pieceType
