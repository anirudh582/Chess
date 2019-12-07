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

tile_width = int(board_width/8)
tile_height = int(board_height/8)
buff = (tile_width+tile_height)//2


board_width=int(board_width/8)*8
board_height=int(board_height/8)*8
screen = pygame.display.set_mode((board_width+buff,board_height),HWSURFACE|DOUBLEBUF|RESIZABLE)
pygame.display.set_caption('Chess')


initial_square = ()
final_square = ()
listening_thread_started = False
turn = 'W'
checkmate = False
timeout = False
history = []
seek = -1
time = 5
opponent_time = time
status = 'not ready'
status_thread_started = False
