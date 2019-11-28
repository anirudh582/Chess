import settings
import pygame
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

tile_width = settings.tile_width
tile_height = settings.tile_height
screen = settings.screen
flip = settings.flip
res = settings.res

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = event.pos
            j,i = int(mouse_x/tile_width), int(mouse_y/tile_height)
            if flip:
                i = 7-i
                mouse_y = 700 - mouse_y
            if new_board.board[i][j].id != "-" and new_board.board[i][j].alliance == turn:
                img = load_image(new_board,(i,j))
                piece = new_board.board[i][j]
                allowed_moves = new_board.board[i][j].allowed_moves(new_board)
                mark_allowed_moves(new_board,allowed_moves,piece)
                new_board.board[i][j] = Null((j,i))
                image_draging = True
                x,y = j*tile_width, i*tile_height
                offset_x, offset_y = mouse_x - x, mouse_y-y 


        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and image_draging:
            image_draging = False
            mouse_x, mouse_y = event.pos
            m, l = int(mouse_x / tile_width), int(mouse_y / tile_height)
            if flip:
                l = 7-l
            if (m,l) in allowed_moves: 
                turn = accept_move_only_if_doesnt_result_in_check(new_board,piece,(m,l),turn)
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
            
            
    if new_board.king_in_check(turn):
        coord = new_board.king[turn]
        if flip:
            draw_red_circle((coord[0],7-coord[1]))
        else:
            draw_red_circle(coord)
       
    pygame.display.update()
    pygame.time.Clock().tick(100)
