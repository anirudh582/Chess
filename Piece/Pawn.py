from helper import *
class Pawn:
    id = 'P'
    def __init__(self,alliance,coord):
        self.alliance = alliance
        self.coord = coord

    def allowed_moves(self,board):
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
            if coord_inside_board(coord) and null_piece(board,coord):
                allowed_moves.append(coord)
            else:
                break

        #check for pawn captures
        if self.alliance == 'W':
            diag_squares = []
            diag_squares.append((self.coord[0]+1,self.coord[1]-1))
            diag_squares.append((self.coord[0]-1,self.coord[1]-1))
            for square in diag_squares:
                if enemy_piece(board,square,self.alliance):
                    allowed_moves.append(square)

        if self.alliance == 'B':
            diag_squares = []
            diag_squares.append((self.coord[0]+1,self.coord[1]+1))
            diag_squares.append((self.coord[0]-1,self.coord[1]+1))
            for square in diag_squares:
                if enemy_piece(board,square,self.alliance):
                    allowed_moves.append(square)

        #implement pawn en-passant

        return allowed_moves                
