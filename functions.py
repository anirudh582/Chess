import settings
import pygame
import pickle
import copy
from helper import *
from Piece.Rook import Rook
from Piece.Knight import Knight
from Piece.Bishop import Bishop
from Piece.Queen import Queen
from Piece.King import King
from Piece.Pawn import Pawn
from Piece.Null import Null


def plot_canvas():
    xpos = 0
    ypos = 0
    tile_width = settings.tile_width
    tile_height = settings.tile_height
    theme = settings.theme
    screen = settings.screen
    white = True
    if theme == 'brown':
        color_white = (255,233,201)
        color_black = (181,135,94)
    elif theme == 'blue':
        color_white = (237, 243, 245)
        color_black = (119, 142, 153)
    elif theme == 'green':
        color_white = (250, 255, 227)
        color_black = (109, 153, 75)
    elif theme == 'pink':
        color_white = (245, 244, 193)
        color_black = (224, 92, 105)
    for i in range(8):
        for j in range(8):
            color = color_white if white else color_black
            pygame.draw.rect(screen,color,(xpos,ypos,tile_width,tile_height))
            white = not white
            xpos+=tile_width
        white = not white
        xpos = 0
        ypos+=tile_height

def plot_board(new_board):
    xpos = 0
    ypos = 0
    pieces = settings.pieces
    res = settings.res
    tile_width = settings.tile_width
    tile_height = settings.tile_height
    board_height = settings.board_height
    flip = settings.flip
    screen = settings.screen
    for i in range(8):
        for j in range(8):
            if new_board.board[i][j].id != '-':
                img = load_image(new_board,(i,j))
                if not flip:
                    screen.blit(img, (xpos, ypos))
                else:
                    screen.blit(img, (xpos, (board_height-tile_height)-ypos))

            xpos += tile_width 
        xpos = 0
        ypos += tile_height

def create_piece(piece_id, alliance, coord):
    if piece_id == 'R':
        return Rook(alliance,coord)
    elif piece_id == 'N':
        return Knight(alliance,coord)
    elif piece_id == 'B':
        return Bishop(alliance, coord)
    elif piece_id == 'Q':
        return Queen(alliance, coord)
    elif piece_id == 'K':
        return King(alliance, coord)
    elif piece_id == 'P':
        return Pawn(alliance, coord)
    else:
        print("Error, invalid piece. Cannot create piece")
        exit(101)

def draw_green_circle(coord):
    tile_width = settings.tile_width
    tile_height = settings.tile_height
    radius = 0.15*(tile_width+tile_height)/2
    screen = settings.screen
    pygame.draw.circle(screen, (99,191,124),(coord[0]*tile_width+tile_width/2,coord[1]*tile_height+tile_height/2),radius)

def draw_red_circle(coord):
    screen = settings.screen
    tile_width = settings.tile_width
    tile_height = settings.tile_height
    radius = 0.15*(tile_width+tile_height)/2
    pygame.draw.circle(screen, (255,0,0),(coord[0]*tile_width+tile_width/2,coord[1]*tile_height+tile_height/2),radius)

def draw_blue_wireframe_rectangle(coord):
    screen = settings.screen
    tile_width = settings.tile_width
    tile_height = settings.tile_height
    pygame.draw.rect(screen,(0,0,255),(coord[0]*tile_width,coord[1]*tile_height,tile_width,tile_height),int(0.04*tile_width))
    
def draw_red_wireframe_circle(coord):
    screen = settings.screen
    tile_width = settings.tile_width
    tile_height = settings.tile_height
    pygame.draw.circle(screen,(255,0,0),(coord[0]*tile_width+tile_width/2,coord[1]*tile_height+tile_height/2),tile_width/2,int(0.04*tile_width))


def mark_allowed_moves(new_board,allowed_moves,piece):
    tile_width = settings.tile_width
    tile_height = settings.tile_height
    flip = settings.flip
    filtered_moves = filter_by_king_check(allowed_moves,new_board,piece)
    for coord in filtered_moves:
        if flip:
            if null_piece(new_board.board, coord):
                draw_green_circle((coord[0],7-coord[1]))
            elif enemy_piece(new_board.board, coord, piece.alliance):
                draw_red_circle((coord[0],7-coord[1])) 
        else:
            if null_piece(new_board.board, coord):
                draw_green_circle(coord)
            elif enemy_piece(new_board.board, coord, piece.alliance):
                draw_red_circle(coord) 

def mark_squares(squares):
    for coord in squares:
        if settings.flip:
            coord_flipped = (coord[0],7-coord[1])
            draw_red_circle(coord_flipped)
        else:
            draw_red_circle(coord)

