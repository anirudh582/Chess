import copy
from Piece.Null import Null
def coord_inside_board(coord):
    return coord[0]<=7 and coord[1]<=7 and coord[0]>=0 and coord[1]>=0

def self_piece(board,coord,alliance):
    if board[coord[1]][coord[0]].id != '-':
        if board[coord[1]][coord[0]].alliance == alliance:
            return True

def null_piece(board,coord):
    return board[coord[1]][coord[0]].id == '-'

def enemy_piece(board,coord,alliance):
    if board[coord[1]][coord[0]].id != '-':
        return board[coord[1]][coord[0]].alliance!=alliance

#def check(board,coord,alliance):
#    all_enemy_attack_squares = []
#    for i in range(8):
#        for j in range(8):
#            if board[i][j].id != '-' and board[i][j].alliance != alliance:
#                if board[i][j].id == 'P': 
#                    for square in board[i][j].attack_squares():
#                        all_enemy_attack_squares.append(square)
#                else:
#                    for square in board[i][j].allowed_moves(board):
#                        all_enemy_attack_squares.append(square)
#
#    return coord in all_enemy_attack_squares

def check(board,coord,alliance):
    all_enemy_attack_squares = []
    check = False
    for i in range(8):
        for j in range(8):
            if board[i][j].id != '-' and board[i][j].alliance != alliance:
                if board[i][j].id == 'P': 
                    check = coord in board[i][j].attack_squares()
                    if check:
                        break
                else:
                    check = coord in board[i][j].allowed_moves(board)
                    if check:
                        break

    return check 

def attacked_squares(board,alliance):
    all_enemy_attack_squares = []
    for i in range(8):
        for j in range(8):
            if board[i][j].id != '-' and board[i][j].alliance != alliance:
                if board[i][j].id == 'P': 
                    for square in board[i][j].attack_squares():
                        all_enemy_attack_squares.append(square)
                else:
                    for square in board[i][j].allowed_moves(board):
                        all_enemy_attack_squares.append(square)

    return all_enemy_attack_squares

def filter_by_king_check(allowed_moves,new_board,piece):
    filtered_moves = []
    look_ahead_board = copy.deepcopy(new_board)
    look_ahead_board.board[piece.coord[1]][piece.coord[0]] = Null(piece.coord)
    if new_board.king_in_check(piece.alliance):
        for square in allowed_moves:
            look_ahead_board.board[square[1]][square[0]] = piece
            look_ahead_board.update_attacked_squares(piece.alliance)
            if piece.id == 'K':
                look_ahead_board.update_king_position(square, piece.alliance)
            if look_ahead_board.king_in_check(piece.alliance):
                continue
            else:
                filtered_moves.append(square)
            look_ahead_board.board[square[1]][square[0]] = Null(square)
        return filtered_moves
    else:
        #check for pin
        look_ahead_board.update_all_attacked_squares()
        if look_ahead_board.king_in_check(piece.alliance):
            return []
        else:
            return allowed_moves

