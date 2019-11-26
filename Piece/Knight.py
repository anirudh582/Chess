from helper import *
class Knight:
    id = 'N'
    def __init__(self,alliance,coord):
        self.alliance = alliance
        self.coord = coord
        
    def allowed_moves(self,new_board):
        allowed_moves = []
        board = new_board.board
        temp = []
        temp.append((self.coord[0]+2,self.coord[1]+1))
        temp.append((self.coord[0]+2,self.coord[1]-1))
        temp.append((self.coord[0]-2,self.coord[1]+1))
        temp.append((self.coord[0]-2,self.coord[1]-1))
        temp.append((self.coord[0]+1,self.coord[1]+2))
        temp.append((self.coord[0]+1,self.coord[1]-2))
        temp.append((self.coord[0]-1,self.coord[1]+2))
        temp.append((self.coord[0]-1,self.coord[1]-2))
        for coord in temp:
            if coord_inside_board(coord) and not self_piece(board,coord,self.alliance):
                allowed_moves.append(coord)
        return allowed_moves

        
