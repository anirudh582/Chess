from Piece.Rook import Rook
from Piece.Knight import Knight
from Piece.Bishop import Bishop
from Piece.Queen import Queen
from Piece.King import King
from Piece.Pawn import Pawn
from Piece.Null import Null

class ChessBoard:
    def __init__(self):
        self.board = []
        self.board.append([Rook('B',(0,0)), Knight('B',(1,0)), Bishop('B',(2,0)), Queen('B',(3,0)), King('B',(4,0)), Bishop('B',(5,0)), Knight('B',(6,0)), Rook('B',(7,0))])
        self.board.append([Pawn('B',(0,1)), Pawn('B',(1,1)), Pawn('B',(2,1)), Pawn('B',(3,1)), Pawn('B',(4,1)), Pawn('B',(5,1)), Pawn('B',(6,1)), Pawn('B',(7,1))])
        self.board.append([Null((0,2)), Null((1,2)), Null((2,2)), Null((3,2)), Null((4,2)), Null((5,2)), Null((6,2)), Null((7,2))])
        self.board.append([Null((0,3)), Null((1,3)), Null((2,3)), Null((3,3)), Null((4,3)), Null((5,3)), Null((6,3)), Null((7,3))])
        self.board.append([Null((0,4)), Null((1,4)), Null((2,4)), Null((3,4)), Null((4,4)), Null((5,4)), Null((6,4)), Null((7,4))])
        self.board.append([Null((0,5)), Null((1,5)), Null((2,5)), Null((3,5)), Null((4,5)), Null((5,5)), Null((6,5)), Null((7,5))])
        self.board.append([Pawn('W',(0,6)), Pawn('W',(1,6)), Pawn('W',(2,6)), Pawn('W',(3,6)), Pawn('W',(4,6)), Pawn('W',(5,6)), Pawn('W',(6,6)), Pawn('W',(7,6))])
        self.board.append([Rook('W',(0,7)), Knight('W',(1,7)), Bishop('W',(2,7)), Queen('W',(3,7)), King('W',(4,7)),Bishop('W',(5,7)), Knight('W',(6,7)), Rook('W',(7,7))])
        self.king = {'W':(4,7),'B':(4,7)}
        self.attacked_squares = {'W':[],'B':[]}

    def show_board(self):
        for i in range(8):
            for j in range(8):
                if self.board[i][j].id !='-':
                    print(self.board[i][j].alliance + self.board[i][j].id, end = "|")
                else:
                    print('--', end = "|")
            print()

    def update_king_position(self, coord, alliance):
        self.king[alliance]=coord

    def update_attacked_squares(self, alliance):
        self.attacked_squares[alliance]=[]
        for i in range(8):
            for j in range(8):
                if self.board[i][j].id != '-' and self.board[i][j].alliance != alliance:
                    if self.board[i][j].id == 'P': 
                        for square in self.board[i][j].attack_squares():
                            self.attacked_squares[alliance].append(square)
                    else:
                        for square in self.board[i][j].allowed_moves(self):
                            self.attacked_squares[alliance].append(square)
                            


    def check(self, coord, alliance):
        return coord in self.attacked_squares[alliance]
    
