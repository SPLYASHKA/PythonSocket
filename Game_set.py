import sys, random
import pygame
from pygame.math import Vector2

pygame.init()

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
snake_head_color = (173, 101, 112)

red_snake_color = (255, 115, 115)
red_snake_head_color = (255, 64, 64)
red_snake_fruit_t_color = (166, 21, 21)

blue_snake_color = (110, 132, 214)
blue_snake_head_color = (72, 103, 214)
blue_snake_fruit_t_color = (36, 58, 139)

score_color = (56, 77, 12)

# todo надо это отсюда убрать
SCREEN_UPDATE = pygame.USEREVENT
SCREEN_UPDATE_list = [pygame.USEREVENT + 1, pygame.USEREVENT + 2]

def base_screen_fill():
    screen.fill(screen_color)
    # draw grass
    for row in range(cell_number):
        if row % 2 == 0:
            for col in range(cell_number):
                if col % 2 == 0:
                    grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                    pygame.draw.rect(screen, grass_color, grass_rect)
        else:
            for col in range(cell_number):
                if col % 2 != 0:
                    grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                    pygame.draw.rect(screen, grass_color, grass_rect)
