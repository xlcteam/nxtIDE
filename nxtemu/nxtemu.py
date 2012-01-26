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

yspeed = 0
xspeed = 0
maxspeed = 4
minspeed = -4
stop = 0
accel = 0.1
yup = True
xleft = True

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

        elif keystate[K_LEFT]:
            xleft = True
            if xspeed < maxspeed:
                xspeed += accel
                robot.x -= xspeed
            if xspeed >= maxspeed:
                xspeed = maxspeed
                robot.x -= xspeed
        elif keystate[K_RIGHT]:
            xleft = False
            if xspeed < maxspeed:
                xspeed += accel
                robot.x += xspeed
            if xspeed >= maxspeed:
                xspeed = maxspeed
                robot.x += xspeed
        elif keystate[K_UP]:
            robot.y -= 1
        elif keystate[K_DOWN]:
            robot.y += 1

        if keystate[K_UP]:
            yup = True
            if yspeed < maxspeed:
                yspeed += accel
                robot.y -= yspeed
            if yspeed >= maxspeed:
                yspeed = maxspeed
                robot.y -= yspeed

        elif keystate[K_DOWN]:
            yup = False
            if yspeed < maxspeed:
                yspeed += accel
                robot.y += yspeed
            if yspeed >= maxspeed:
                yspeed = maxspeed
                robot.y += yspeed



        
        # if keys aren't push
        if (not(keystate[K_LEFT]) and not(keystate[K_RIGHT])):
            if xspeed < stop:
                xspeed += accel
                if xleft:
                    robot.x -= xspeed
                else:
                    robot.x += xspeed
            if xspeed > stop:
                xspeed -= accel
                if xleft:
                    robot.x -= xspeed
                else:
                    robot.x += xspeed
            if round(xspeed, 5) == stop:
                xspeed = stop

        if (not(keystate[K_UP]) and not(keystate[K_DOWN])):
            if yspeed < stop:
                yspeed += accel
                if yup:
                    robot.y -= yspeed
                else:
                    robot.y += yspeed
            if yspeed > stop:
                yspeed -= accel
                if yup:
                    robot.y -= yspeed
                else:
                    robot.y += yspeed
            if round(yspeed, 5) == stop:
                yspeed = stop


        if robot.dragged: 
            robot.draw() 
            robot.drag() 
        else:
            robot.tick()

        clock.tick(30) # Frame rate  
