from helper import *
class Pawn:
    id = 'P'
    def __init__(self,alliance,coord):
        self.alliance = alliance
        self.coord = coord

    def get_allowed_moves(self,board):
        allowed_moves = []
        temp = []
        if self.alliance=='W':
            if self.coord[1] == 6:
                temp.append((self.coord[0],self.coord[1]-1))
                temp.append((self.coord[0],self.coord[1]-2))
            else:
                temp.append((self.coord[0],self.coord[1]-1))
                
        else:
            if self.coord[1] == 1:
                temp.append((self.coord[0],self.coord[1]+1))
                temp.append((self.coord[0],self.coord[1]+2))
            else:
                temp.append((self.coord[0],self.coord[1]+1))
                
        for coord in temp:
            if coord_inside_board(coord) and not self_piece(board,coord,self.alliance):
                allowed_moves.append(coord)
        return allowed_moves                
