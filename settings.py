import pygame
import random
pieces = random.choice(['alpha','cburnett','cheq','leipzig','merida'])
#pieces = 'merida'
res = 'low'
theme = random.choice(['blue','brown','green','pink'])
#theme = 'pink'

flip = random.choice ([False,True]) 

(board_width, board_height) = (800,800)
screen = pygame.display.set_mode((board_width,board_height))
pygame.display.set_caption('Chess')

tile_width = 100
tile_height = 100
