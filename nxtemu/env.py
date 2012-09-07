#!/usr/bin/env python
import pygame, random, math, time, sys, os, ConfigParser
from pygame.locals import * 

import imgs

w = 640 
h = 480

def p(path):
    """Nasty monkey patch - shall be removed"""
    import os
    from os.path import abspath, dirname
    return dirname(abspath(sys.argv[0])).replace('library.zip', '') + os.sep \
            + path

WALL_HEIGHT = 3

window = pygame.display.set_mode((w + WALL_HEIGHT*2 + 378,h + WALL_HEIGHT*2)) 
screen = pygame.display.get_surface() 
background = pygame.Surface(screen.get_size()).convert()
cfg = ConfigParser.RawConfigParser()

def init():
    cfg.read(p('config.ini'))

    bckg = cfg.get('nxtemu', 'bckg')

    background.fill((255, 255, 255))

    pygame.display.set_caption("nxtemu")
    #background.blit(pygame.image.load("./icons/brick.jpg").convert(), (640, 0))
    background.blit(imgs.brick.convert(), (640, 0))

    pygame.draw.rect(background, pygame.Color("gray"), ((0, 0), (646, 486)))
    pygame.draw.rect(background, pygame.Color("white"), ((3, 3), (640, 480)))

    if bckg:
        try:
            img = pygame.image.load(bckg)
            if img.get_alpha() != None:
                img = img.convert_alpha()
            else:
                img = img.convert()
            background.blit(img, (3, 3))
        except:
            pass
