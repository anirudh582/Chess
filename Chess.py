import pygame
from ChessBoard import ChessBoard 

(width, height) = (800,800)

screen = pygame.display.set_mode((width,height))
pygame.display.set_caption('Chess')
            
xpos = 0
ypos = 0
width = 100
height = 100
white = True 
color_white = (255,233,201)
color_black = (181,135,94)
for i in range(8):
    for j in range(8):
        color = color_white if white else color_black
        pygame.draw.rect(screen,color,(xpos,ypos,width,height))
        white = not white
        xpos+=100     
    white = not white
    xpos = 0
    ypos+=100


new_board = ChessBoard()

new_board.show_board()

xpos = 0
ypos = 0
tile_width = 100
tile_height = 100

for i in range(8):
    for j in range(8):
        if new_board.board[i][j] != '--':
            img = pygame.image.load('ChessArt/'+ new_board.board[i][j]+'.png')
            img = pygame.transform.smoothscale(img,(tile_width,tile_height))
            screen.blit(img,(xpos,ypos))
            
        xpos+=100
    xpos=0
    ypos+=100

pygame.display.update()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

