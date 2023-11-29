import sys, random
import pygame
from pygame.math import Vector2

pygame.init()

# base const
framerate = 60

clock = pygame.time.Clock()

SCREEN_UPDATE = pygame.USEREVENT