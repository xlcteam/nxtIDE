#!/usr/bin/env python

import pygame, random, math, time, sys, os
from pygame.locals import * 

from pgu import gui 

import imgs

from os.path import abspath, dirname
sys.path.append(os.path.dirname(sys.argv[0]))

def p(path):
    """Nasty monkey patch - shall be removed"""
    import os
    from os.path import abspath, dirname
    return dirname(abspath(sys.argv[0])).replace('library.zip', '') + os.sep \
            + path


from api import *
from clicker import Clicker

from robot import Robot
from robothread import *

import env

pygame.init() 
icon = pygame.image.load(p('./icons/nxtemu.png')).convert_alpha()
pygame.display.set_icon(icon)
pygame.mixer.pre_init(44100, -16, 2)


env.init()

#   env.background = pygame.Surface(env.screen.get_size()) 
#   env.background = env.background.convert() 
#   env.background.fill((255, 255, 255))

#   pygame.display.set_caption("nxtemu")
#   #background.blit(pygame.image.load("./icons/brick.jpg").convert(), (640, 0))
#   env.background.blit(imgs.brick.convert(), (640, 0))

#   pygame.draw.rect(env.background, pygame.Color("gray"), ((0, 0), (646, 486)))
#   pygame.draw.rect(env.background, pygame.Color("white"), ((3, 3), (640, 480)))

# background.blit(pygame.image.load("settings.png").convert_alpha(), (970, 400))
#background.blit(pygame.image.load("./line.jpg"), (3, 3))


clock = pygame.time.Clock() 


if __name__ == "__main__":
    env.app = gui.App(theme=gui.Theme(p("theme/default/"))) 
    settings = gui.Image(p("icons/settings.png"))
   # settings.connect
    c = gui.Container(align=-1,valign=-1)
    c.add(settings, 960, 400)
    env.app.init(c, env.screen)    

    running = True 

    if len(sys.argv) > 1:
        robot = Robot(wboot = False)         
        robot.draw()


        prog = sys.argv[1]
        robot.progLoad()
        #print robot.progs
       
        robot.prog = robot.progs.index(prog)
        robot.screen = 3
        robot.wboot = False
        
        def runner():
            robot.scrout()
            Wait(800)
            robot.onCenter()

        RoboThread(target=runner).start()
        
    else:
        robot = Robot()
        robot.draw()


    clicker = Clicker()

    clicker.bind(((810, 252), (41, 40)), robot.onCenter)
    clicker.bind(((810, 308), (41, 26)), robot.onBack)
    clicker.bind(((751, 252), (41, 40)), robot.onLeft)
    clicker.bind(((870, 252), (41, 40)), robot.onRight)
    clicker.bind(((960, 400), (50, 50)), robot.onDialog)

    while running: 
        for event in pygame.event.get(): 
            
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                clicker.process(pygame.mouse.get_pos())
            
            if event.type == QUIT: 
                robot.die = True
                running = False
                pygame.quit()
                sys.exit(0)

            elif event.type == MOUSEBUTTONDOWN and robot.mouseOver(): 

                if event.button == 1:
                    robot.dragged = not robot.dragged
                
                if robot.dragged:
                    pygame.mouse.set_cursor(*pygame.cursors.broken_x)
                else:
                    pygame.mouse.set_cursor(*pygame.cursors.arrow)
   

                if event.button == 4:
                    robot.angle += 1
                    robot.angle = round(robot.angle, 0)
                elif event.button == 5:
                    robot.angle -= 1
                    robot.angle = round(robot.angle, 0)

            env.app.event(event)
            
            
        pygame.event.pump()
        keystate = pygame.key.get_pressed()
        mod = pygame.key.get_mods()

        # move robot by keys
        if keystate[K_LEFT] and mod & KMOD_SHIFT:
            robot.angle -= 1
        elif keystate[K_RIGHT] and mod & KMOD_SHIFT:
            robot.angle += 1

        if robot.dragged: 
            robot.draw() 
            robot.drag() 
        else:
            robot.tick()

        clock.tick(40) # Frame rate  

