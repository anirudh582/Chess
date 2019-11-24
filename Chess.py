import pygame
from helper import *
from ChessBoard import ChessBoard
from Piece.Rook import Rook
from Piece.Knight import Knight
from Piece.Bishop import Bishop
from Piece.Queen import Queen
from Piece.King import King
from Piece.Pawn import Pawn
from Piece.Null import Null

(width, height) = (800,800)

screen = pygame.display.set_mode((width,height))
pygame.display.set_caption('Chess')

tile_width = 100
tile_height = 100

def plot_canvas():
    xpos = 0
    ypos = 0
    global tile_width
    global tile_height
    white = True
    color_white = (255,233,201)
    color_black = (181,135,94)
    for i in range(8):
        for j in range(8):
            color = color_white if white else color_black
            pygame.draw.rect(screen,color,(xpos,ypos,tile_width,tile_height))
            white = not white
            xpos+=100
        white = not white
        xpos = 0
        ypos+=100

def plot_board(new_board):
    xpos = 0
    ypos = 0
    global tile_width
    global tile_height
    for i in range(8):
        for j in range(8):
            if new_board.board[i][j].id != '-':
                img = pygame.image.load('ChessArt/' + new_board.board[i][j].alliance + new_board.board[i][j].id + '.png')
                img = pygame.transform.smoothscale(img, (tile_width, tile_height))
                screen.blit(img, (xpos, ypos))

            xpos += 100
        xpos = 0
        ypos += 100

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

def mark_allowed_moves(allowed_moves,alliance):
    global tile_width
    global tile_height
    global new_board
    for coord in allowed_moves:
        if null_piece(new_board.board, coord):
            pygame.draw.circle(screen, (99,191,124),(coord[0]*tile_width+tile_width/2,coord[1]*tile_height+tile_height/2),15)
        elif enemy_piece(new_board.board, coord, alliance):
            pygame.draw.circle(screen, (255,0,0),(coord[0]*tile_width+tile_width/2,coord[1]*tile_height+tile_height/2),15)

new_board = ChessBoard()

new_board.show_board()


img=None
image_draging = False
piece = None
allowed_moves = []
offset_x = None
offset_y = None
turn = 'W'

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = event.pos
            j,i = int(mouse_x/tile_width), int(mouse_y/tile_height)
            if new_board.board[i][j].id != "-" and new_board.board[i][j].alliance == turn:
                img = pygame.image.load('ChessArt/' + new_board.board[i][j].alliance + new_board.board[i][j].id + '.png')
                img = pygame.transform.smoothscale(img, (tile_width, tile_height))
                piece = new_board.board[i][j]
                allowed_moves = new_board.board[i][j].allowed_moves(new_board)
                mark_allowed_moves(allowed_moves,piece.alliance)
                pygame.display.update()
                new_board.board[i][j] = Null((i,j))
                image_draging = True
                x,y = j*tile_width, i*tile_height
                offset_x, offset_y = mouse_x - x, mouse_y-y 


        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and image_draging:
            image_draging = False
            mouse_x, mouse_y = event.pos
            m, l = int(mouse_x / tile_width), int(mouse_y / tile_height)
            if (m,l) in allowed_moves:
                new_board.board[l][m] = create_piece(piece.id, piece.alliance, (m,l))
                screen.blit(img,(m*tile_height,l*tile_width))
                pygame.display.update()
                if piece.id == 'K':
                    new_board.update_king_position((m,l),piece.alliance)
                new_board.update_attacked_squares(piece.alliance)
                turn = 'B' if turn=='W' else 'W'
            else:
                new_board.board[piece.coord[1]][piece.coord[0]] = piece
                screen.blit(img, (piece.coord[1]*tile_height,piece.coord[0]*tile_width))
            img_name=None

        elif event.type == pygame.MOUSEMOTION and image_draging:
            mouse_x, mouse_y = event.pos
            mark_allowed_moves(allowed_moves,piece.alliance)
            screen.blit(img,(mouse_x-offset_x,mouse_y-offset_y))
            pygame.display.update()

#    print(check(new_board.board,new_board.king['W'],'W'))
#    print(new_board.attacked_squares)
    plot_canvas()
    plot_board(new_board)
    pygame.display.update()
    pygame.time.Clock().tick(100)
