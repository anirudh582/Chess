from Piece.Rook import Rook
from Piece.Bishop import Bishop
from helper import *

class Queen:
    id = 'Q'
    def __init__(self,alliance,coord):
        self.alliance = alliance
        self.coord = coord
    def allowed_moves(self, new_board):
        allowed_moves=[]
        board = new_board.board

        #half file #1
        square = (self.coord[0],self.coord[1]+1)
        while coord_inside_board(square) and null_piece(board,square):
            allowed_moves.append(square)
            square = (square[0],square[1]+1)
        else:
            if coord_inside_board(square) and enemy_piece(board,square,self.alliance):
                allowed_moves.append(square)
        
        #half file #2
        square = (self.coord[0],self.coord[1]-1)
        while coord_inside_board(square) and null_piece(board,square):
            allowed_moves.append(square)
            square = (square[0],square[1]-1)
        else:
            if coord_inside_board(square) and enemy_piece(board,square,self.alliance):
                allowed_moves.append(square)

        #half rank #1
        square = (self.coord[0]+1,self.coord[1])
        while coord_inside_board(square) and null_piece(board,square):
            allowed_moves.append(square)
            square = (square[0]+1,square[1])
        else:
            if coord_inside_board(square) and enemy_piece(board,square,self.alliance):
                allowed_moves.append(square)
        
        #half rank #2
        square = (self.coord[0]-1,self.coord[1])
        while coord_inside_board(square) and null_piece(board,square):
            allowed_moves.append(square)
            square = (square[0]-1,square[1])
        else:
            if coord_inside_board(square) and enemy_piece(board,square,self.alliance):
                allowed_moves.append(square)
        
        #diag1
        square = ((self.coord[0]+1,self.coord[1]+1))
        while coord_inside_board(square) and null_piece(board,square):  
            allowed_moves.append(square)
            square = (square[0]+1,square[1]+1)
        else:
            if coord_inside_board(square) and enemy_piece(board,square,self.alliance):
                allowed_moves.append(square)
        #diag2
        square = ((self.coord[0]-1,self.coord[1]+1))
        while coord_inside_board(square) and null_piece(board,square):  
            allowed_moves.append(square)
            square = (square[0]-1,square[1]+1)
        else:
            if coord_inside_board(square) and enemy_piece(board,square,self.alliance):
                allowed_moves.append(square)
        #diag3
        square = ((self.coord[0]-1,self.coord[1]-1))
        while coord_inside_board(square) and null_piece(board,square):  
            allowed_moves.append(square)
            square = (square[0]-1,square[1]-1)
        else:
            if coord_inside_board(square) and enemy_piece(board,square,self.alliance):
                allowed_moves.append(square)
        #diag4
        square = ((self.coord[0]+1,self.coord[1]-1))
        while coord_inside_board(square) and null_piece(board,square):  
            allowed_moves.append(square)
            square = (square[0]+1,square[1]-1)
        else:
            if coord_inside_board(square) and enemy_piece(board,square,self.alliance):
                allowed_moves.append(square)

        return allowed_moves
