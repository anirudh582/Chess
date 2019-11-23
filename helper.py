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
