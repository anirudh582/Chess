from helper import *
class King:
    id = 'K'
    def __init__(self,alliance,coord):
        self.alliance = alliance
        self.coord = coord
    def allowed_moves(self,board):
        allowed_moves=[]
        for i in range(-1,2):
            for j in range(-1,2):
                if i == 0 and j == 0:
                    continue
                square = (self.coord[0]+i,self.coord[1]+j)
                #if coord_inside_board(square) and ((null_piece(board,square) and not check(board, square, self.alliance)) or enemy_piece(board,square,self.alliance)):
                if coord_inside_board(square): 
                    allowed_moves.append(square)
        return allowed_moves
