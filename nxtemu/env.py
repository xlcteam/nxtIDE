#!/usr/bin/env python
import pygame, random, math, time, sys, os
from pygame.locals import *
import yaml

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

stream = open("./config.yml", "r")
cfg = yaml.load(stream)
stream.close()

ports_backup = None

def write_config(filename = './config.yml'):
    stream = open(filename, "w")
    yaml.dump(cfg, stream)
    stream.close()

def check_brick(brick_hidden):
    bckg = cfg["others"]["background"];
    if brick_hidden:
        background.fill((250, 250, 250))

        pygame.draw.rect(background, pygame.Color("gray"), ((0, 0), (960, 486)))
        pygame.draw.rect(background, pygame.Color("white"), ((3, 3), (954, 480)))
    else:
        background.fill((250, 250, 250))
        background.blit(imgs.brick.convert(), (640, 0))
        pygame.draw.rect(background, pygame.Color("gray"), ((0, 0), (646, 486)))
        pygame.draw.rect(background, pygame.Color("white"), ((3, 3), (640, 480)))

        if ports_backup is not None:
            for port in ports_backup:
                if ports_backup[port] is not '':
                    pygame.draw.rect(background, (0, 0, 0), 
                              (735 + 60*(port-1), 463, 26, 34))
                    img = pygame.image.load(p("icons/w_port%d.png" % int(port))).convert()
                    background.blit(img, (735 + 60*int(port-1), 440)) 

    if bckg:
        try:
            img = pygame.image.load(bckg)
            if img.get_alpha() != None:
                img = img.convert_alpha()
            else:
                img = img.convert()
            if brick_hidden:
                img = pygame.transform.scale(img, (960, 480))
            else:            
                img = pygame.transform.scale(img, (640, 480))
            background.blit(img, (3, 3))
        except:
            pass
        

def init(ports=None):
    bckg = cfg["others"]["background"];
    
    background.fill((250, 250, 250))

    pygame.display.set_caption("nxtemu")
    #background.blit(pygame.image.load("./icons/brick.jpg").convert(), (640, 0))
    background.blit(imgs.brick.convert(), (640, 0))

    pygame.draw.rect(background, pygame.Color("gray"), ((0, 0), (646, 486)))
    pygame.draw.rect(background, pygame.Color("white"), ((3, 3), (640, 480)))

    #draw output cables
    pygame.draw.rect(background, pygame.Color("black"), (728, 0, 26, 29))
    pygame.draw.rect(background, pygame.Color("black"), (788, 0, 26, 29))

    ports_backup = ports
    if ports is not None:
        for port in ports:
            if ports[port] is not '':
                pygame.draw.rect(background, (0, 0, 0), 
                          (735 + 60*(port-1), 463, 26, 34))
                img = pygame.image.load(p("icons/w_port%d.png" % int(port))).convert()
                background.blit(img, (735 + 60*int(port-1), 440))    

    if bckg:
        try:
            img = pygame.image.load(bckg)
            if img.get_alpha() != None:
                img = img.convert_alpha()
            else:
                img = img.convert()
            
            img = pygame.transform.scale(img, (640, 480))
            background.blit(img, (3, 3))
        except:
            pass
