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
        self.board.append([Rook('B',(0,0)), Knight('B',(0,1)), Bishop('B',(0,2)), Queen('B',(0,3)), King('B',(0,4)), Bishop('B',(0,5)), Knight('B',(0,6)), Rook('B',(0,7))])
        self.board.append([Pawn('B',(1,0)), Pawn('B',(1,1)), Pawn('B',(1,2)), Pawn('B',(1,3)), Pawn('B',(1,4)), Pawn('B',(1,5)), Pawn('B',(1,6)), Pawn('B',(1,7))])
        self.board.append([Null((3,0)), Null((3,1)), Null((3,2)), Null((3,3)), Null((3,4)), Null((3,5)), Null((3,6)), Null((3,7))])
        self.board.append([Null((4,0)), Null((4,1)), Null((4,2)), Null((4,3)), Null((4,4)), Null((4,5)), Null((4,6)), Null((4,7))])
        self.board.append([Null((5,0)), Null((5,1)), Null((5,2)), Null((5,3)), Null((5,4)), Null((5,5)), Null((5,6)), Null((5,7))])
        self.board.append([Null((6,0)), Null((6,1)), Null((6,2)), Null((6,3)), Null((6,4)), Null((6,5)), Null((6,6)), Null((6,7))])
        self.board.append([Pawn('W',(7,0)), Pawn('W',(7,1)), Pawn('W',(7,2)), Pawn('W',(7,3)), Pawn('W',(7,4)), Pawn('W',(7,5)), Pawn('W',(7,6)), Pawn('W',(7,7))])
        self.board.append([Rook('W',(7,0)), Knight('W',(7,1)), Bishop('W',(7,2)), Queen('W',(7,3)), King('W',(7,4)),Bishop('W',(7,5)), Knight('W',(7,6)), Rook('W',(7,7))])

    def show_board(self):
        for i in range(8):
            for j in range(8):
                if self.board[i][j].id !='-':
                    print(self.board[i][j].alliance + self.board[i][j].id, end = "|")
                else:
                    print('--', end = "|")
            print()