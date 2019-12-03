import pygame
from pygame.locals import *
import random
pieces = random.choice(['alpha','cburnett','cheq','leipzig','merida'])
#pieces = 'merida'
res = 'low'
theme = random.choice(['blue','brown','green','pink'])
#theme = 'pink'

flip = random.choice ([False,True]) 

board_width = 500 
board_height = 500 

board_width=int(board_width/8)*8
board_height=int(board_height/8)*8
screen = pygame.display.set_mode((board_width,board_height),HWSURFACE|DOUBLEBUF|RESIZABLE)
pygame.display.set_caption('Chess')

tile_width = int(board_width/8)
tile_height = int(board_height/8)

initial_square = ()
final_square = ()
listening_thread_started = False
turn = 'W'
checkmate = False
history = []
seek = -1
