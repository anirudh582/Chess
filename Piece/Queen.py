from Piece.Rook import Rook
from Piece.Bishop import Bishop

class Queen:
    id = 'Q'
    def __init__(self,alliance,coord):
        self.alliance = alliance
        self.coord = coord
    def allowed_moves(self, board):
        allowed_moves=[]
        temp_rook = Rook(self.alliance,self.coord)
        temp_bishop = Bishop(self.alliance,self.coord)
        if len(temp_rook.allowed_moves(board)):
            for square in temp_rook.allowed_moves(board):
                allowed_moves.append(square)
        if len(temp_bishop.allowed_moves(board)):
            for square in temp_bishop.allowed_moves(board):
                allowed_moves.append(square)
        return allowed_moves
