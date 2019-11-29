import settings
import pygame
from pygame.locals import *
import copy
import random
from helper import *
from functions import *
from ChessBoard import ChessBoard
from Piece.Rook import Rook
from Piece.Knight import Knight
from Piece.Bishop import Bishop
from Piece.Queen import Queen
from Piece.King import King
from Piece.Pawn import Pawn
from Piece.Null import Null

import socket
import pickle

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("10.10.10.109",1234))
player_alliance = s.recv(2048).decode()
print(f'player_alliance = {player_alliance}')

if player_alliance =='W':
    settings.flip = False
elif player_alliance == 'B':
    settings.flip = True


new_board = ChessBoard()

plot_canvas()
plot_board(new_board)

img=None
image_draging = False
piece = None
allowed_moves = []
offset_x = None
offset_y = None
turn = 'W'
board_height = settings.board_height
board_width = settings.board_width
tile_width = settings.tile_width
tile_height = settings.tile_height
screen = settings.screen
flip = settings.flip
resize = []
videoresize = False 
accept_move = False
initial_square = ()
prev_initial_square = ()
final_square = ()
move_accepted = False
game_start = True


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == VIDEORESIZE:
            resize.append(event.dict['size'])
            videoresize = True
        if turn == player_alliance:        
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = event.pos
                j,i = int(mouse_x/tile_width), int(mouse_y/tile_height)
                if flip:
                    i = 7-i
                    mouse_y = (board_height-tile_height) - mouse_y
                if new_board.board[i][j].id != "-" and new_board.board[i][j].alliance == turn:
                    img = load_image(new_board,(i,j))
                    piece = new_board.board[i][j]
                    allowed_moves = new_board.board[i][j].allowed_moves(new_board)
                    mark_allowed_moves(new_board,allowed_moves,piece)
                    new_board.board[i][j] = Null((j,i))
                    image_draging = True
                    x,y = j*tile_width, i*tile_height
                    offset_x, offset_y = mouse_x - x, mouse_y-y 
                    initial_square = (j,i)

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and image_draging:
                image_draging = False
                mouse_x, mouse_y = event.pos
                m, l = int(mouse_x / tile_width), int(mouse_y / tile_height)
                if flip:
                    l = 7-l
                if (m,l) in allowed_moves: 
                    turn, temp_initial_square, temp_final_square, move_accepted = accept_move_only_if_doesnt_result_in_check(new_board,piece,(m,l),turn,initial_square)
                    if temp_initial_square:
                        prev_initial_square = temp_initial_square
                    if temp_final_square:
                        final_square = temp_final_square
                else:
                    reject_move(new_board,piece)
                plot_canvas()
                plot_board(new_board)

            elif event.type == pygame.MOUSEMOTION and image_draging:
                mouse_x, mouse_y = event.pos
                plot_canvas()
                plot_board(new_board)
                mark_allowed_moves(new_board,allowed_moves,piece)
                if flip:
                    screen.blit(img,(mouse_x-offset_x,mouse_y+offset_y))
                else:
                    screen.blit(img,(mouse_x-offset_x,mouse_y-offset_y))

            if move_accepted:
                if settings.flip:
                    data = (player_alliance, (7-prev_initial_square[0],prev_initial_square[1]), (7-final_square[0],final_square[1]))
                else:
                    data = (player_alliance, prev_initial_square, final_square)
                s.send(pickle.dumps(data))
                print('sent:', data)
                move_accepted = False
                
        else:
            data = pickle.loads(s.recv(2048))
            print('received:', data)
            player_alliance_recv, opp_init_sq_temp, opp_final_sq_temp = data
            if settings.flip:
                opp_init_sq = (7-opp_init_sq_temp[0], opp_init_sq_temp[1])
                opp_final_sq = (7-opp_final_sq_temp[0], opp_final_sq_temp[1])
            else:
                opp_init_sq = opp_init_sq_temp
                opp_final_sq = opp_final_sq_temp
            print(opp_init_sq,opp_final_sq)    
            moved_piece = new_board.board[opp_init_sq[1]][opp_init_sq[0]]
            new_board.board[opp_init_sq[1]][opp_init_sq[0]] = Null(opp_init_sq)
            new_board.board[opp_final_sq[1]][opp_final_sq[0]] = moved_piece
            if moved_piece.id == 'K':
                new_board.update_king_position(coord,piece.alliance)
                move_rook_if_castling(new_board,piece,coord)
            if moved_piece.id == 'R' or moved_piece.id == 'K':
                new_board.board[opp_final_sq[1]][opp_final_sq[0]].set_moved()
            new_board.update_all_attacked_squares()
            plot_canvas()
            plot_board(new_board)
            prev_initial_square = opp_init_sq
            final_square = opp_final_sq
            if new_board.king_in_check(turn):
                coord = new_board.king[turn]
                if flip:
                    draw_red_wireframe_circle((coord[0],7-coord[1]))
                else:
                    draw_red_wireframe_circle(coord)
            if(data):
                turn = 'B' if turn == 'W' else 'W'
    
    if new_board.king_in_check(turn):
        coord = new_board.king[turn]
        if flip:
            draw_red_wireframe_circle((coord[0],7-coord[1]))
        else:
            draw_red_wireframe_circle(coord)

    if videoresize:
        settings.board_width, settings.board_height = resize[-1]
        settings.board_width = settings.board_width//8*8
        settings.board_height = settings.board_width
        settings.tile_width = settings.board_width//8
        settings.tile_height = settings.tile_width
        tile_width = settings.tile_width
        tile_height = settings.tile_width
        board_height = settings.board_width
        board_width = settings.board_width
        screen = pygame.display.set_mode((settings.board_width,settings.board_width),HWSURFACE|DOUBLEBUF|RESIZABLE)
        pygame.display.update()
        plot_canvas()
        plot_board(new_board)
        videoresize = False

    mark_move(prev_initial_square,final_square)
    pygame.display.update()
    pygame.time.Clock().tick(100)
