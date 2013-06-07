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

def write_config(filename = './config.yml'):
    stream = open(filename, "w")
    yaml.dump(cfg, stream)
    stream.close()

def read_config(filename = './config.yml'):
    stream = open(filename, "r")
    cfg = yaml.load(stream)
    stream.close()
    return cfg

def draw_background():
    bckg = cfg["others"]["background"];
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

def check_brick():
    background.fill((255, 255, 255))

    if robot.brick_hidden:
        pygame.draw.rect(background, pygame.Color("gray"), ((0, 0), (960, 486)))
        pygame.draw.rect(background, pygame.Color("white"), ((3, 3), (954, 480)))
    else:
        background.blit(imgs.brick.convert(), (640, 0))
        pygame.draw.rect(background, pygame.Color("gray"), ((0, 0), (646, 486)))
        pygame.draw.rect(background, pygame.Color("white"), ((3, 3), (640, 480)))

        #draw output cables
        pygame.draw.rect(background, pygame.Color("black"), (728, 0, 26, 29))
        pygame.draw.rect(background, pygame.Color("black"), (788, 0, 26, 29))

        if ports_backup is not None:
            for i, port in ports_backup.iteritems():
                if port is not '' and port != 0 and port is not None:
                    pygame.draw.rect(background, (0, 0, 0), 
                              (735 + 60*(i-1), 463, 26, 34))
                    img = pygame.image.load(p("icons/w_port%d.png" % int(i))).convert()
                    background.blit(img, (735 + 60*int(i-1), 437)) 

    draw_background()

cfg = read_config()
ports_backup = None

def init(ports=None):   
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
        for i, port in ports.iteritems():
            if port is not '' and port is not None and port != 0:
                pygame.draw.rect(background, (0, 0, 0), 
                          (735 + 60*(i-1), 463, 26, 34))
                img = pygame.image.load(p("icons/w_port%d.png" % int(i))).convert()
                background.blit(img, (735 + 60*int(i-1), 437))    

    draw_background()
