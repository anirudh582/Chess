import pygame
from ChessBoard import ChessBoard 

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
            if new_board.board[i][j] != '--':
                img = pygame.image.load('ChessArt/' + new_board.board[i][j] + '.png')
                img = pygame.transform.smoothscale(img, (tile_width, tile_height))
                screen.blit(img, (xpos, ypos))

            xpos += 100
        xpos = 0
        ypos += 100

new_board = ChessBoard()

new_board.show_board()

img=None
image_draging = False
img_name = None
offset_x = None
offset_y = None

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = event.pos
            j,i = int(mouse_x/tile_width), int(mouse_y/tile_height)
            if new_board.board[i][j] != "--":
                img = pygame.image.load('ChessArt/' + new_board.board[i][j] + '.png')
                img = pygame.transform.smoothscale(img, (tile_width, tile_height))
                img_name = new_board.board[i][j]
                new_board.board[i][j] = "--"
                image_draging = True
                x,y = j*tile_width, i*tile_height
                offset_x, offset_y = mouse_x - x, mouse_y-y 


        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            image_draging = False
            mouse_x, mouse_y = event.pos
            m, l = int(mouse_x / tile_width), int(mouse_y / tile_height)
            new_board.board[l][m] = img_name if img_name != None else "--"
            screen.blit(img,(m*tile_height,l*tile_width))
            pygame.display.update()
            img_name=None

        elif event.type == pygame.MOUSEMOTION and image_draging:
            mouse_x, mouse_y = event.pos
            screen.blit(img,(mouse_x-offset_x,mouse_y-offset_y))
            pygame.display.update()

    plot_canvas()
    plot_board(new_board)
    pygame.display.update()
    #pygame.time.Clock().tick(30)





