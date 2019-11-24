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

def check(board,coord,alliance):
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

    return coord in all_enemy_attack_squares
