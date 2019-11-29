from helper import *
import settings

class King:
    id = 'K'
    def __init__(self,alliance,coord):
        self.alliance = alliance
        self.coord = coord
        self.moved = False
    def allowed_moves(self,new_board):
        allowed_moves=[]
        board = new_board.board
        for i in range(-1,2):
            for j in range(-1,2):
                if i == 0 and j == 0:
                    continue
                square = (self.coord[0]+i,self.coord[1]+j)
                if coord_inside_board(square) and ((null_piece(board,square) and not new_board.check(square,self.alliance)) or enemy_piece(board,square,self.alliance)):
                    allowed_moves.append(square)

        #castling
        if self.alliance == 'W':
            #castling short
            king_side_rook = board[7][7] if board[7][7].id == 'R' else False
            if king_side_rook:
                if not settings.flip:
                    can_castle_shortside = (not self.moved) and (not new_board.king_in_check(self.alliance)) and (not king_side_rook.moved) and (null_piece(board,(5,7)) and not new_board.check((5,7),self.alliance)) and  (null_piece(board,(6,7)) and not new_board.check((6,7),self.alliance))
                    if can_castle_shortside:
                        allowed_moves.append((6,7))
                else:
                    can_castle_shortside = (not self.moved) and (not new_board.king_in_check(self.alliance)) and (not king_side_rook.moved) and (null_piece(board,(1,7)) and not new_board.check((1,7),self.alliance)) and  (null_piece(board,(2,7)) and not new_board.check((2,7),self.alliance))
                    if can_castle_shortside:
                        allowed_moves.append((1,7))
            
            #castling long
            queen_side_rook = board[0][7] if board[0][7].id == 'R' else False
            if queen_side_rook:
                can_castle_long_side = (not self.moved) and (not new_board.king_in_check(self.alliance)) and (not queen_side_rook.moved)
                castling_squares = []
                if not settings.flip:
                    castling_squares.append((1,7)); castling_squares.append((2,7)); castling_squares.append((3,7))
                    for square in castling_squares:
                        if null_piece(board,square) and not new_board.check(square,self.alliance): 
                            continue
                        else:
                            can_castle_long_side = can_castle_long_side and False
                            break 
                    if can_castle_long_side:
                        allowed_moves.append((2,7))
                else:
                    castling_squares.append((4,7)); castling_squares.append((5,7)); castling_squares.append((6,7))
                    for square in castling_squares:
                        if null_piece(board,square) and not new_board.check(square,self.alliance): 
                            continue
                        else:
                            can_castle_long_side = can_castle_long_side and False
                            break 
                    if can_castle_long_side:
                        allowed_moves.append((5,7))

        if self.alliance == 'B':
            #castling short
            king_side_rook = board[0][7] if board[0][7].id == 'R' else False
            if king_side_rook:
                if not settings.flip:
                    can_castle_shortside = (not self.moved) and (not new_board.king_in_check(self.alliance)) and (not king_side_rook.moved) and (null_piece(board,(5,0)) and not new_board.check((5,0),self.alliance)) and  (null_piece(board,(6,0)) and not new_board.check((6,0),self.alliance))
                    if can_castle_shortside:
                        allowed_moves.append((6,0))
                else:
                    can_castle_shortside = (not self.moved) and (not new_board.king_in_check(self.alliance)) and (not king_side_rook.moved) and (null_piece(board,(1,0)) and not new_board.check((1,0),self.alliance)) and  (null_piece(board,(2,0)) and not new_board.check((2,0),self.alliance))
                    if can_castle_shortside:
                        allowed_moves.append((1,0))

            
            #castling long
            queen_side_rook = board[0][0] if board[0][0].id == 'R' else False
            if queen_side_rook:
                can_castle_long_side = (not self.moved) and (not new_board.king_in_check(self.alliance)) and (not queen_side_rook.moved)
                castling_squares = []
                if not settings.flip:
                    castling_squares.append((1,0)); castling_squares.append((2,0)); castling_squares.append((3,0))
                    for square in castling_squares:
                        if null_piece(board,square) and not new_board.check(square,self.alliance): 
                            continue
                        else:
                            can_castle_long_side = can_castle_long_side and False
                            break 
                    if can_castle_long_side:
                        allowed_moves.append((2,0))
                else:
                    castling_squares.append((4,0)); castling_squares.append((5,0)); castling_squares.append((6,0))
                    for square in castling_squares:
                        if null_piece(board,square) and not new_board.check(square,self.alliance): 
                            continue
                        else:
                            can_castle_long_side = can_castle_long_side and False
                            break 
                    if can_castle_long_side:
                        allowed_moves.append((5,0))
                     
        
        return allowed_moves
    def set_moved(self):
        self.moved = True