def move_rook_if_castling(new_board,king,move_to_coord):
    if not settings.flip:
        if king.alliance == 'W' and king.coord == (4,7):
            if move_to_coord == (6,7):
                new_board.board[7][7] = Null((7,7))
                new_board.board[7][5] = Rook('W',(5,7))
            if move_to_coord == (2,7):
                new_board.board[7][0] = Null((0,7))
                new_board.board[7][3] = Rook('W',(3,7))
        if king.alliance == 'B' and king.coord == (4,0):
            if move_to_coord == (6,0):
                new_board.board[0][7] = Null((7,0))
                new_board.board[0][5] = Rook('B',(5,0))
            if move_to_coord == (2,0):
                new_board.board[0][0] = Null((0,0))
                new_board.board[0][3] = Rook('B',(3,0))
    else:
        if king.alliance == 'W' and king.coord == (3,7):
            if move_to_coord == (1,7):
                new_board.board[7][0] = Null((0,7))
                new_board.board[7][2] = Rook('W',(2,7))
            if move_to_coord == (5,7):
                new_board.board[7][7] = Null((7,7))
                new_board.board[7][4] = Rook('W',(4,7))
        if king.alliance == 'B' and king.coord == (3,0):
            if move_to_coord == (1,0):
                new_board.board[0][0] = Null((0,0))
                new_board.board[0][2] = Rook('B',(2,0))
            if move_to_coord == (5,0):
                new_board.board[0][7] = Null((7,0))
                new_board.board[0][4] = Rook('B',(4,0))
        

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

def load_image(new_board,coord):
    pieces = settings.pieces
    tile_width = settings.tile_width
    tile_height = settings.tile_height
    res = settings.res
    i = coord[0]
    j = coord[1]
    img = pygame.image.load('ChessArt/'+pieces+'/'+res+'/' + new_board.board[i][j].alliance + new_board.board[i][j].id + '.png')
    img = pygame.transform.smoothscale(img, (tile_width, tile_height))
    return img

def accept_move(new_board,piece,coord):
    new_board.board[coord[1]][coord[0]] = create_piece(piece.id, piece.alliance, coord)
    if piece.id == 'K':
        new_board.update_king_position(coord,piece.alliance)
        move_rook_if_castling(new_board,piece,coord)
    if piece.id == 'R' or piece.id == 'K':
        new_board.board[coord[1]][coord[0]].set_moved()
    new_board.update_all_attacked_squares()
    settings.turn = 'B' if settings.turn=='W' else 'W'

def reject_move(new_board, piece):
    new_board.board[piece.coord[1]][piece.coord[0]] = piece

def accept_move_only_if_doesnt_result_in_check(new_board,piece,coord,initial_square):
    prev_initial_square=()
    final_square=()
    move_accepted = False
    look_ahead_board = copy.deepcopy(new_board)
    look_ahead_board.board[coord[1]][coord[0]] = create_piece(piece.id, piece.alliance, coord)
    if piece.id == 'K':
        look_ahead_board.update_king_position(coord,piece.alliance)
    look_ahead_board.update_all_attacked_squares()
    if not look_ahead_board.king_in_check(settings.turn):
        accept_move(new_board,piece,coord)
        prev_initial_square = initial_square
        final_square=coord
        move_accepted = True
    else:
        reject_move(new_board,piece)
    return (prev_initial_square,final_square,move_accepted)

def mark_move():
    initial_square = settings.initial_square
    final_square = settings.final_square
    flip = settings.flip
    if initial_square and final_square:
        if flip:
            draw_blue_wireframe_rectangle((initial_square[0],7-initial_square[1]))
            draw_blue_wireframe_rectangle((final_square[0], 7-final_square[1]))
        else:    
            draw_blue_wireframe_rectangle(initial_square)
            draw_blue_wireframe_rectangle(final_square)

def receive_opponent_move(new_board,socket):
    data = pickle.loads(socket.recv(2048))
    print('received: ', data)
    player_alliance_recv, opp_init_sq_temp, opp_final_sq_temp = data
    if settings.flip:
        opp_init_sq = (7-opp_init_sq_temp[0], opp_init_sq_temp[1])
        opp_final_sq = (7-opp_final_sq_temp[0], opp_final_sq_temp[1])
    else:
        opp_init_sq = opp_init_sq_temp
        opp_final_sq = opp_final_sq_temp
    moved_piece = new_board.board[opp_init_sq[1]][opp_init_sq[0]]
    new_board.board[opp_init_sq[1]][opp_init_sq[0]] = Null(opp_init_sq)
    accept_move(new_board,moved_piece,opp_final_sq)
    plot_canvas()
    plot_board(new_board)
    settings.initial_square = opp_init_sq
    settings.final_square = opp_final_sq
    settings.listening_thread_started = False
