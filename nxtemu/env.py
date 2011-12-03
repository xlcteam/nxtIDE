
import pygame, random, math, time, sys, os
from pygame.locals import * 


w = 640 
h = 480


WALL_HEIGHT = 3

window = pygame.display.set_mode((w + WALL_HEIGHT*2 + 378,h + WALL_HEIGHT*2)) 
screen = pygame.display.get_surface() 

