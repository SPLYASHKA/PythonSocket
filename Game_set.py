import sys, random
import pygame
from pygame.math import Vector2

pygame.init()

# game set
snake_start_speed = 150  # ms
snake_change_speed = 20
snake_max_speed = 50

# base const
framerate = 60
cell_number = 20  # >= 10 меньше не имеет смысла
cell_size = 40

screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()
game_font = pygame.font.Font(None, 25)

# colors
screen_color = (175, 215, 70)
grass_color = (167, 209, 61)
fruit_color = (126, 166, 114)
fruit_cut_color = (150,5,255)
fruit_t_color = (40,4,255)
snake_color = (183, 111, 122)
alt_snake_color = (0, 0, 0)
snake_head_color = (173, 101, 112)
score_color = (56, 77, 12)

SCREEN_UPDATE = pygame.USEREVENT