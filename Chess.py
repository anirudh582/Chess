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
import threading

pygame.init()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
if hasattr(socket, "TCP_KEEPIDLE") and hasattr(socket, "TCP_KEEPINTVL") and hasattr(socket, "TCP_KEEPCNT"):
    print('inside tcp options if')
    s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 1 * 60)
    s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 2 * 60)
    s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 20)
s.connect(("34.82.161.100",1234))
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
image_clicking = False
image_draging = False
piece = None
marked_piece = None
allowed_moves = []
offset_x = None
offset_y = None
screen = settings.screen
resize = []
videoresize = False 
accept_move = False
initial_square = ()
move_accepted = False
game_start = True

pygame.time.set_timer(pygame.USEREVENT,1000)



running = True
while running:

    if settings.status == "not ready" and not settings.status_thread_started:
        thread = threading.Thread(target=status, args=(new_board,s))
        thread.daemon = True
        thread.start()
        settings.status_thread_started = True
         
        font = pygame.font.SysFont("comicsans", 30)
        msg = "Waiting for Opponent"
        text_width, text_height = font.size(msg)
        text = font.render(msg, 1, (0,0,255), True)
        settings.screen.blit(text,((settings.board_width-text_width)/2, (settings.board_height-text_height)/2))

    if settings.turn == player_alliance or settings.listening_thread_started:        
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

            elif event.type == VIDEORESIZE:
                resize.append(event.dict['size'])
                videoresize = True

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not settings.listening_thread_started and settings.seek==len(settings.history)-1 and int(settings.time*60)>0 and settings.status == "ready":
                mouse_x, mouse_y = event.pos
                j,i = int(mouse_x/settings.tile_width), int(mouse_y/settings.tile_height)
                if settings.flip:
                    i = 7-i
                    mouse_y = (settings.board_height-settings.tile_height) - mouse_y
                if coord_inside_board((j,i)) and new_board.board[i][j].id != "-" and new_board.board[i][j].alliance == settings.turn:
                    if marked_piece == None or (marked_piece!=None and marked_piece.coord != (j,i)):
                        img = load_image(new_board,(i,j))
                        piece = new_board.board[i][j]
                        allowed_moves = new_board.board[i][j].allowed_moves(new_board)
                        mark_allowed_moves(new_board,allowed_moves,piece)
                        new_board.board[i][j] = Null((j,i))
                        x,y = j*settings.tile_width, i*settings.tile_height
                        offset_x, offset_y = mouse_x - x, mouse_y-y 
                        initial_square = (j,i)
                        marked_piece=None
                    if marked_piece!=None and marked_piece.coord == (j,i):
                        marked_piece=None
                        initial_square = ()
                        new_board.board[i][j] = Null((j,i))
                    draw_transparent_green_square((j,i))
                    image_clicking = True

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                temp_initial_square=()
                temp_final_square=()
                mouse_x, mouse_y = event.pos
                m, l = int(mouse_x / settings.tile_width), int(mouse_y / settings.tile_height)
                if settings.flip:
                    l = 7-l
                if (m,l) in allowed_moves: 
                    if (marked_piece == None and piece!=None and initial_square) or image_draging:
                        temp_initial_square, temp_final_square, move_accepted, taken_piece = accept_move_only_if_doesnt_result_in_check(new_board,piece,(m,l),piece.coord)
                    elif marked_piece!=None:
                        new_board.board[marked_piece.coord[1]][marked_piece.coord[0]] = Null(marked_piece.coord)
                        temp_initial_square, temp_final_square, move_accepted, taken_piece = accept_move_only_if_doesnt_result_in_check(new_board,marked_piece,(m,l),marked_piece.coord)
                    if temp_initial_square:
                        settings.initial_square = temp_initial_square
                    if temp_final_square:
                        settings.final_square = temp_final_square
                elif (m,l) == initial_square and piece!=None:
                    reject_move(new_board,piece)
                    marked_piece = piece
                else:
                    if piece!=None:
                        reject_move(new_board,piece)
                    piece=None
                    marked_piece=None
                if int(settings.time*60)>0 and not settings.checkmate:
                    plot_canvas()
                if marked_piece!=None and (m,l) == marked_piece.coord and not move_accepted:
                    draw_transparent_green_square((m,l))
                if int(settings.time*60)>0 and not settings.checkmate:
                    plot_board(new_board)
                mark_king(new_board)
                if marked_piece!=None and (m,l) == marked_piece.coord and not move_accepted:
                    mark_allowed_moves(new_board,allowed_moves,piece)
                mark_move()
                image_clicking = False
                image_draging = False

            elif event.type == pygame.MOUSEMOTION and image_clicking:
                mouse_x, mouse_y = event.pos
                plot_canvas()
                draw_transparent_green_square(piece.coord)
                plot_board(new_board)
                mark_allowed_moves(new_board,allowed_moves,piece)
                if settings.flip:
                    screen.blit(img,(mouse_x-offset_x,mouse_y+offset_y))
                else:
                    screen.blit(img,(mouse_x-offset_x,mouse_y-offset_y))
                image_draging = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if len(settings.history)>0 and settings.seek>=0:
                        (prev_move_alliance, prev_move_init_sq_temp, prev_move_final_sq_temp, _), prev_taken_piece = settings.history[settings.seek]
                        if settings.flip:
                            prev_move_init_sq = (7-prev_move_init_sq_temp[0],prev_move_init_sq_temp[1])
                            prev_move_final_sq = (7-prev_move_final_sq_temp[0], prev_move_final_sq_temp[1])
                        else:
                            prev_move_init_sq = prev_move_init_sq_temp
                            prev_move_final_sq = prev_move_final_sq_temp
                        settings.seek -= 1
                        moved_piece = new_board.board[prev_move_final_sq[1]][prev_move_final_sq[0]]
                        new_board.board[prev_move_final_sq[1]][prev_move_final_sq[0]] = prev_taken_piece
                        new_board.board[prev_move_init_sq[1]][prev_move_init_sq[0]] = moved_piece
                        plot_canvas()
                        plot_board(new_board)
                if event.key == pygame.K_RIGHT:
                    if len(settings.history)>0 and settings.seek<len(settings.history)-1:
                        (next_move_alliance, next_move_init_sq_temp, next_move_final_sq_temp, _), next_taken_piece = settings.history[settings.seek+1]
                        if settings.flip:
                            next_move_init_sq = (7-next_move_init_sq_temp[0],next_move_init_sq_temp[1])
                            next_move_final_sq = (7-next_move_final_sq_temp[0], next_move_final_sq_temp[1])
                        else:
                            next_move_init_sq = next_move_init_sq_temp
                            next_move_final_sq = next_move_final_sq_temp
                        settings.seek += 1
                        moved_piece = new_board.board[next_move_init_sq[1]][next_move_init_sq[0]]
                        new_board.board[next_move_init_sq[1]][next_move_init_sq[0]] = Null(next_move_init_sq)
                        new_board.board[next_move_final_sq[1]][next_move_final_sq[0]] = moved_piece
                        plot_canvas()
                        plot_board(new_board)
                        
            elif event.type == pygame.USEREVENT:
                if len(settings.history)>1 and not settings.listening_thread_started and int(settings.time*60)>0 and not settings.checkmate:
                    settings.time = settings.time - 1/60

                elif len(settings.history)>1 and settings.listening_thread_started and int(settings.opponent_time*60)>0 and not settings.checkmate:
                    settings.opponent_time = settings.opponent_time - 1/60

            if move_accepted:

                if len(settings.history)>1 and not settings.listening_thread_started and int(settings.time*60)>0 and not settings.checkmate:
                    settings.time += settings.increment/60

                if settings.flip:
                    data = [player_alliance, (7-settings.initial_square[0],settings.initial_square[1]), (7-settings.final_square[0],settings.final_square[1]),settings.time]
                else:
                    data = [player_alliance, settings.initial_square, settings.final_square,settings.time]
                s.sendall(pickle.dumps(data))
                print('sent: ', data)
                move_accepted = False
                settings.history.append((data,taken_piece))
                settings.seek = len(settings.history)-1
                marked_piece = None
                piece = None
                

            

    elif settings.turn != player_alliance and not settings.listening_thread_started:
        thread = threading.Thread(target=receive_opponent_move, args=(new_board,s))
        thread.daemon = True
        thread.start()
        settings.listening_thread_started = True
    

    if videoresize:
        settings.board_width, settings.board_height = resize[-1]
        settings.board_width = settings.board_width//8*8
        settings.board_height = settings.board_width
        settings.tile_width = settings.board_width//8
        settings.tile_height = settings.tile_width
        settings.buff = settings.tile_width
        screen = pygame.display.set_mode((settings.board_width+settings.buff,settings.board_width),HWSURFACE|DOUBLEBUF|RESIZABLE)
        pygame.display.update()
        plot_canvas()
        plot_board(new_board)
        mark_move()
        mark_king(new_board)
        videoresize = False

    if not settings.listening_thread_started:
        mark_move()
        

    text1 = str(int(settings.time/1))+ ":" + str(int(settings.time%1 * 60)).zfill(2)
    text2 = str(int(settings.opponent_time//1)) + ":" + str(int(settings.opponent_time%1 * 60)).zfill(2)
    font = pygame.font.SysFont('Consolas',20)
    text1_width, text1_height = font.size(text1)
    text2_width, text2_height = font.size(text2)
    pygame.draw.rect(screen, (61, 55, 55), (settings.board_width,0,settings.buff,settings.board_height))
    if player_alliance == 'W':
        if not settings.flip:
            screen.blit(font.render(text1,True,(0,255,0)),(settings.board_width+(settings.buff-text1_width)/2,settings.board_height-0.025*settings.tile_height-text1_height))
            screen.blit(font.render(text2,True,(0,255,0)),(settings.board_width+(settings.buff-text2_width)/2,0.1*settings.tile_height))
        else:
            screen.blit(font.render(text1,True,(0,255,0)),(settings.board_width+(settings.buff-text1_width)/2,0.1*settings.tile_height))
            screen.blit(font.render(text2,True,(0,255,0)),(settings.board_width+(settings.buff-text2_width)/2,settings.board_height-0.025*settings.tile_height-text2_height))

    else:
        if settings.flip:
            screen.blit(font.render(text1,True,(0,255,0)),(settings.board_width+(settings.buff-text1_width)/2,settings.board_height-0.025*settings.tile_height-text1_height))
            screen.blit(font.render(text2,True,(0,255,0)),(settings.board_width+(settings.buff-text2_width)/2,0.1*settings.tile_height))
        else:
            screen.blit(font.render(text1,True,(0,255,0)),(settings.board_width+(settings.buff-text1_width)/2,0.1*settings.tile_height))
            screen.blit(font.render(text2,True,(0,255,0)),(settings.board_width+(settings.buff-text2_width)/2,settings.board_height-0.025*settings.tile_height-text2_height))

    if int(settings.time*60) == 0 and int(settings.opponent_time*60)>0 and not settings.timeout:
        winner = "White" if player_alliance == 'B' else "Black"
        msg = "Timeout " + winner + " Wins!"
        text_width, text_height = font.size(msg)
        text = font.render(msg, 1, (0,0,255), True)
        settings.screen.blit(text,((settings.board_width-text_width)/2, (settings.board_height-text_height)/2))
        settings.timeout = True
    elif int(settings.time*60) > 0 and int(settings.opponent_time*60)==0 and not settings.timeout:
        winner = "Black" if player_alliance == 'B' else "White"
        msg = "Timeout " + winner + " Wins!"
        text_width, text_height = font.size(msg)
        text = font.render(msg, 1, (0,0,255), True)
        settings.screen.blit(text,((settings.board_width-text_width)/2, (settings.board_height-text_height)/2))
        settings.timeout = True
    
    pygame.display.update()
    pygame.time.Clock().tick(100)
